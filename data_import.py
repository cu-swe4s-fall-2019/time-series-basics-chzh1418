import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import time
import sys
import copy
import numpy as np
import math


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
        self._type = 0
        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._type = 0

        elif ('smbg' in data_csv or 'hr' in data_csv or 'cgm' in data_csv or
              'basal' in data_csv):
            self._type = 1

    # open file, create a reader from csv.DictReader,
    # and read input times and values
        with open(data_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['time'] == ''):
                    continue
                else:
                    try:
                        time_add = (dateutil.parser.parse(row['time']))
                        if (row['value'] == 'low'):
                            print('replace low to 40')
                            val = 40
                        elif (row['value'] == 'high'):
                            print('replace high to 300')
                            val = 300

                        else:
                            val = float(row['value'])
                        self._value.append(val)
                        self._time.append(time_add)
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
        low = -1
        high = len(self._time)
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
            print('No value found at key_time')
            hits = -1
        return hits


def roundTimeArray(obj, res):
    """
    Given a time resolution, group times
    Arguments
    --------
    obj: ImportData object
    resolution: integer
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
    round_obj = copy.deepcopy(obj)
    round_lst = []
    values = []
    time_entries = len(round_obj._time)
    for i in range(time_entries):
        tm = round_obj._time[i]
        discard = datetime.timedelta(minutes=tm.minute % res,
                                     seconds=tm.second)
        tm -= discard
        if (discard >= datetime.timedelta(
                minutes=math.ceil(res/2))):
            tm += datetime.timedelta(minutes=res)
        round_obj._time[i] = tm

    if time_entries > 0:
        round_lst.append(round_obj._time[0])
        search_result = round_obj.binary_search_value(round_obj._time[0])
        if (obj._type == 0):
            values.append(sum(search_result))
        elif (obj._type == 1):
            values.append(sum(search_result)/len(search_result))

    for i in range(1, time_entries):
        if round_obj._time[i] == round_obj._time[i - 1]:
            continue
        else:
            round_lst.append(round_obj._time[i])
            search_result = round_obj.binary_search_value(round_obj._time[i])
            if obj._type == 0:
                values.append(sum(search_result))
            elif obj._type == 1:
                values.append(sum(search_result)/len(search_result))

    return zip(round_lst, values)


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
    output = base_name + '.csv'
    if isfile(output):
        raise NameError('File already exist')
        sys.exit(1)
    if key_file not in annotation_list:
        raise ValueError('File not found')
    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                anno_list_a.append(annotation_list[i])
                data_list_a.append(data_list[i])
            else:
                anno_list_b.append(annotation_list[i])
                # data_list_b.append(data_list[i])

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
    parser = argparse.ArgumentParser(description='A class to import,' +
                                     'combine, and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder')

    parser.add_argument('--output_file', type=str, help='Name of Output file')

    parser.add_argument('--sort_key', type=str, help='File to sort on')

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
