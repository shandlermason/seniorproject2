from influxdb_client import InfluxDBClient

# Generated API token, org and bucket
token = "F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w=="
org = "NCAT Senior Project 2"
bucket = "SP2"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    query_api = client.query_api()
    # Search for data within bucket and retrieve data
    # Retrieving data written between time 1 hour ago and now
    # Filtering data to only return all x-values between the timeframe
    query = 'from(bucket: "SP2") \
    |> range(start: -10y) \
    |> filter(fn:(r) => r._measurement == "power")'
    result = query_api.query(org=org, query=query)

    # Print data retrieved in console
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    print(results)
    # Have to figure out how to get just the value from the record and put value into variable
#
#client.close()


'''
battery_soc = (most recent data pulled from influx) 100 (figure out how to read record by record in a loop that way 
                it'll constantly keep updating)
twin_battery_soc = 0
delta = battery_soc-twin_battery_soc

while not False (while true basically):
    if(delta < 0.1)
        twin_battery_soc = battery_soc
        break (or change to false to break while loop)
        (check email sent by Tim for logic)
    
'''