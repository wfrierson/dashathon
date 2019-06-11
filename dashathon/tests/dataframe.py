import pandas as pd
from functions import converttime
from functions import pipe_reader


def converttime_checker(time_var):
    """Checks if time conversion works well or not"""
    is_correct_time = True

    if (converttime(time_var)) != 86399:
        is_correct_time = False
    return is_correct_time


def pipe_reader_checker(link):
    """Checks if it is able to read CSV files with pipe delimiters on basis of
    no. of rows and columns"""
    is_correct_read = True

    if (pipe_reader(link).shape) != (22824, 20):
        is_correct_read = False
    return is_correct_read
