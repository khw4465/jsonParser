import pymysql

conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = "root",
    password = "dkssud123!",
    database = "hairshop"
)
cursor = conn.cursor()

cursor.execute("SELECT * FROM Shop")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()