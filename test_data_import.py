import unittest
import os
import datetime
import data_import
import random
import statistics
from os.path import join

class Test_Math_Lib(unittest.TestCase):
    def test_import_data(self):
        file = './smallData/activity_small.csv'
        input = data_import.ImportData(file)
        self.assertEqual(len(input._time), len(input._value))

    def test_linear_search(self):
        file = './smallData/activity_small.csv'
        input = data_import.ImportData(file)
        test_data = datetime.datetime(2018, 3, 12, 0, 11)
        self.assertEqual(input.linear_search_value(test_data), [3])

    def test_linear_search_false(self):
        file = './smallData/activity_small.csv'
        input = data_import.ImportData(file)
        test_data = datetime.datetime(2019, 3, 12, 0, 11)
        self.assertEqual(input.linear_search_value(test_data), -1)
    
    def test_binary_search(self):
        file = './smallData/activity_small.csv'
        input = data_import.ImportData(file)
        input.binary_sort()
        test_data = datetime.datetime(2018, 3, 12, 0, 11)
        self.assertEqual(input.binary_search_value(test_data), [3])

    def test_binary_search_false(self):
        file = './smallData/activity_small.csv'
        input = data_import.ImportData(file)
        input.binary_sort()
        test_data = datetime.datetime(2018, 3, 12, 0, 11)
        self.assertNotEqual(input.binary_search_value(test_data), [-1])

    def test_import(self):
        filename = './smallData/cgm_small.csv'
        with open(filename, 'rt') as input_file:
            with open('out.csv', 'wt') as output_file:
                for line in input_file:
                    line = line.replace('40', 'low')
                    line = line.replace('300', 'high')
                    output_file.write(line)
            output_file.close()
        input_file.close()
        obj = data_import.ImportData('out.csv')
        self.assertEqual(len(obj._time), len(obj._value))
        os.remove('out.csv')

    def test_low_high_replace(self):
        f = open('test1.csv', 'w')
        f.write('time,value\n')
        f.write('3/15/19 1:00,low\n')
        f.write('3/16/19 2:00,high')
        f.close()
        obj = data_import.ImportData('test1.csv')
        self.assertEqual(obj._value[0], 40)
        self.assertEqual(obj._value[1], 300)
        os.remove('test1.csv')

    def test_round_time(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        rounded = data_import.roundTimeArray(obj, 5)
        for (time, value) in rounded:
            self.assertEqual(value, 254.0)
            d = datetime.datetime(2018, 3, 16, 8, 45)
            self.assertEqual(time, d)
            break

    def test_print_array(self):
        files_lst = os.listdir('./smallData/')
        data_lst = []
        for f in files_lst:
            data_lst.append(data_import.ImportData(join('./smallData/', f)))

        data_5 = []
        for obj in data_lst:
            data_5.append(data_import.roundTimeArray(obj, 5))

        r = data_import.printArray(data_5, files_lst, 'out_5',
                                   'smbg_small.csv')
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')
if __name__ == '__main__':
    unittest.main()



