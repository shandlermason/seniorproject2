from influxdb_client import InfluxDBClient
import pandas as pd
from numpy import mean

def retrieve_data(token, org, bucket, query):
    # Generated API token, org and bucket - ask Shandler for InfluxDB username and password
    # run InfluxDB on local host
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        query_api = client.query_api()
        # Search for data within SP2 bucket
        result = query_api.query(org=org, query=query)
        # List of each field and its value
        list_of_values = []
        # list_of_units = []

        for table in result:
            for record in table.records:
                # flexible, assuming we don't know parameters
                if record.get_field() != '':
                    values = [record.get_field(), record.get_value(), record.get_time()]
                    # add list to running list of values
                    list_of_values.append(values)
        return list_of_values


# organizing current, voltage values
def separating_c_and_v(data_c_v):
    list_of_currents = []
    list_of_voltage = []
    count = 0
    while count < len(data_c_v):
        if "_C" in data_c_v[count][0]:
            list_of_currents.append(data_c_v[count])
        else:
            list_of_voltage.append(data_c_v[count])
        count += 1

    return list_of_currents, list_of_voltage


def organize_power(power_data):
    p_mounted = []
    p_deployed = []
    count = 0
    # sorts through power_body_mounted and power_generated_deployed
    while count < len(power_data):
        if "_mounted" in power_data[count][0]:
            p_mounted.append(power_data[count])
        elif "_deployed" in power_data[count][0]:
            p_deployed.append(power_data[count])
        count += 1

    power_list = p_mounted + p_deployed

    # empty dictionary
    freq = {}
    # iterates through real telemetry current and voltage and simulated power
    for element in power_list:
        '''Sets the default of the dictionary making the time the key value and the field/value the value. 
        .setdefault() allows for multiple values to have the same key. The purpose of the dictionary is to sort 
        the field/value by there times. Sorting by the time will allows us to sum the power values 
        of all 8 solar panels on 1 satellite.'''
        freq.setdefault((element[2].strftime("%Y-%m-%d %H:%M:%S")), []).append(element[1])

    # sum the current values of solar panels 1-8 with the same keys (the same times)
    temp = list(freq)
    test_key = temp[0]
    for key, values in freq.items():
        # updates the dictionary to have the current of the satellite (all 8 solar panels) at a specific time
        freq[key] = max(values)  # max value between mounted and deployed at each time
        # goes to the next key in the dictionary
        temp[temp.index(test_key) + 1]

    return freq


# f
def organize_data(data_list):

    # empty dictionary
    freq = {}
    # iterates through real telemetry current and voltage and simulated power
    for element in data_list:
        '''Sets the default of the dictionary making the time the key value and the field/value the value. 
        .setdefault() allows for multiple values to have the same key. The purpose of the dictionary is to sort 
        the field/value by there times. Sorting by the time will allows us to sum the current/voltage values 
        of all 8 solar panels on 1 satellite.'''
        freq.setdefault((element[2].strftime("%Y-%m-%d %H:%M:%S")), []).append(element[1])

    # sum the current values of solar panels 1-8 with the same keys (the same times)
    temp = list(freq)
    test_key = temp[0]
    for key, values in freq.items():
        # updates the dictionary to have the current of the satellite (all 8 solar panels) at a specific time
        freq[key] = mean(values)  # sum all values and divide by 8 to get the average current for satellite at each time
        # goes to the next key in the dictionary
        temp[temp.index(test_key) + 1]

    return freq


# creates timestamp values for every 10 seconds and fills in with estimated values
def analyze_data(vals):
    vals_df = pd.DataFrame(vals.items(), columns=['Timestamp', 'Value'])
    vals_df['New_Timestamp'] = pd.to_datetime(vals_df['Timestamp'].astype(str), format= '%Y%m%d %H:%M:%S')
    '''Upsample the series into 10 S bins and average the values of the timestamps falling into a bin. 
    The dataset has been upsampled with nan values for the remaining times except for those times which were 
    originally available in our dataset.'''
    upsampled = vals_df.set_index('New_Timestamp').resample('10S').mean()
    '''This draws a cubic plot between available data, in this case on the last of the month, and fills in values
    at the chosen frequency from this line.'''
    interpolated = upsampled.interpolate(method='cubic')

    # testing to see if the value makes sense/is correct
    # print(interpolated.loc['2018-06-15 02:16'])

    return interpolated


# Make sure to change query to actual information in InfluxDB
data_set_1 = retrieve_data("F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", "NCAT Senior Project 2", "SP2",
        query = 'from(bucket: "Real_Telemetry_c_v") \
        |> range(start: -10y) \
        |> filter(fn:(r) => r._measurement == "power_real")')
data_set_2 = retrieve_data("F9Mc-Unn4MGPfZIHb18W2a2FFOraMQzbqt_oQjZxlH79No3_v0kKETqnt0Cjmprzl9-VT5EtXjAr8e3Ce3w78w==", "NCAT Senior Project 2", "SP2_2",
        query = 'from(bucket: "Simulated_Telemetry_p") \
        |> range(start: -10y) \
        |> filter(fn:(r) => r._measurement == "power")')
c_list, v_list = separating_c_and_v(data_set_1)

dict_p = organize_power(data_set_2)
dict_c = organize_data(c_list)
dict_v = organize_data(v_list)

inter_1 = analyze_data(dict_c)
inter_2 = analyze_data(dict_v)
inter_3 = analyze_data(dict_p)
