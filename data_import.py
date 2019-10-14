import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import time
import sys
import math
import copy
import numpy as np


class ImportData:
    """Read data_csv file and modify low and high values

    Attributes:
        _time: times column in data_csv file
        _value: values column in data_csv file
        _type: different types for duplicates, sum and average
    """
    def __init__(self, data_csv):
        """Initialize ImportData object and read in data_csv file"""
        self._time = []
        self._value = []
        self._file = data_csv
        self._type = 0
        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._type = 0

        elif ('smbg' in data_csv or 'hr' in data_csv or 'cgm' in data_csv or
              'basal' in data_csv):
            self._type = 1

        else:
            self._type == -1
            print("Don't know average or sum!")
            sys.exit(1)

    # open file, create a reader from csv.DictReader,
    # and read input times and values
        with open(data_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['time'] == ''):
                    continue
                time = (dateutil.parser.parse(row['time']))
                try:
                    if (row['value'] == 'low'):
                        print('replace low to 40')
                        row['value'] = 40
                    elif (row['value'] == 'high'):
                        print('replace high to 300')
                        row['value'] == 300

                    value = float(row['value'])
                    if (not math.isnan(value)):
                        self._value.append(value)
                        self._time.append(time)
                except ValueError:
                    print('Check value: ' + row['value'])

        # Check the order of time
        if (len(self._time) > 0):
            if (self._time[-1] < self._time[0]):
                self._time.reverse()
                self._value.reverse()
            csvfile.close()

    def linear_search_value(self, key_time):
        """
        Linear search of key_time
        Arguments
        --------
        key_time: time to search for

        Return
        -------
        hits: index of matched time
        -1: No value found
        """
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        hits = []
        for i in range(len(self._time)):
            if self._time[i] == key_time:
                hits.append(self._value[i])

        if (len(hits) == 0):
            print('Not value found at key_time')
            return -1
        return hits

    def binary_sort(self):
        times = self._time.copy()
        values = self._value.copy()
        zipped = zip(times, values)
        zipped_sort = sorted(zipped)

        times_tup, values_tup = zip(*zipped_sort)
        times_sorted = list(times_tup)
        values_sorted = list(values_tup)
        self._time = times_sorted
        self._value = values_sorted
        return

    def binary_search_value(self, key_time):
        """
        Binary search of key_time

        Arguments
        -------
        key_time: time to search for

        Returns
        -------
        hits: index of matched tiime
        -1: No hits found
        """
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        hits = []
        low = 0
        high = len(self._time) - 1
        middle = -1
        while (high - low > 1):
            middle = (high + low) // 2
            if (self._time[middle] == key_time):
                break
            elif (self._time[middle] < key_time):
                low = middle + 1
            else:
                high = middle - 1
        hits.append(self._value[middle])

        if (len(hits) == 0):
            print('Not value found at key_time')
            return -1

        return hits


def roundTimeArray(obj, res):
    """
    Given a time resolution, group times
    Arguments
    --------
    obj: ImportData object
    res: integer
         minute resolution of time
    Returns
    --------
    Zipped object of grouped times and values
    """
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    time_rounded_obj = copy.deepcopy(obj)
    rounded_times = []
    unique_rounded_times = []

    for time in time_rounded_obj._time:
        minminus = datetime.timedelta(minutes=(time.minute % res))
        minplus = datetime.timedelta(minutes=res) - minminus
        if (time.minute % res) <= (res/2):
            newtime = time - minminus
            if newtime not in rounded_times:
                unique_rounded_times.append(newtime)
            rounded_times.append(newtime)
        else:
            newtime = time + minplus
            if newtime not in rounded_times:
                unique_rounded_times.append(newtime)
            rounded_times.append(newtime)

    time_rounded_obj._time = rounded_times

    sorted_values = [[] for i in range(len(unique_rounded_times))]

    # Linear search
    rounded_values = obj._value

    for unique_idx in range(len(unique_rounded_times)):
        value_idx = None
        time_rounded_obj._time = rounded_times
        time_rounded_obj._value = rounded_values

        while value_idx != -1 and len(time_rounded_obj._value) > 0:
            if value_idx is not None:
                value = time_rounded_obj._value.pop(value_idx)
                sorted_values[unique_idx].append(value)
                time_rounded_obj._time.pop(value_idx)
            value_idx = time_rounded_obj.linear_search_value(
                        unique_rounded_times[unique_idx])

    # Binary search
    # Sort the object
    time_rounded_obj.binary_sort()
    sorted_rounded_times = time_rounded_obj._time
    sorted_rounded_values = time_rounded_obj._value

    for unique_idx in range(len(unique_rounded_times)):
        value_idx = None
        time_rounded_obj._time = sorted_rounded_times
        time_rounded_obj._value = sorted_rounded_values

        while value_idx != 1:
            if value_idx is not None:
                value = time_rounded_obj._value.pop(value_idx)
                sorted_values[unique_idx].append(value)
                time_rounded_obj._time.pop(value_idx)
            value_idx = time_rounded_obj.binary_search_value(
                        uique_rounded_times[unique_idx])

    output = []
    if time_rounded_obj._type == 1:
        for idx in range(len(sorted_values)):
            output.append(np.mean(sorted_values[idx]))
    if time_rounded_obj._type == 0:
        for idx in range(len(sorted_values)):
            output.append(np.sum(sorted_values[idx]))

    return zip(unique_rounded_times, output)


def printArray(data_list, annotation_list, base_name, key_file):
    """
    Print array to file
    Arguments
    --------
    data_list: list of data to import
    annotation_list: list of column titles
    base_name: basename of saved name
    key_file: the first column of the written csv file

    Returns
    --------
    """
    data_list_a = []
    data_list_b = []
    anno_list_a = []
    anno_list_b = []
    if isfile(output):
        raise NameError('File already exist')
    if key_file not in annotation_list:
        raise ValueError('File not found')
    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                anno_list_a.append(annotation_list[i])
                data_list_a.append(data_list[i])
            else:
                anno_list_b.append(annotation_list[i])
                data_list_b.append(data_list[i])

    attributes = ['time', key_file] + anno_list_b
    with open(base_name + '.csv', mode='w') as output:
        writer = csv.writer(output, delimiter=',')
        writer.writerow(attributes)
        for (time1, value1) in data_list_a[0]:
            left_values = []
            for data in data_list_b:
                left_values_len = len(left_values)
                for (time2, value2) in data:
                    if (time1 == time2):
                        left_values.append(value2)
                if(len(left_values) == left_values_len):
                    left_values.append(0)
            writer.writerow([time1, value1] + left_values)


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import,
                                     combine, and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str, help='Name of the folder')

    parser.add_argument('output_file', type=str, help='Name of Output file')

    parser.add_argument('sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()
    folder_path = args.folder_name
    output = args.output_file
    sorter = args.sort_key
    # pull all the folders in the file
    try:
        files_lst = [f for f in listdir(folder_path) if f.endswith('.csv')]
    except (FileNotFoundError, NameError):
        print('File not found')
        sys.exit(1)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for file in files_lst:
        data_lst.append(ImportData(folder_path + '/' + file))

    if (len(data_lst) == 0):
        print('Data not found')
        sys.exit(1)
    print(data_lst)

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    for data in data_lst:
        data_5.append(roundTimeArray(data, 5))
    data_15 = []  # a list with time rounded to 15min
    for data in data_lst:
        data_15.append(roundTimeArray(data, 15))

    # print to a csv file
    print_5 = printArray(data_5, files_lst,
                         args.output_file+'_5', args.sort_key)
    print_15 = printArray(data_15, files_lst,
                          args.output_file+'_15', args.sort_key)
