from pyproj import Proj, Transformer, transform
import pymysql
import json
import time

WGS84 = { 'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84', }

GRS80 = { 'proj':'tmerc', 'lat_0':'38', 'lon_0':'127', 'k':1, 'x_0':200000,
    'y_0':600000, 'ellps':'GRS80', 'units':'m' }

# def grs80_to_wgs84(x, y):
#     transformer = Transformer.from_proj(GRS80, "EPSG:4326", always_xy=True)
#     return transformer.transform(x, y)

def grs80_to_wgs84(x, y):
    in_proj = Proj(init = 'epsg:5186')
    out_proj = Proj(init = 'epsg:4326')
    wgs84_x, wgs84_y = transform(in_proj, out_proj, x, y)
    return wgs84_x, wgs84_y

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

# 시작 시간 기록
start_time = time.time()

try:
    with open('/Users/khw4465/openapi.json', encoding='utf-8') as f:
        json_data = json.load(f)

        batch_size = 1000
        total_rows = len(json_data['DATA'])
        batch_count = (total_rows + batch_size -1) // batch_size

        for i in range(batch_count):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, total_rows)

            batch_data = json_data['DATA'][start_idx:end_idx]

            row = []
            for data in batch_data:
                shopName = data.get('bplcnm', '')
                x = data.get('x', '')
                y = data.get('y', '')

                if x and y:
                    wgs84_x, wgs84_y = grs80_to_wgs84(float(x), float(y))
                    row.append((shopName, wgs84_x, wgs84_y))


            # sql = "INSERT INTO MyAround (shopName, x, y) VALUES (%s, %s, %s)"
            # cursor.executemany(sql, row)
            # print("insert완료")

            print(row)

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

# 종료 시간 기록
end_time = time.time()

# 총 처리 시간 계산
total_time = end_time - start_time
print("총 처리 시간:", total_time, "초")