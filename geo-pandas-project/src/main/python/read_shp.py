from string import Template

import geopandas as gpd
import os
from geojson import Feature, dump
from shapely import Polygon, intersects

path = '/Users/meenzoon/Downloads/'
sig_file = 'sig_20230729/sig.shp'
shp_file = os.path.join(path, sig_file)
# shp 파일 읽기
sgg = gpd.read_file(shp_file)
# shp 파일 기본 좌표계 정보 저장
sgg.crs = {'init': 'epsg:5179'}

output_file = os.path.join(path, 'sip.json')
f = open(output_file, 'w')
# 파일 좌표계 변경
jinju_sig = sgg[sgg['SIG_CD'] == '48170'].to_crs(epsg=4326)

polygon = Polygon(((127.86837, 35.35689), (127.86837, 35.04432), (128.38336, 35.04432), (128.38336, 35.35689), (127.86837, 35.35689)))

for i in range(0, len(jinju_sig)):
    row = jinju_sig.iloc[i]
    geom = row['geometry']

    intersects(polygon, geom)

    feat = Feature(geometry=row['geometry'], properties={"SIG_CD": row[0]})

    f.write('{"index": {"_index": "sip"}}' + '\n')
    dump(feat, f)
