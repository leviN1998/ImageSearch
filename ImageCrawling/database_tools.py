import sqlite3


def _connect_to_db(database_name: str):
	conn = sqlite3.connect(database_name)
	return conn


def _create_table(conn: sqlite3.Connection, table_name, names, types, drop_if_exists: bool=True):
	cur = conn.cursor()
	if drop_if_exists:
		cur.execute("DROP TABLE IF EXISTS " + table_name)
	
	# handle case that table exists
	query_str = "CREATE TABLE " + table_name + " ("
	for n, t in zip(names, types):
		query_str += n + " " + t + ", "
	query_str = query_str[:-2]
	query_str += ")"
	cur.execute(query_str)
	conn.commit()


def _create_images_table(conn: sqlite3.Connection):
	names = ["id", "class", "database_name", "website", "data"]
	types = ["int", "text", "text", "text", "BLOB"]
	_create_table(conn, "images", names, types, drop_if_exists=True)


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
	

def __print_table(col_names, data, max_elements: int=20, max_element_length: int=20):
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

		
def print_info_images(conn: sqlite3.Connection, table_name: str):
	cur = conn.cursor()
	sub_query = table_name
	query_str =  "SELECT t.database_name, t.class, count(t.class) "
	query_str += "FROM " + sub_query + " AS t "
	query_str += "GROUP BY t.database_name, t.class "
	query_str += "ORDER BY t.database_name"
	cur.execute(query_str)
	info_result = cur.fetchall()
	__print_table(["database", "class", "count"], info_result)


def print_info_images_connect(database: str, table_name: str):
	conn = _connect_to_db(database)
	print_info_images(conn, table_name)
	conn.close()


def drop_database_from_images(conn: sqlite3.Connection, table_name: str, database_name: str):
	cur = conn.cursor()
	query_str =  "DELETE FROM " + table_name + " "
	query_str += "WHERE database_name = '" + database_name + "'"
	cur.execute(query_str)
	conn.commit()


def _get_usable_ids(conn: sqlite3.Connection, table_name):
	cur = conn.cursor()
	query_str = "SELECT max(t.id) FROM " + table_name + " AS t"
	cur.execute(query_str)
	max_index = cur.fetchall()[0][0]
	if max_index != None:
		max_index += 1
	else:
		max_index = 0

	ids = []
	query_str =  "SELECT t.id FROM " + table_name + " AS t "
	query_str += "WHERE t.id = "
	for i in range(0, max_index):
		cur.execute(query_str + str(i))
		if len(cur.fetchall()) == 0:
			ids.append(i)
	return max_index, ids


def load_images_to_db(database: str, table: str, images, img_class: str, database_name: str, website: str):
	# TODO: also save features!
	conn = _connect_to_db(database)
	cur = conn.cursor()
	img_tuples = []
	high_id, reusable_ids = _get_usable_ids(conn, table)
	high_id -= 1
	for i in range(0, len(images)):
		id = 0
		if i >= len(reusable_ids):
			id = high_id + 1
		else:
			id = reusable_ids[i]
		img_tuples.append((id, img_class, database_name, website, images[i]))
	
	print("finished creating tuples, start loading into db now")
	query_str =  "INSERT INTO " + table + "(id, class, database_name, website, data) "
	query_str += "VALUES (?, ?, ?, ?, ?)"
	cur.executemany(query_str, img_tuples)
	conn.commit()
	print_info_images(conn, table)
	conn.close()



	


if __name__ == '__main__':
	import crawling_base
	crawling_base._change_folder("ImageDatabases", verbose=True)
	conn = _connect_to_db("test_database")
	# print_table(conn, "images")
	# drop_database_from_images(conn, "images", "cifar_100")
	print_info_images(conn, "images")
	# _get_usable_ids(conn, "images")
	conn.close()