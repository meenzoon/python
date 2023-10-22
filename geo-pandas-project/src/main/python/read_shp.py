import geopandas as gpd
import pandas as pd
import os

path = '/Users/meenzoon/Downloads/'
file = 'sig_20230729/sig.shp'
shp_file = os.path.join(path, file)
# shp 파일 읽기
sgg = gpd.read_file(shp_file)
# shp 파일 기본 좌표계 정보 저장
sgg.crs = {'init': 'epsg:5179'}

print(sgg.crs)
# 파일 좌표계 변경
sgg = sgg.to_crs(epsg=4326)

print(sgg)