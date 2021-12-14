import json

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Generated API token, org and bucket
token = "F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w=="
org = "NCAT Senior Project 2"
bucket = "senior project 2"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    #Send mock data to database
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("mem") \
        .tag("host", "host1") \
        .field("x", 1) \
        .field("y", 2) \
        .time(datetime.utcnow(), WritePrecision.NS)
    point2 = Point("mem2") \
        .tag("host", "host1") \
        .field("x", 3) \
        .field("y", 4)\
        .time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(bucket, org, point)
    write_api.write(bucket, org, point2)

    #Search for data within bucket and retrieve data
    query = 'from(bucket: "senior project 2") |> range(start: -1m)'
    tables = client.query_api().query(query, org=org)

    #Print data retrieved in consol
    for table in tables:
        for record in table.records:
            print(record)
#
client.close()