import sqlite3
import pandas as pd


conn = sqlite3.connect('test_database2') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS products
          ([product_id] INTEGER PRIMARY KEY, [product_link] TEXT)
          ''')
          
c.execute('''
          CREATE TABLE IF NOT EXISTS vectors
          ([product_id] INTEGER PRIMARY KEY, [vector] ARRAY)
          ''')
          
c.execute('''
          CREATE TABLE IF NOT EXISTS widths
          ([product_id] INTEGER PRIMARY KEY, [width] INTEGER)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS heights
          ([product_id] INTEGER PRIMARY KEY, [height] INTEGER)
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
                (1,'[1,2,3,4,5,6,7,8,9,10,11,12,13]'),
                (2,'[1,2,3,4,5,6,7,8,9,10,11,12,13]'),
                (3,'[1,2,3,4,5,6,7,8,9,10,11,12,13]'),
                (4,'[1,2,3,4,5,6,7,8,9,10,11,12,13]'),
                (5,'[1,2,3,4,5,6,7,8,9,10,11,12,20]')
          ''')

c.execute('''
          INSERT INTO widths (product_id, width)

                VALUES
                (1,256),
                (2,1920),
                (3,12),
                (4,28),
                (5,150)
          ''')
          
c.execute('''
          INSERT INTO heights (product_id, height)

                VALUES
                (1,256),
                (2,1920),
                (3,12),
                (4,28),
                (5,150)
          ''')
          
conn.commit()
conn.close()

