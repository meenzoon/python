from string import Template

import pandas as pd
import os
from datetime import datetime, timezone, timedelta

path = os.path.expanduser('~/tools/osm/')
csv_file = 'dtg_input_10m.csv'
data_file = os.path.join(path, csv_file)

df = pd.read_csv(data_file, delimiter='|', header=None)
print(df)

point_output_file_path = os.path.join(path, 'output_point.geojson')
point_output_file = open(point_output_file_path, 'w')
point_output_file.write('{"type": "FeatureCollection","features": [')

barefoot_output_file_path = os.path.join(path, 'input_barefoot.geojson')
barefoot_output_file = open(barefoot_output_file_path, 'w')
barefoot_output_file.write("[")

hopper_output_file_path = os.path.join(path, 'input_hopper.gpx')
hopper_output_file = open(hopper_output_file_path, 'w')
hopper_output_file.write('''<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" version="1.0" 
xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" 
creator="gpx.py -- https://github.com/tkrajina/gpxpy">
  <trk>
    <name/>
    <type/>
    <desc/>
    <trkseg>''' + "\n")

# 기본 geojson 문자열 형태 지정
point_template = Template('{"type": "Feature","properties": {"time": "${dateTime}"},"geometry": {"coordinates": [${longitude},${latitude}],"type": "Point"}}')
barefoot_template = Template('{"point":"POINT(${longitude} ${latitude})","time":"${dateTime}","id":"${carRegNo}"}')
hopper_template = Template('      <trkpt lat="${latitude}" lon="${longitude}"><time>${dateTime}</time></trkpt>')
for i in range(0, len(df)):
    row = df.iloc[i]

    dateTimeStr = str(row[4])
    dateTime_without_time = datetime(int(dateTimeStr[0:4]), int(dateTimeStr[4:6]), int(dateTimeStr[6:8]),
                                     int(dateTimeStr[8:10]), int(dateTimeStr[10:12]), int(dateTimeStr[12:14]),
                                     tzinfo=timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S%z")
    dateTime_with_time = datetime(int(dateTimeStr[0:4]), int(dateTimeStr[4:6]), int(dateTimeStr[6:8]),
                                  int(dateTimeStr[8:10]), int(dateTimeStr[10:12]), int(dateTimeStr[12:14]),
                                  tzinfo=timezone(timedelta(hours=9))).strftime("%Y-%m-%dT%H:%M:%S%z")

    point_str = point_template.substitute(dateTime=dateTime_without_time, longitude=row[8], latitude=row[9])
    barefoot_str = barefoot_template.substitute(dateTime=dateTime_without_time, longitude=row[8], latitude=row[9],
                                                carRegNo=row[1])
    hopper_str = hopper_template.substitute(dateTime=dateTime_with_time, longitude=row[8], latitude=row[9])

    point_output_file.write(point_str)
    barefoot_output_file.write(barefoot_str)
    if i != len(df) - 1:
        point_output_file.write(",")
        barefoot_output_file.write(",")
    hopper_output_file.write(hopper_str + "\n")


point_output_file.write(']}')
barefoot_output_file.write("]")
hopper_output_file.write('''    </trkseg>
  </trk>
</gpx>''')
