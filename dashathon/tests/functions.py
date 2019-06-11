import numpy as np
import pandas as pd
import time
import datetime


def converttime(t):
    """
    Converting time to seconds
    :param t: time in HH:MM:SS format
    :return: time returned as total seconds
    """
    t = str(t)
    x = time.strptime(t, '%H:%M:%S')
    return int(datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,
                                  seconds=x.tm_sec).total_seconds())


def pipe_reader(link):
    """
    Read datasets without pandas read_csv when we have a pipe delimiter dataset
    with commas inside columns
    :param link: The local address link of the pipe delimited .CSV file to read
    :return: The pipe delimited file as a dataframe
    """
    with open(link, 'r') as f:
        temp_file = f.read()
    temp_file = temp_file.split('\n')
    lis = []
    for row in temp_file:
        row = row.split('|')
        if len(row) == 20:
            lis.append(row)
    temp_df = pd.DataFrame(lis, columns=lis[0])
    temp_df = temp_df.drop(0, axis=0)
    return temp_df
