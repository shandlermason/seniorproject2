from influxdb_client import InfluxDBClient


def retrieve_data():
    # Generated API token, org and bucket - ask Shandler for InfluxDB username and password
    token = "F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w=="
    org = "NCAT Senior Project 2"
    bucket = "SP2"

    # run InfluxDB on local host
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        query_api = client.query_api()

        # Search for data within SP2 bucket
        query = 'from(bucket: "SP2") \
        |> range(start: -10y) \
        |> filter(fn:(r) => r._measurement == "power")'
        result = query_api.query(org=org, query=query)

        # Creates a list of data for each field
        battery_soc_list = []
        pg_body_mounted_list = []
        pg_deployed = []
        for table in result:
            for record in table.records:
                if record.get_field() == "battery_state_of_charge":
                    battery_soc_list.append(record.get_value())
                elif record.get_field() == "power_generated_body_mounted":
                    pg_body_mounted_list.append(record.get_value())
                elif record.get_field() == "power_generated_deployed":
                    pg_deployed.append(record.get_value())

        # test to check if values are appending to specific list
        print('batter state of charge list # 1: ', battery_soc_list)
        return battery_soc_list, pg_body_mounted_list, pg_deployed


def twin_model(soc, bm, deploy):
    twin_soc = 0
    twin_bm = 0
    twin_deploy = 0
    index = 400
    # What is the purpose of the list of deltas
    list_delta_soc = []

    while index <= len(soc)-1:
        # test to check values in variables
        num1 = soc[index]
        num2 = twin_soc

        delta_soc = soc[index] - twin_soc
        if abs(delta_soc) > 0.001:
            twin_soc = soc[index]
            list_delta_soc.append(delta_soc)
        index += 1

    # test to make sure delta values are calculating and appending to list
    # Need to figure out how to disregard first delta because it is skewed (100 - 0 = 100 for delta)
    print('list of deltas: ', list_delta_soc)


b_state_of_charge, pg_body_mounted, pg_deploy = retrieve_data()
'''
# tests to make sure the data is being retrieved and put into list
print('batter soc list: ', b_state_of_charge)
print('power generated body mounted list: ', pg_body_mounted)
print('power generated deploy list: ', pg_deploy)
'''
twin_model(b_state_of_charge, pg_body_mounted, pg_deploy)

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
