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

        else:
            print("주소 변환 실패로 인해 데이터를 스킵합니다.")