import pymysql

conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = "root",
    password = "dkssud123!",
    database = "hairshop"
)
cursor = conn.cursor()

result = cursor.execute("SELECT * FROM Shop")
print(result)