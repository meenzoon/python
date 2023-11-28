import geopandas as gpd
import os
from geojson import Feature, dump
from shapely import Polygon, intersects

path = '/Users/meenzoon/Downloads/'
link_file = 'nodelink/nodelink.shp'
shp_file = os.path.join(path, link_file)
# shp 파일 읽기
link = gpd.read_file(shp_file, encoding='CP949')

highway_output_file = os.path.join(path, 'highway.json')
highway_f = open(highway_output_file, 'w')

road_output_file = os.path.join(path, 'road.json')
road_f = open(road_output_file, 'w')

# overlap
polygon = Polygon(((127.86837, 35.35689), (127.86837, 35.04432), (128.38336, 35.04432), (128.38336, 35.35689), (127.86837, 35.35689)))

count = 0
for i in range(0, len(link)):
    row = link.iloc[i]
    road_rank = row['ROAD_RANK']
    geom = row['geometry']
    if intersects(polygon, geom):
        count += 1
        feat = Feature(geometry=row['geometry'],
                       properties={"LINK_ID": row['LINK_ID'], "F_NODE": row['F_NODE'], "T_NODE": row['T_NODE'],
                                   "LANES": int(row['LANES']), "ROAD_RANK": row['ROAD_RANK'],
                                   "ROAD_TYPE": row['ROAD_TYPE'], "ROAD_NO": row['ROAD_NO'],
                                   "MULTI_LINK": row['MULTI_LINK'], "CONNECT": row['CONNECT'],
                                   "MAX_SPD": int(row['MAX_SPD']), "REST_VEH": row['REST_VEH']})

        if road_rank == '101' or road_rank == '102':
            # 고속도로
            highway_f.write('{"index": {"_index": "highway"}}' + '\n')
            dump(feat, highway_f)
            highway_f.write("\n")
            highway_f.write("\n")
        else:
            # 일반도로
            road_f.write('{"index": {"_index": "road"}}' + '\n')
            dump(feat, road_f)
            road_f.write("\n")
            road_f.write("\n")


print(count)