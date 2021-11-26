import sqlite3
import pandas as pd
conn = sqlite3.connect('test_database') 
c = conn.cursor()

conn = sqlite3.connect('test_database') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS products
          ([product_id] INTEGER PRIMARY KEY, [product_link] TEXT)
          ''')
          
c.execute('''
          CREATE TABLE IF NOT EXISTS vectors
          ([product_id] INTEGER PRIMARY KEY, [vector] INTEGER)
          ''')
          
c.execute('''
          INSERT INTO products (product_id, product_link)

                VALUES
                (1,'Computer'),
                (2,'Printer'),
                (3,'Tablet'),
                (4,'Desk'),
                (5,'Chair')
          ''')

c.execute('''
          INSERT INTO vectors (product_id, vector)

                VALUES
                (1,800),
                (2,200),
                (3,300),
                (4,450),
                (5,150)
          ''')
          
conn.commit()


c.execute('''
          SELECT
          a.product_link,
          b.vector
          FROM products a
          LEFT JOIN vectors b ON a.product_id = b.product_id
          ''')

df = pd.DataFrame(c.fetchall(), columns=['product_link','vector'])
print (df)