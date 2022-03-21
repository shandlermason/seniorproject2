from influxdb_client import InfluxDBClient


def retrieve_data(token, org, bucket, query):
    # Generated API token, org and bucket - ask Shandler for InfluxDB username and password

    # run InfluxDB on local host
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        query_api = client.query_api()
        # Search for data within SP2 bucket
        result = query_api.query(org=org, query=query)
        # List of each field and its value
        list_of_values = []

        for table in result:
            for record in table.records:
                # flexible, assuming we don't know parameters
                if record.get_field() != '':
                    values = [record.get_field(), record.get_value(), record.get_time()]
                    # add list to running list of values
                    list_of_values.append(values)
        return list_of_values


# currently, comparing numbers of the same timestamp
def compare_data(r_data_c_v, s_data_power):
  # empty dictionary
    freq = {}
    # iterates through real telemetry current and voltage
    for element in r_data_c_v:
        '''Sets the default of the dictionary making the time the key value and the field/value the value. 
        .setdefault() allows for multiple values to have the same key. The purpose of the dictionary is to sort 
        the field/value by there times. Sorting by the time will allows us to sum the current values and 
        voltage values of all 8 solar panels on 1 satellite.'''
        freq.setdefault(element[2], []).append(element[0:2])

    print(freq)

    current = {}
    voltage = {}
    for key in freq.items():
        count = 0
        current_list = []
        voltage_list = []
        for values in freq.values():
            if "_C" in values[count][0]:
                # this works knowing there are 8 solar panels collecting data for the satellite
                current_list.append(values[count][1])
            elif "_V" in values[count][0]:
                k = values[count][0]
                # this works knowing there are 8 solar panels collecting data for the satellite
                voltage_list.append(values[count][1])
            count += 1
            if count == 16:
                current = {key: (sum(current_list)/8)}
                voltage = {key: (sum(voltage_list)/8)}



    '''list_values1 = []
    list_values2 = []
    # list for storing the intensity of the deltas
    deltas = []


    # extracts the value (2nd element) from the tuple and stores it in list
    for x in r_data_c_v:
        if(x[3])
        value1 = x[1]
        list_values1.append(value1)
    
    for y in s_data_power:
        value2 = y[1]
        list_values2.append(value2)

    # finds and stores just deltas in list
    zip_object = zip(list_values1, list_values2)
    for list1_v, list2_v in zip_object:
        deltas.append(list1_v - list2_v)
    '''
    return 0

# Make sure to change query to actual bucket name in InfluxDB


data_set_1 = retrieve_data("F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", "NCAT Senior Project 2", "SP2",
        query = 'from(bucket: "Real_Telemetry_c_v") \
        |> range(start: -10y) \
        |> filter(fn:(r) => r._measurement == "power_real")')
data_set_2 = retrieve_data("F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", "NCAT Senior Project 2", "SP2_2",
        query = 'from(bucket: "Simulated_Telemetry_p") \
        |> range(start: -10y) \
        |> filter(fn:(r) => r._measurement == "power")')
compare_data(data_set_1, data_set_2)








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
