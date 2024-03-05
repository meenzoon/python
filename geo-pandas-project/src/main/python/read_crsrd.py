from string import Template

import pandas as pd
import os

path = '/Users/meenzoon/Downloads/'
csv_file = 'crsrd.csv'
data_file = os.path.join(path, csv_file)
# shp 파일 읽기

df = pd.read_csv(data_file)
print(df)

output_file = os.path.join(path, 'aring.json')
f = open(output_file, 'w')

output2_file = os.path.join(path, 'bring.json')
bring_output_f = open(output2_file, 'w')

crsrd_output_file = os.path.join(path, 'crsrd.json')
crsrd_output_f = open(crsrd_output_file, 'w')

# 기본 geojson 문자열 형태 지정
aringGeoJsonTemplate = Template("""
{"type":"Feature", "longitude": "${longitude}", "latitude": "${latitude}", "aring":{"type":"LineString","coordinates":[[${aring_strt_lon},${aring_strt_lat}],[${aring_mid_lon},${aring_mid_lat}],[${aring_end_lon},${aring_end_lat}]]}, "crt_dt": "${crt_dt}", "crsrd_no": "${crsrd_no}", "crsrd_nm": "${crsrd_nm}", "flmvcr_no": "${flmvcr_no}"}
""")
bringGeoJsonTemplate = Template("""
{"type":"Feature", "longitude": "${longitude}", "latitude": "${latitude}", "bring":{"type":"LineString","coordinates":[[${bring_strt_lon},${bring_strt_lat}],[${bring_mid_lon},${bring_mid_lat}],[${bring_end_lon},${bring_end_lat}]]}, "crt_dt": "${crt_dt}", "crsrd_no": "${crsrd_no}", "crsrd_nm": "${crsrd_nm}", "flmvcr_no": "${flmvcr_no}"}
""")
crsrdGeoJsonTemplate = Template("""
{"type":"Feature", "longitude": "${longitude}", "latitude": "${latitude}", "bring":{"type":"LineString","coordinates":[[${bring_strt_lon},${bring_strt_lat}],[${bring_mid_lon},${bring_mid_lat}],[${bring_end_lon},${bring_end_lat}]]}, "crt_dt": "${crt_dt}", "crsrd_no": "${crsrd_no}", "crsrd_nm": "${crsrd_nm}", "flmvcr_no": "${flmvcr_no}"}
""")

for i in range(0, len(df)):
    row = df.iloc[i]

    data = aringGeoJsonTemplate.substitute(longitude=row['LON'], latitude=row['LAT'], aring_strt_lon=row['ARING_STRT_LON'], aring_strt_lat=row['ARING_STRT_LAT'], aring_mid_lon=row['ARING_MID_LON'], aring_mid_lat=row['ARING_MID_LAT'], aring_end_lon=row['ARING_END_LON'], aring_end_lat=row['ARING_END_LAT'], crt_dt=row['CRT_DT'], crsrd_no=row['CRSRD_NO'], crsrd_nm=row['CRSRD_NM'], flmvcr_no=str(row['ARING_FLMVCR_NO']) + str(row['BRING_FLMVCR_NO']))

    f.write('{"index": {"_index": "aring"}}')
    f.write(data + "\n")

    bring_data = bringGeoJsonTemplate.substitute(longitude=row['LON'], latitude=row['LAT'], bring_strt_lon=row['BRING_STRT_LON'], bring_strt_lat=row['BRING_STRT_LAT'], bring_mid_lon=row['BRING_MID_LON'], bring_mid_lat=row['BRING_MID_LAT'], bring_end_lon=row['BRING_END_LON'], bring_end_lat=row['BRING_END_LAT'], crt_dt=row['CRT_DT'], crsrd_no=row['CRSRD_NO'], crsrd_nm=row['CRSRD_NM'], flmvcr_no=str(row['ARING_FLMVCR_NO']) + str(row['BRING_FLMVCR_NO']))

    bring_output_f.write('{"index": {"_index": "bring"}}')
    bring_output_f.write(bring_data + "\n")