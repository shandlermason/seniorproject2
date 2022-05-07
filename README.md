# Team 6 - The Aerospace Team Senior Project 2
Team Members: Shandler Mason, Timothy Bass, Brandez Tronshaw

Advisor: Dr. Kelvin Bryant
## Product Installation/Set-Up Instructions
1. Download and install InfluxDB for specific operating system 
2. Using your command prompt start/run InfluxDB on local host using command. 

https://docs.influxdata.com/influxdb/v2.1/install/?t=Windows\

3. Fill in token, org, bucket, query for method using appropriate credentials. <pre><code>def retrieve_data()</code> </pre> 
4. You should now be able to retrieve data from InfluxDB


## Product User's Manual
Current code runs using Shandler's credentials 
### Methods:
Retrieve field, value, and timestamp from InfluxDB buckets
<pre><code>def retrieve_data(token, org, bucket, query)</code></pre>

Seperates/organizes current and voltage values 
<pre><code>def separating_c_and_v(data_c_v)</code></pre>

Sorts through 2 different power fields. Determines max value between power body mounted and power deployed at each time. Itierates through real telemetry current and voltage and simulated power. Sum the current and voltage values of solar panels 1-8 with the ame times.
<pre><code>def organize_power(power_data)</code></pre>

Creates timestamp values for every 10 seconds and fills in with estimated values.
<pre><code>def analyze_data(vals)</code></pre>

Find deltas by taking the absolute value of (power - (current*voltage)). Outputs graph of Deltas vs. Timestamp and CSV file.
<pre><code>def find_deltas(current, voltage, power)</code></pre>

Creates graphs for Current, Volatage, Power vs. Time
<pre><code>def create_output_c(data)</code></pre>
<pre><code>def create_output_c(data)</code></pre>
<pre><code>def create_output_c(data)</code></pre>
