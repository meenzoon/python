from string import Template

import pandas as pd
from shapely import wkt
from geojson import Feature, LineString, dump

# 기본 geojson 문자열 형태 지정
geoJsonTemplate = Template("""
{"type":"Feature","geometry":{"type":"LineString","coordinates":[[${lon1},${lat1}],[${lon2},${lat2}]]},"name": "${name}"
}
""")

# json 파일 읽기
df = pd.read_json('nodelink.json')

# print(df)

f = open('out.json', 'w')

for i in range(0, len(df)):
    row = df.iloc[i]
    geom = wkt.loads(row['geom'])
    coords = geom.coords

    lineStr = LineString([(coords[0][0], coords[0][1]), (coords[1][0], coords[1][1])])
    feat = Feature(geometry=lineStr, properties={"id": row['id'], "link_id": row['link_id'], "degree": row['drc_val']})

    # geojson 데이터 작성
    '''
    data = geoJsonTemplate.substitute(lon1=coords[0][0], lat1=coords[0][1], lon2=coords[1][0], lat2=coords[1][1],
                                      name=row['link_id'])
    '''

    f.write('{"index": {"_index": "link"}}')
    dump(feat, f)

f.close()
