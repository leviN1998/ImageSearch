from pyexpat import features
import sqlite3
from PIL import Image
import io
from tensorflow import keras
import numpy as np


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


def get_highest_id(conn: sqlite3.Connection, table_name):
	cur = conn.cursor()
	query_str = "SELECT MAX(i.id) FROM " + table_name + " AS i"
	cur.execute(query_str)
	result = cur.fetchall()
	id = result[0][0]
	if id == None:
		id = -1
	return id


def load_images_to_db(database: str, table: str, images, img_class: str, database_name: str, website: str):
	# TODO: also save features!
	#!!!!!!!!!!!!!!!!!!!!!!!!! 
	# TODO: FIX IDS
	# Schleife zählt nicht richtig hoch
	conn = _connect_to_db(database)
	cur = conn.cursor()
	img_tuples = []
	id = get_highest_id(conn, table) + 1
	for i in range(0, len(images)):
		img_tuples.append((id, img_class, database_name, website, images[i]))
		id += 1
	
	print("finished creating tuples, start loading into db now")
	query_str =  "INSERT INTO " + table + "(id, class, database_name, website, data) "
	query_str += "VALUES (?, ?, ?, ?, ?)"
	cur.executemany(query_str, img_tuples)
	conn.commit()
	print_info_images(conn, table)
	conn.close()


def _get_ids_without_feature(conn: sqlite3.Connection, network: str):
	cur = conn.cursor()
	sub_query = "SELECT f.id FROM features AS f WHERE f.network = '" + network + "'"
	query_str =  "SELECT i.id, i.data "
	query_str += "FROM images AS i "
	query_str += "WHERE i.id NOT IN (" + sub_query + ")"
	cur.execute(query_str)
	results = cur.fetchall()
	return results


def __add_features_to_db(conn: sqlite3.Connection, table: str, network: str, ids, images, feature_function, hash_creation_function):
	cur = conn.cursor()
	feature_tuples = []
	features = feature_function(images)
	hashes = hash_creation_function(images)
	for id, feature, hash in zip(ids, features, hashes):
		feature_tuples.append((id, network, feature, hash))
	query_str =  "INSERT INTO " + table + "(id, network, feature, hashing) "
	query_str += "VALUES (?, ?, ?, ?)"
	cur.executemany(query_str, feature_tuples)
	conn.commit()
	conn.close()


def add_features_to_db(database: str, network: str, feature_function, hash_creation_function):
	conn = _connect_to_db(database)
	tuples = _get_ids_without_feature(conn, network)
	ids = []
	images = []
	for t in tuples:
		ids.append(t[0])
		images.append(t[1])

	# DEBUG
	# ids = [ids[0]]
	# images = [images[0]]

	__add_features_to_db(conn, "features", network, ids, images, feature_function, hash_creation_function)


def create_feature_table(conn: sqlite3.Connection):
	names = ["id", "network", "feature", "hashing"]
	types = ["int", "text", "BLOB", "BLOB"]
	_create_table(conn, "features", names, types, drop_if_exists=True)

# Init MobileNet
keras.applications.mobilenet.MobileNet()

mobile = keras.applications.mobilenet.MobileNet(
    input_shape=None,
    alpha=1.0,
    depth_multiplier=1,
    dropout=0.001,
    include_top=False,
    weights="imagenet",
    input_tensor=None,
    pooling="avg",
    classifier_activation="softmax",
)


def __dummy_prepare_image(image_data):
	image = Image.open(io.BytesIO(image_data)).convert("RGB")
	image = image.resize((224, 224))
	# image.show()
	img_array = keras.preprocessing.image.img_to_array(image)
	img_array_expanded_dims = np.expand_dims(img_array, axis=0)
	# print(np.shape(img_array))
	# print(np.shape(img_array_expanded_dims))
	return keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)


def __dummy_ectract_image(image_data):
	preprocessed_image = __dummy_prepare_image(image_data)
	feature = mobile.predict(preprocessed_image)[0]
	feature = feature / np.linalg.norm(feature)
	buf = io.BytesIO()
	np.save(buf, feature)
	return buf.getvalue()


def __dummy_feature_func(images):
	print("Extracting Features! This might take some time")
	count = 0
	features = []
	for image in images:
		feature = __dummy_ectract_image(image)
		features.append(feature)
		if count % 100 == 0:
			print("Extracted Features " + str(count) + "/" + str(len(images)))
		count += 1
	print("Finished extracting Features! Starting to save them into table")
	return features


def __dummy_hashing_func(images):
	hashes = []
	for image in images:
		hashes.append(bin(255))
	return hashes


def __dummy_get_test_image():
	conn = _connect_to_db("light_database.db")
	cur = conn.cursor()
	query_str =  "SELECT i.id, f.feature, i.data "
	query_str += "FROM images AS i, features AS f "
	query_str += "WHERE i.database_name = 'cifar10_test' "
	query_str += "AND i.id = f.id "
	query_str += "AND f.network = 'mobileNet'"
	cur.execute(query_str)
	image = cur.fetchall()[0]
	conn.close()
	return image


def _get_features_for_database(conn: sqlite3.Connection, database_name: str, network: str):
	# TODO: optimize Query
	cur = conn.cursor()
	query_str =  "SELECT f.id, f.feature "
	query_str += "FROM features AS f, images AS i "
	query_str += "WHERE f.network = '" + network + "' "
	query_str += "AND i.id = f.id "
	query_str += "AND i.database_name = '" + database_name + "'"
	cur.execute(query_str)
	return cur.fetchall()


def calculate_distance(feature1, feature2):
	return np.linalg.norm(feature1 - feature2)


def _insert_ordered(list, element):
	if len(list) == 0:
		list.append(element)
		return
	else:
		for i in range(0, len(list)):
			if list[i][1] > element[1]:
				list.insert(i, element)
				return
				

def get_image_from_id(conn: sqlite3.Connection, id):
	cur = conn.cursor()
	query_str =  "SELECT i.data "
	query_str += "FROM images AS i "
	query_str += "WHERE i.id = " + str(id)
	cur.execute(query_str)
	result = cur.fetchall()
	return Image.open(io.BytesIO(result[0][0])).convert("RGB").resize((500, 500))


def get_nearest_images(database: str, image_feature, database_name: str, network: str, count: int=10):
	conn = _connect_to_db(database)
	features = _get_features_for_database(conn, database_name, network)
	closest_images = []
	for f in features:
		# print(len(closest_images))
		# create numpy array
		feature = np.load(io.BytesIO(f[1]))
		distance = calculate_distance(image_feature, feature)
		if len(closest_images) < count:
			_insert_ordered(closest_images, (f[0], distance))
		elif distance < closest_images[-1][1]:
			_insert_ordered(closest_images, (f[0], distance))
			closest_images.pop()
	output = []
	for i in closest_images:
		output.append((get_image_from_id(conn, i[0]), i[1]))
	conn.close()
	return output
	


def debug_og():
	img = keras.preprocessing.image.load_img("cifar10_80/airplane0.jpg", target_size=(224,224))
	img_array = keras.preprocessing.image.img_to_array(img)
	img_array_expanded_dims = np.expand_dims(img_array, axis=0)
	print(np.shape(img_array))
	print(np.shape(img_array_expanded_dims))
	preprocessed_image = keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)
	feature = mobile.predict(preprocessed_image)[0]
	# print(np.shape(feature))
	feature_finished = feature / np.linalg.norm(feature)
	# print(feature_finished)


# restore Numpy Feature Array:
# print(np.load(io.BytesIO(feature)))


if __name__ == '__main__':
	import crawling_base
	crawling_base._change_folder("ImageDatabases", verbose=True)
	# conn = _connect_to_db("light_database.db")
	# print_info_images(conn, "images")
	# create_feature_table(conn)
	
	# debug_og()
	# add_features_to_db("light_database.db", "mobileNet", __dummy_feature_func, __dummy_hashing_func)

	# print_table(conn, "features")

	
	# conn.close()

	image = __dummy_get_test_image()
	Image.open(io.BytesIO(image[2])).convert("RGB").resize((500, 500)).show()
	feature = np.load(io.BytesIO(image[1]))

	images = get_nearest_images("light_database.db", feature, "cifar10", "mobileNet", count=10)
	for i in images:
		i[0].show()