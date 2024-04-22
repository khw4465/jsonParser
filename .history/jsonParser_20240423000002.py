import pymysql
import json
from geopy.geocoders import Nominatim

def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    try:
        geo = geolocoder.geocode(address)
        if geo is None:
            print("주소를 찾을 수 없습니다:", address)
            return
        crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
        return crd
    except Exception as e:
        print("주소 변환 중 오류가 발생했습니다:", e)
        return

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

try:
    with open('/Users/khw4465/openapi.json', encoding='utf-8') as f:
        json_data = json.load(f)

        for data in json_data['DATA']:
            shopName = data.get('bplcnm', '')
            if not shopName:
                print("매장 이름이 없는 데이터를 스킵합니다.")
                continue

            address = data.get('rdnwhladdr', '')
            if not address:
                print("주소 정보가 없는 데이터를 스킵합니다.")
                continue

            a = address.split(' ')
            address = " ".join(a[0:4])
            if ',' in address[-1]:
                address = address[:-1]
            crd = geocoding(address)

            if crd is not None:
                x = crd['lat']
                y = crd['lng']

                sql = "INSERT INTO MyAround (shopName, x, y) VALUES (%s, %s, %s)"
                cursor.execute(sql, (shopName, x, y))
            else:
                print("주소 변환 실패로 인해 데이터를 스킵합니다.")

    # 변경사항 커밋
    conn.commit()
    print("데이터가 성공적으로 삽입되었습니다.")

except Exception as e:
    # 예외 발생 시 롤백
    conn.rollback()
    print("데이터 삽입 중 오류가 발생하였습니다:", e)

finally:
    # 연결 종료
    conn.close()
