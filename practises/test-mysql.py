import mysql.connector as connector

dbconfig = {
    'user': 'stock',
    'password': 'abcd@123',
    'host': '10.211.55.9',
    'database': 'stock'
}

connection = connector.connect(**dbconfig)

cursor = connection.cursor()

cursor.execute('select * from tbl_StockList limit 1')

for d in cursor:
    print d

connection.close()
