from string import Template

import pandas as pd
import os

path = '/Users/meenzoon/Downloads/'
csv_file = 'smart_intersection.csv'
data_file = os.path.join(path, csv_file)
# shp 파일 읽기

df = pd.read_csv(data_file)
print(df)

output_file = os.path.join(path, 'smart_intersection.json')
f = open(output_file, 'w')

# 기본 geojson 문자열 형태 지정
geoJsonTemplate = Template("""
{"type":"Feature","geometry":{"type":"Point","coordinates":[${longitude},${latitude}]}, "fclts_id": "${fclts_id}", "fclts_nm": "${fclts_nm}", "system_fclts_id": "${system_fclts_id}", "addr": "${addr}"}
""")
for i in range(0, len(df)):
    row = df.iloc[i]

    data = geoJsonTemplate.substitute(longitude=row['longitude'], latitude=row['latitude'], fclts_nm=row['fclts_nm']
                                      , fclts_id=row['fclts_id'], system_fclts_id=row['system_fclts_id'], addr=row['addr'],)

    f.write('{"index": {"_index": "smart_intersection"}}')
    f.write(data + "\n")