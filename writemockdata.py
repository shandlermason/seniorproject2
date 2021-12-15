from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Generated API token, org and bucket
token = "F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w=="
org = "NCAT Senior Project 2"
bucket = "senior project 2"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Mock real-time fields and data at 1 timestamp
    point = Point("mem") \
        .tag("host", "host1") \
        .field("x", 4) \
        .field("y", 2) \
        .field("z", 3) \
        .time(datetime.utcnow(), WritePrecision.NS)

    # Send mock real-time data to InfluxDB
    write_api.write(bucket, org, point)

    # Search for data within bucket and retrieve data
    # Retrieving data written between time 1 hour ago and now
    # Filtering data to only return all x-values between the timeframe
    query = 'from(bucket: "senior project 2") |> range(start: -1h, stop: now()) |> filter(fn:(r) => r._field == "x" )'
    tables = client.query_api().query(query, org=org)

    # Print data retrieved in console
    for table in tables:
        for record in table.records:
            print(record)

    # Have to figure out how to get just the value from the record and put value into variable
#
client.close()
