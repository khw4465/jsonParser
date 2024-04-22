import pymysql
import json

# secretes.json 파일에서 정보를 읽어옴
with open('secretes.json') as f:
    secrets = json.load(f)

DB_HOST = secrets["DB_HOST"]
DB_PORT = int(secrets["DB_PORT"])
DB_USER = secrets["DB_USER"]
DB_PASS = secrets["DB_PASS"]
DATABASE = secrets["DATABASE"]

conn = pymysql.connect(
    host = DB_HOST,
    port = DB_PORT,
    user = DB_USER,
    password = DB_PASS,
    database = DATABASE
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM Shop")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()