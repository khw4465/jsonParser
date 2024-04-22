import json

with open('/Users/khw4465/openapi.json', encoding='utf-8') as f:
    json_data = json.load(f)

    for data in json_data['DATA']:
        shopName = data.get('bplcnm', '')
        x = data.get('x', '')
        y = data.get('y', '')