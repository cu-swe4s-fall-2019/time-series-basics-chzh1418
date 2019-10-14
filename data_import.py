import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import time
import sys
import math


class ImportData:
    def __init__(self, data_csv):
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
                time = (datatime.datetime.strptime(
                    row['time'], '%m/%d/%y %H:%M'))

                try:
                    if (row['value'] == 'low'):
                        print('replace low to 40')
                        row['value'] = 40
                    elif(row['value'] == 'high'):
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

    def linear_search_value(self, key_time):
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

    def binary_search_value(self, key_time):
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
    time_list = []
    values = []
    num_times = len(obj._time)

    for i in range(num_times):
        time = obj._time[i]
        bad_time = datetime.timedelta(minutes=time.minute % res,
                                      seconds=time.second)
        time -= bad_time
        if (bad_time >= datetime.timedelta(minutes=math.ceil(res/2))):
            time += datetime.timedelta(minutes=res)
        obj._time[i] = time

    if num_times > 0:
        time_list.append(obj._time[0])
        search_results = obj.linear_search_value(obj._time[0])
        # summaiton
        if type == 0:
            values.append(sum(search))
        # Average
        elif type == 1:
            values.append(sum(search)/len(search))

    for i in range(1, num_times):
        if obj._time[i] == obj._time[i - 1]:
            continue
        else:
            time_list.append(obj._time[i])
            search = obj.linear_search_value(obj._time[i])
            if type == 0:
                values.append(sum(search))
            elif type == 1:
                values.append(sum(search)/len(search))
    output = zip(time_list, values)
    return output


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    data_list_a = []
    data_list_b = []
    anno_list_a = []
    anno_list_b = []
    output = base_name + '.csv'
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
        writer.writerow(zipper)
        for (time1, value1) in data_list_a[0]:
            list1 = []
            for data in data_list_b:
                list1_len = len(list1)
                for (time2, value2) in data:
                    if (time1 == time2):
                        list1.append(value2)
                if(len(list1) == list1_len):
                    list1.append(0)
            writer.writeow([time1, value1] + list1)



if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('output_file', type=str, help = 'Name of Output file')

    parser.add_argument('sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()


    #pull all the folders in the file
    files_lst = # list the folders


    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min

    #print to a csv file
    printLargeArray(data_5,files_lst,args.output_file+'_5',args.sort_key)
    printLargeArray(data_15, files_lst,args.output_file+'_15',args.sort_key)
