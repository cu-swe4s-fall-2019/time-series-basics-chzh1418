# time-series-basics
Time Series basics - importing, cleaning, printing to csv

*Note date files are synthetic data. ## Modify .yaml file for continuous integration
## Modify .yml file for continuous integration
## Install
To use this package, you need to install python3 and the following python packages:

* os
* sys
* csv
* dateutil.parser
* argparse
* datetime
* time
* copy
* numpy
* math
* pycodestyle
* unittest
Pycodestyle is used to test code style
ssshtest is used for functional test
## Usage
`data_import.py` is the script used to generate integrated csv file.
It is used in the following manner:
`python data_import.py --folder_name smallData --output_file out --sort_key hr_small.csv`
--folder_name is the folder contains csv files
--output_file is the name of output file
--sort_key is the file used to sort data

### ImportData class
ImportData takes a csv file that contains time and value columns.

**Functions**
linear_search_value: linearly search and return the value corresponding to datetime.
binary_search_value: binary search and then return the value corresponding to datetime.

### roundTimeArray(obj,res)
* Inputs : ImportData object and resolution
* Action: Create a time array with the time rounded to the nearest resolution miniutes
	  No duplicates
	  Activity, Bolus, Meal values are summed
	  Smbg, Hr, Cgm, Basal values are averaged

### printArray(data_list, annotation_list, base_name, key_file)
* Inputs : data_list a list of zip objects of data(time, value) paires
	   annotation_list a list of strings with column labels for data value
	   base_name the file name to print
	   key_file the name from annotation_list to align the data on 
* Action : Creat a csv file while aligns the data in the list of zip objects base on the key_file
* Returns : a csv file named base_name.csv

### Benchmarking
* Benchmark time to test the binary and linear search speed

	Time took for linear search
	* data_5: 4.842226028442383
	* data_15: 1.9132914543151855

	Time took for binary search
	* data_5: 0.322634220123291
	* data_15: 0.3005979061126709

## Unittes and functional test
* Added test_data_import.py for unit test.
`python test_data_import.py`
* Added test_data_import.sh for functional test.
`bash test_data_import.sh`



