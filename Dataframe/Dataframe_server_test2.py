import sqlite3
import pandas as pd
conn = sqlite3.connect('test_database2') 
c = conn.cursor()
c.execute('''
          SELECT
          a.product_link,
          b.vector,
          c.width,
          d.height
          FROM products a
          LEFT JOIN vectors b ON a.product_id = b.product_id
          LEFT JOIN widths c ON b.product_id = c.product_id
          LEFT JOIN heights d ON c.product_id = d.product_id
          ''')

df = pd.DataFrame(c.fetchall(), columns=['product_link','vector','width','height'])
#print (df)

print(df.at[0,'product_link'])

print(df.at[0,'vector'])

if df.at[0,'product_link'] == 'Computer':
    print('Die Sonne')
    
print(df.last_valid_index())

#a = df.last_valid_index()
i = 0
while i < 5 :
    if df.at[i,'product_link'] == 'Chair':
        print('ist ein Stern')
    i += 1