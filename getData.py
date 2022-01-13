import pandas as pd
from influxdb_client import InfluxDBClient
import csv

client = InfluxDBClient(url="http://localhost:8086", token="F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", org="NCAT Senior Project 2")

file_path = r'C:/Users/Owner/Desktop/writeCSV.csv'

import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(file_path):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open('C:/Users/Owner/Desktop/writeCSV.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            print(rows)

            data[key] = rows
    # Open a json writer, and use the json.dumps()
    # function to dump data
    #with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:

        #print(json.dumps(data, indent=4))

# Call the make_json function
make_json('C:/Users/Owner/Desktop/writeCSV.csv')







'''
csvReader = pd.read_csv(file_path)

print(csvReader.shape)
print(csvReader.columns)

for row_index, row in csvReader.iterrows() :
    group = row[1]
    datatype=row[2]
    default=row[3]
    #fieldvalue = row[2]
    json_body = [
        {
            "measurement": "Measurement_name",
            "tags": {
                        "Tag_name1": tags
                    },
            "fields": {
                        "table": row[2],
                        "Field2": row[3],
                        "Field3": row[4]
                        }
        }
    ]
    client.write_api().write('senior project 2', 'NCAT Senior Project 2', json_body)





'''







'''
with open('C:/Users/Owner/Desktop/writeCSV.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        print(line)
'''
'''
client = InfluxDBClient(url="http://localhost:8086", token="F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", org="NCAT Senior Project 2")
write_client = client.write_api()

df = pd.read_csv("~/Desktop/writeCSV.csv")
#df['_time'] = pd.to_datetime(df['_time'], format="%Y-%m-%dT%H:%M:%SZ")
#df.set_index(['_time'])
print(df)
write_client.write("SENIOR PROJECT", "NCAT Senior Project 2", record=df, data_frame_measurement_name="_measurement",
                   data_frame_tag_columns=['region', 'host'])

query = 'from(bucket: "SENIOR PROJECT") |> range(start: -1h, stop: now())'
tables = client.query_api().query(query, org="NCAT Senior Project 2")

# Print data retrieved in console
for table in tables:
    for record in table.records:
        print(record)
'''
'''from influxdb_client import InfluxDBClient, Point, WritePrecision
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
    query = 'from(bucket: "senior project 2") |> range(start: -1h, stop: now())'
    tables = client.query_api().query(query, org=org)

    # Print data retrieved in console
    for table in tables:
        for record in table.records:
            print(record)

    # Have to figure out how to get just the value from the record and put value into variable
#
client.close()
'''