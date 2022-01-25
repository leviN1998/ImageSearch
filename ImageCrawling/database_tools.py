import sqlite3
import os


def connect(database_name: str):
    '''
    Connect to db
    '''
    old_wd = os.getcwd()
    os.chdir('ImageDatabases')

    conn = sqlite3.connect(database_name)

    os.chdir(old_wd)
    return conn


def create_table(conn: sqlite3.Connection, table_name: str, column_names, column_types, drop_if_exists: bool=True):
    '''
    '''
    cur = conn.cursor()
    if drop_if_exists:
        cur.execute("DROP TABLE IF EXISTS " + table_name)

    # Handle case that table already exists! TODO
    query_str = "CREATE TABLE " + table_name + " ("
    for n, t in zip(column_names, column_types):
        query_str += n + " " + t + ", "
    query_str = query_str[:-2]
    query_str += ")"
    cur.execute(query_str)
    conn.commit()


def create_images_table(conn: sqlite3.Connection):
    '''
    '''
    names = ["id", "class", "database_name", "website", "data"]
    types = ["int", "text", "text", "text", "BLOB"]
    create_table(conn, "images", names, types, drop_if_exists=True)


def create_feature_table(conn: sqlite3.Connection):
    '''
    '''
    names = ["id", "network", "feature", "hashing"]
    types = ["int", "text", "BLOB", "BLOB"]
    create_table(conn, "features", names, types, drop_if_exists=True)


def create_db(database_name: str):
    '''
    '''
    conn = connect(database_name)
    create_images_table(conn)
    create_feature_table(conn)
    conn.close()


def __print_table(col_names, data, max_elements: int=20, max_element_length: int=20):
    '''
    '''
    # Example result: [(0, 'porcupine', 'cifar_100', 'shutterstock', verylong)]
    cols = []
    for c in col_names:
        cols.append([c, "-"])   
    rows = 0
    for row in data:
        for c, col in zip(row, cols):
            string = str(c)
            if len(string) > max_element_length:
                string = "..."
            col.append(string)
        rows += 1
        if rows == max_elements:
            break
    # make all strings in a column same length
    for i in range(0, len(cols)):
        max_len = 0
        for s in cols[i]:
            if len(s) > max_len:
                max_len = len(s)
        for j in range(0, len(cols[i])):
            diff = max_len - len(cols[i][j])
            if diff > 0:
                filler = " "
                if cols[i][j] == "-":
                    filler = "-"
                string = ""
                for o in range(0, diff):
                    string += filler
                cols[i][j] = string + cols[i][j]
            cols[i][j] = " " + cols[i][j] + " " 
    # print Coloumns
    print()
    for i in range(0, len(cols[0])):
        string = "|"
        for c in cols:
            string += c[i] + "|"
        print(string)
    print()


def print_table(conn: sqlite3.Connection, table_name: str, max_elements: int=20, max_element_length: int=20):
    cur = conn.cursor()
    query_str = "PRAGMA table_info(" + table_name + ")"
    # Example result: (0, 'id', 'int', 0, None, 0)
    cur.execute(query_str)
    table_head = cur.fetchall()
    col_names = []
    for c in table_head:
        col_names.append(c[1])
    
    query_str = "SELECT t.* FROM " + table_name + " AS t"
    cur.execute(query_str)
    table_content = cur.fetchall()
    # Example result: [(0, 'porcupine', 'cifar_100', 'shutterstock', verylong)]
    __print_table(col_names, table_content, max_elements, max_element_length)


def print_info_images(conn: sqlite3.Connection):
    '''
    '''
    cur = conn.cursor()
    sub_query = "images"
    query_str =  "SELECT t.database_name, t.class, count(t.class) "
    query_str += "FROM " + sub_query + " AS t "
    query_str += "GROUP BY t.database_name, t.class "
    query_str += "ORDER BY t.database_name"
    cur.execute(query_str)
    info_result = cur.fetchall()
    __print_table(["database", "class", "count"], info_result)


def print_info_features(conn: sqlite3.Connection):
    '''
    TODO do usefull print
    '''
    cur = conn.cursor()
    query_str =  "SELECT i.database_name, count(i.database_name) "
    query_str += "FROM images AS i "
    query_str += "GROUP BY i.database_name"
    cur.execute(query_str)
    images_infos = cur.fetchall()
    # print(images_infos)     # [('cifar10', 50000), ('cifar10_test', 10000)]
    query_str =  "SELECT i.database_name, f.network, count(f.network) "
    query_str += "FROM images AS i, features AS f "
    query_str += "WHERE i.id = f.id "
    query_str += "GROUP BY f.network, i.database_name"
    cur.execute(query_str)
    features_infos = cur.fetchall()
    # print(features_infos)   # [('cifar10', 'mobile_net', 3000)]
    tuples = []
    for i in images_infos:
        found = False
        for f in features_infos:
            if f[0] == i[0]:
                tuples.append((f[1], i[0], i[1], f[2]))
                found = True
        if not found:
            tuples.append(("None", i[0], i[1], "None"))
    __print_table(["network", "database", "database_size", "features_size"], tuples)



def print_db_info(database_name: str):
    '''
    '''
    conn = connect(database_name)
    _print_db_info(conn)
    conn.close()


def _print_db_info(conn: sqlite3.Connection):
    print("Images:")
    print()
    print_info_images(conn)
    print()
    print("Features:")
    print()
    print_info_features(conn)
    conn.close()


def drop_db_from_images():
    '''
    TODO
    '''
    pass


def _get_highest_id(conn: sqlite3.Connection, table_name: str):
    '''
    '''
    cur = conn.cursor()
    query_str = "SELECT MAX(i.id) FROM " + table_name + " AS i"
    cur.execute(query_str)
    result = cur.fetchall()
    id = result[0][0]
    if id == None:
        id = -1
    return id


def _get_image(conn: sqlite3.Connection, id:int):
    '''
    Returns Tuple ("id", "class", "database_name", "website", "data")
    '''
    cur = conn.cursor()
    query_str =  "SELECT i.* "
    query_str += "FROM images AS i "
    query_str += "WHERE i.id = " + str(id)
    cur.execute(query_str)
    result = cur.fetchall()
    return result[0]

def _get_ids_without_feature(conn: sqlite3.Connection, network: str):
    '''
    '''
    cur = conn.cursor()
    sub_query = "SELECT f.id FROM features AS f WHERE f.network = '" + network + "'"
    query_str =  "SELECT i.id, i.data "
    query_str += "FROM images AS i "
    query_str += "WHERE i.id NOT IN (" + sub_query + ")"
    cur.execute(query_str)
    results = cur.fetchall()
    return results


def add_images(conn: sqlite3.Connection, images, img_class: str, img_db_name: str, website: str):
    '''
    '''
    cur = conn.cursor()
    img_tuples = []
    id = _get_highest_id(conn, "images") + 1
    for i in range(0, len(images)):
        img_tuples.append((id, img_class, img_db_name, website, images[i]))
        id += 1

    table = "images"
    query_str = "INSERT INTO " + table + "(id, class, database_name, website, data) "
    query_str += "VALUES (?, ?, ?, ?, ?)"
    cur.executemany(query_str, img_tuples)
    conn.commit()


def _add_features(conn: sqlite3.Connection, ids, network: str, features, hashings):
    '''
    '''
    cur = conn.cursor()
    feature_tuples = []
    for id, feature, hash in zip(ids, features, hashings):
        feature_tuples.append((id, network, feature, hash))

    table = "features"
    query_str =  "INSERT INTO " + table + "(id, network, feature, hashing) "
    query_str += "VALUES (?, ?, ?, ?)"
    cur.executemany(query_str, feature_tuples)
    conn.commit()


def calculate_features(conn: sqlite3.Connection, network: str, feature_function, hash_creating_function, count: int=0):
    '''
    '''
    tuples = _get_ids_without_feature(conn, network)
    ids = []
    images = []
    for t in tuples:
        ids.append(t[0])
        images.append(t[1])

    if count != 0:
        images = images[0:count]

    features = feature_function(images)
    hashes = hash_creating_function(features)
    _add_features(conn, ids, network, features, hashes)


def get_features_for_comparison(conn: sqlite3.Connection, database_name: str, network: str):
    '''
    '''
    # TODO: optimize Query
    cur = conn.cursor()
    query_str =  "SELECT f.id, f.feature "
    query_str += "FROM features AS f, images AS i "
    query_str += "WHERE f.network = '" + network + "' "
    query_str += "AND i.id = f.id "
    query_str += "AND i.database_name = '" + database_name + "'"
    cur.execute(query_str)
    return cur.fetchall()


if __name__ == '__main__':
    create_db("test.db")
    print_db_info("test.db")