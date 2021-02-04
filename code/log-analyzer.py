#!/bin/env python
# coding=utf-8

from datetime import datetime
import sys
import re
import pandas as pd
import os

# To avoid long lines in the output xls file, we defined the maximum number of characters per error line to be reported
MAXIMUM_CHARACTERS_PER_LINE = 3000

# (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d*) *([A-Z]*)( *\[.*?\] * (.*?) \- *(.*)| *([A-Z]*)  \- \[.*\] *(.*))
# Regular expression that maps the logs
# The following expression checks for text such as:
# 2017-05-16 07:38:18,679 ERROR [WebContainer : 33] com.nm.services.DocumentFolderGeneratorServiceImpl - BlaBlaBla
# 2017-05-16 00:00:00,001 INFO  - [SchedulerThread-1-5] jobToBeExecuted: Maintenance. BlaBlaBla
# The regular expression has to be adapted to handle different log files
regular_expression = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d*) *([A-Z]*) *\[.*?\] * (.*?) \- *(.*)|(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d*) *([A-Z]*) \- \[.*\] *(.*)"

# compile the regular expression
expression = re.compile(regular_expression)


def create_data_frame():
    """
    Create a Pandas data frame, to easily work with the logs
    :return: Pandas data frame
    """
    return pd.DataFrame(columns=('Timestamp', 'Error', 'Class', 'Error-Message'))


def export_date_frame_to_excel(data_frames_dict, xls_file_name):
    """
    Exports Pandas data frames to a xls file
    :param data_frames_dict: dictionary type, where keys are data frame name and value is the data frame to be exported
    :param xls_file_name: name of the xls file
    """
    excel_writer = pd.ExcelWriter(xls_file_name, encoding='utf-8')
    # for error, data_frame in data_frames_dict.iteritems():
    for error, data_frame in data_frames_dict.items():
        data_frame.to_excel(excel_writer, error)
    excel_writer.save()


def is_date(str_value):
    """
    Check if the string is a timestamp or not
    :param str_value: String
    :return: boolean
    """
    try:
        datetime.strptime(str_value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_found_errors(data_frame):
    """
    Get unique list of errors in a data frame
    :param data_frame: pandas data frame
    :return: unique list of errors
    """
    return data_frame.Error.unique()


def group_errors(data_frame, column_name='Error'):
    """
    Group errors, create a data frame for each error
    :param data_frame: data frame
    :param column_name: column name
    :return: dict, where keys are the errors and values are data frame that has this error
    """
    error_data_frames = {}
    errors = get_found_errors(data_frame)
    for error in errors:
        error_data_frames[error] = data_frame.loc[data_frame[column_name] == error]
    return error_data_frames


def path_check(path):
    """
    create a path if it does not exist
    :param path: string
    """
    if not os.path.exists(path):
        os.makedirs(path)


def parse_file(file_name, output_path):
    """
    Parse input file
    :param file_name: input file name
    :param output_path: output file name
    """
    data_frame = create_data_frame()
    # dict, that records how many times each error message appeared
    errors_statistics = {}
    # open the file
    with open(file_name) as f:
        previous_data = {}
        previous_index = 0
        # iterate over the file lines
        for index, line in enumerate(f, 1):
            print(line)
            line_space_split = line.split()
            if len(line_space_split) <= 0:
                continue
            # if line starts with a timestamp, it means it a new log, else it belongs to the previous log message
            if is_date(line_space_split[0]):
                # apply the reg expression
                values = expression.search(line)
                if values is None:
                    continue
                values_group = values.groups()
                # check in which group is the message
                if values.lastindex == 7:
                    timestamp = values_group[4]
                    error_type = values_group[5]
                    error = values_group[6]
                    klass = ''
                else:
                    timestamp = values_group[0]
                    error_type = values_group[1]
                    klass = values_group[2]
                    error = values_group[3]

                new_data = {
                    'Timestamp': timestamp,
                    'Error': error_type,
                    'Class': klass,
                    'Error-Message': error[:MAXIMUM_CHARACTERS_PER_LINE] + '..' if len(
                        error) > MAXIMUM_CHARACTERS_PER_LINE else error
                }
                previous_data = new_data
                previous_index = index
                data_frame.loc[index] = new_data
                if klass not in errors_statistics.keys():
                    errors_statistics[klass] = {}

                if error_type not in errors_statistics[klass].keys():
                    errors_statistics[klass][error_type] = 1
                else:
                    errors_statistics[klass][error_type] += 1
            else:
                # Ignore all deep JAVA errors such as
                # at com.nm.exprlang.functions.MethodCallFunction.calculate(MethodCallFunction.java:88)
                if not line.startswith('	at '):
                    # check the number of characters in an error message and ignore
                    # if it is more than MAXIMUM_CHARACTERS_BER_LINE
                    if previous_data.get('Error-Message', None) is not None and len(
                            previous_data['Error-Message']) < MAXIMUM_CHARACTERS_PER_LINE:
                        previous_data['Error-Message'] = "{0} {1}".format(previous_data['Error-Message'],
                                                                          line[:MAXIMUM_CHARACTERS_PER_LINE])
                    data_frame.loc[previous_index] = previous_data

    # group the errors
    data_frames = group_errors(data_frame)
    # create a statistics data frame
    data_frames['Statistics'] = pd.DataFrame.from_dict(errors_statistics, orient='index')
    # Remove all of the actual messages from the dictionary
    # Large logs will blow up excel due to the 65k row limit
    # We only want to keep the Statistics
    data_frames.pop('ERROR', None)
    data_frames.pop('WARN', None)
    data_frames.pop('INFO', None)
    data_frames.pop('DEBUG', None)

    # export data frames to xls
    path_check(output_path)
    output_file_path = os.path.join(output_path, os.path.basename(file_name))
    export_date_frame_to_excel(data_frames, '{0}.xls'.format(output_file_path))


def main(args):
    if len(args) < 3:
        print("Please enter the log files path and the output path")
        exit(-1)
    print(args)
    path = args[1]
    output_path = args[2]
    # iterate over the files in the a directory
    for filename in os.listdir(path):
        # catch only files that ends with .log
        if filename.endswith('.log'):
            file_path = os.path.join(path, filename)
            print('processing file {0}'.format(filename))
            # parse the file
            parse_file(file_path, output_path)


if __name__ == '__main__':
    print("Start Parser >>>>>>> ")
    main(sys.argv)
