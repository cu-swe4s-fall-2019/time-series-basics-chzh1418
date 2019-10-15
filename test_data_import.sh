#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_pystyle pycodestyle data_import.py
assert_no_stdout

run test_pystyle pycodestyle test_data_import.py
assert_no_stdout

run folder_not_found python data_import.py --folder_name DATA --output_file out --sort_key hr_small.csv
assert_stdout
assert_exit_code 1

run no_sort_key python data_import.py --folder_name smallData --output_file out --sort_key nothing
assert_stdout
assert_exit_code 1

run basic_test python data_import.py --folder_name smallData --output_file output --sort_key hr_small.csv
assert_exit_code 0

run file_exit python data_import.py --folder_name smallData --output_file output --sort_key hr_small.csv
assert_exit_code 1

rm output_5.csv
rm output_15.csv
