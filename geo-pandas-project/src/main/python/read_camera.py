from string import Template

import pandas as pd
import os

path = '/Users/meenzoon/Downloads/'
csv_file = 'jinju.csv'
data_file = os.path.join(path, csv_file)
# shp 파일 읽기

cameraDf = pd.read_csv(data_file)
print(cameraDf)

output_file = os.path.join(path, 'camera.json')
f = open(output_file, 'w')

# 기본 geojson 문자열 형태 지정
geoJsonTemplate = Template("""
{"type":"Feature","geometry":{"type":"Point","coordinates":[${longitude},${latitude}]}, "id": "${id}", "name": "${name}"}
""")
for i in range(0, len(cameraDf)):
    row = cameraDf.iloc[i]

    data = geoJsonTemplate.substitute(longitude=row['longitude'], latitude=row['latitude'], name=row['name'], id=row['id'])

    f.write('{"index": {"_index": "camera"}}')
    f.write(data + "\n")