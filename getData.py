from influxdb_client import InfluxDBClient

def retrieve_data(token, org, bucket):
    # Generated API token, org and bucket - ask Shandler for InfluxDB username and password

    # run InfluxDB on local host
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        query_api = client.query_api()

        # Search for data within SP2 bucket
        query = 'from(bucket: "SP2") \
        |> range(start: -10y) \
        |> filter(fn:(r) => r._measurement == "power")'
        result = query_api.query(org=org, query=query)

        # List of each field and its value
        list_of_values = []

        for table in result:
            for record in table.records:
                # flexible, assuming we don't know parameters
                if record.get_field() != '':
                    field_name = (record.get_field(), record.get_value())
                    # add tuple to running list of values
                    list_of_values.append(field_name)
        return list_of_values

data_set_1 = retrieve_data("F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", "NCAT Senior Project 2", "SP2")

data_set_2 = retrieve_data("F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", "NCAT Senior Project 2", "SP2")









#functionally be able to grab from one data set and compare to another data set
#two data sets, compare numbers of particular timestamp
#paste data into two different buckets
#dont change numbers there should be no deltas, if make changes to numbers then deltas should be showing up
#comparing real data and simulated data
'''
def twin_model(soc, bm, deploy):
    twin_soc = 0
    twin_bm = 0
    twin_deploy = 0
    index = 400
    # What is the purpose of the list of deltas - we do not have to answer this question
    # Just provide Aerospace deltas between telemetry and intensity of each delta
    # give aerospace which parameters have deltas and how big they are
    # output format for delta list - which parameter and time stamp and what delta actually is
    #look at powerpoint sent from Alex

    #figure out using equation current and voltage (simulated) to create simulated Power to compare to real Power
    #process telemetry to have simulated power

    #some timesteps wont match, different data sets will have different timestep sizes
    #if you need timestamp 6
    #if you know 4 and you know 8 then you can make an estimate of what 6 is

    #dont need requirements 5 and 6 on proposal
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
    #print('list of deltas: ', list_delta_soc)


b_state_of_charge, pg_body_mounted, pg_deploy = retrieve_data()
'''
# tests to make sure the data is being retrieved and put into list
'''
print('batter soc list: ', b_state_of_charge)
print('power generated body mounted list: ', pg_body_mounted)
print('power generated deploy list: ', pg_deploy)
'''
'''
twin_model(b_state_of_charge, pg_body_mounted, pg_deploy)
'''
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
