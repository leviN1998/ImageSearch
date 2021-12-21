import sqlite3

conn = sqlite3.connect('test_database') 
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS images")
c.execute("CREATE TABLE images (id int, feature int, class text)")

img_list = [
	(0, 111, 'test'),
	(1, 111, 'test'),
	(2, 111, 'test')
]

c.executemany("INSERT INTO images VALUES (?, ?, ?)", img_list)

c.execute("SELECT i.* FROM images AS i")
print(c.fetchall())

conn.commit()