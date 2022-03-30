from influxdb_client import InfluxDBClient
import pandas as pd

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
def organize_data_C_V(r_data_c_v):
    list_of_currents = []
    list_of_voltage = []
    count = 0
    while count < len(r_data_c_v):
        if "_C" in r_data_c_v[count][0]:
            list_of_currents.append(r_data_c_v[count])
        else:
            list_of_voltage.append(r_data_c_v[count])
        count += 1

    # empty dictionaries
    freq_c = {}
    freq_v = {}
    # iterates through real telemetry current and voltage
    for element in list_of_currents:
        '''Sets the default of the dictionary making the time the key value and the field/value the value. 
        .setdefault() allows for multiple values to have the same key. The purpose of the dictionary is to sort 
        the field/value by there times. Sorting by the time will allows us to sum the current values 
        of all 8 solar panels on 1 satellite.'''
        freq_c.setdefault((element[2].strftime("%Y-%m-%d %H:%M:%S")), []).append(element[1])
    for element in list_of_voltage:
        '''Sets the default of the dictionary making the time the key value and the field/value the value. 
        .setdefault() allows for multiple values to have the same key. The purpose of the dictionary is to sort 
        the field/value by there times. Sorting by the time will allows us to sum the current values 
        of all 8 solar panels on 1 satellite.'''
        freq_v.setdefault((element[2].strftime("%Y-%m-%d %H:%M:%S")), []).append(element[1])

    # sum the current values of solar panels 1-8 with the same keys (the same times)
    temp = list(freq_c)
    test_key = temp[0]
    for key, values in freq_c.items():
        # updates the dictionary to have the current of the satellite (all 8 solar panels) at a specific time
        freq_c[key] = (sum(values)/8) # sum all values and divide by 8 to get the average current for satellite at each time
        # goes to the next key in the dictionary
        temp[temp.index(test_key) + 1]

    # sum the voltage values of solar panels 1-8 with the same keys (the same times)
    temp = list(freq_v)
    test_key = temp[0]
    for key, values in freq_v.items():
        # updates the dictionary to have the voltage of the satellite (all 8 solar panels) at a specific time
        freq_v[key] = (sum(values)/8) # sum all values and divide by 8 to get the average voltage for satellite at each time
        # goes to the next key in the dictionary
        temp[temp.index(test_key) + 1]
    return freq_c, freq_v


def organize_power(power_data):
    return 0

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
    # print(interpolated['2018-06-15 02:10'])

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
dict_c, dict_v = organize_data_C_V(data_set_1)
dict_p = organize_power(data_set_2)
analyze_data(dict_c)
analyze_data(dict_v)
analyze_data(dict_p)

