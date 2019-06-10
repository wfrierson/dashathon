import pandas as pd
import numpy as np


def convert_time(time_minutes):
    """
    Convert time expressed in (float) minutes into (float) seconds.

    :param float time_minutes: Time expressed in minutes.
    :return: Time expressed in seconds.
    :rtype: float
    """
    time_seconds = time_minutes * 60
    return time_seconds


def transform_llimllib_boston_data(df, year):
    """
    Transform 2013-2104 Boston Marathon data into a standard form for downstream processing.

    :param pandas.DataFrame df: DataFrame representing 2013-2014 Boston Marathon data from llimllib's Github repo.
    :param int year: Year of Boston Marathon
    :return: DataFrame of transformed marathon data
    :rtype: pandas.DataFrame
    """

    headers_split = ['5k', '10k', '20k', 'half', '25k', '30k', '35k', '40k', 'official']

    # Replace nan placeholders with actual nan values
    for header in headers_split:
        df[header].replace('-', np.nan, inplace=True)

    # Cast split times to float
    dtypes_new = dict(zip(headers_split, [float] * len(headers_split)))
    df = df.astype(dtypes_new)

    # Convert split time from decimal minutes to seconds
    for header in headers_split + ['pace']:
        df[header] = df[header].apply(convert_time)

    # Add year field
    df['year'] = year

    # Add empty columns for 15k split time and gender_place rank
    df['15k'] = np.nan
    df['gender_place'] = np.nan

    df = df.rename(columns={'official': 'official_time', 'ctz': 'citizen'})

    return df


# at least one row in 2015 had an incomprehensible official finish time: 0.124548611111111
# I believe there was only one, but the try/catch below should handle
# missing values, placeholder '-', and bad values
def get_sec(time_str):
    """
    Convert time in a string format 'HH:MM:SS' into (int) seconds.

    :param time_str: Time in a string format 'HH:MM:SS'
    :return: Time expressed in seconds
    :rtype: int
    """
    try:
        hours_str, minutes_str, seconds_str = time_str.split(':')
        return int(hours_str) * 3600 + int(minutes_str) * 60 + int(seconds_str)
    except:
        return np.nan


def transform_rojour_boston_data(df, year):
    """

    :param pandas.DataFrame df:
    :param year:
    :return:
    :rtype: pandas.DataFrame
    """
    # Drop unnecessary columns
    if year == 2016:
        df.drop('Proj Time', axis=1)
    else:
        df.drop([df.columns[0], 'Proj Time'], axis=1)

    # The split times in the Kaggle data are formatted as strings hh:mm:ss. We want these times in total seconds.
    headers_split = ['5K', '10K', '15K', '20K', 'Half', '25K', '30K', '35K', '40K', 'Official Time']
    for header in headers_split:
        df[header] = df[header].apply(get_sec)

    if year == 2015:
        df.dropna(subset=['Official Time'])

    # Create a year field and an empty field for 'genderdiv'
    df['year'] = year
    df['genderdiv'] = np.nan

    headers_map = {'Age': 'age', 'Official Time': 'official_time', 'Bib': 'bib', 'Citizen': 'citizen',
                   'Overall': 'overall', 'Pace': 'pace', 'State': 'state', 'Country': 'country', 'City': 'city',
                   'Name': 'name', 'Division': 'division', 'M/F': 'gender', '5K': '5k', '10K': '10k', '15K': '15k',
                   '20K': '20k', 'Half': 'half', '25K': '25k', '30K': '30k', '35K': '35k', '40K': '40k',
                   'Gender': 'gender_place'}

    if year == 2016:
        headers_map.update({'Unnamed: 8': 'para_status'})
    else:
        headers_map.update({'Unnamed: 9': 'para_status'})

    df = df.rename(columns=headers_map)

    # as discussed, this section is dropping all runners with a para status
    # then dropping those cols as they will be empty
    df = df[df.para_status != 'MI']
    df = df[df.para_status != 'VI']
    df = df.drop('para_status', axis=1)

    return df


# NOTE: The age brackets on the BAA website are as follows:
# 14-19*, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54,
# 55-59, 60-64, 65-70, 70-74, 75-79, and 80
# This places 70 into two brackets! I have assumed a typo and followed the pattern
# I have also ignored the minimum age in case it has not been the same in every year
def bin_ages(age):
    """

    :param age:
    :return:
    """
    try:
        if age <= 19:
            bid = 1
            bstr = '<= 19'
        elif age <= 24:
            bid = 2
            bstr = '20-24'
        elif age <= 29:
            bid = 3
            bstr = '25-29'
        elif age <= 34:
            bid = 4
            bstr = '30-34'
        elif age <= 39:
            bid = 5
            bstr = '35-39'
        elif age <= 44:
            bid = 6
            bstr = '40-44'
        elif age <= 49:
            bid = 7
            bstr = '45-49'
        elif age <= 54:
            bid = 8
            bstr = '50-54'
        elif age <= 59:
            bid = 9
            bstr = '55-59'
        elif age <= 64:
            bid = 10
            bstr = '60-64'
        elif age <= 69:
            bid = 11
            bstr = '65-69'
        elif age <= 74:
            bid = 12
            bstr = '70-74'
        elif age <= 79:
            bid = 13
            bstr = '75-79'
        else:
            bid = 14
            bstr = '80+'
        return bid, bstr
    except:
        bid = np.nan
        bstr = np.nan
        return bid, bstr


# use the above function to make two new cols, as described
def apply_and_concat(df, val, func, col_names):
    """

    :param pandas.DataFrame df:
    :param val:
    :param func:
    :param col_names:
    :return:
    :rtype: pandas.DataFrame
    """
    return pd.concat((
        df,
        df[val].apply(
            lambda cell: pd.Series(func(cell), index=col_names))), axis=1)


def combine_boston_data(list_dfs):
    """

    :param list[pandas.DataFrame] list_dfs:
    :return:
    :rtype: pandas.DataFrame
    """
    df_combine = pd.concat(list_dfs, sort=True)
    df_combine = apply_and_concat(df_combine, 'age', bin_ages, ['age_bucket', 'age_range'])

    return df_combine


# Read in data
llimllib_boston_results_2013 = pd.read_csv('./data/external_data/llimllib_boston_results_2013.csv', delimiter=',')
llimllib_boston_results_2014 = pd.read_csv('./data/external_data/llimllib_boston_results_2014.csv', delimiter=',')
rojour_boston_results_2015 = pd.read_csv('./data/external_data/rojour_boston_results_2015.csv', delimiter=',')
rojour_boston_results_2016 = pd.read_csv('./data/external_data/rojour_boston_results_2016.csv', delimiter=',')
rojour_boston_results_2017 = pd.read_csv('./data/external_data/rojour_boston_results_2017.csv', delimiter=',')

# Transform data
boston_results_2013 = transform_llimllib_boston_data(df=llimllib_boston_results_2013, year=2013)
boston_results_2014 = transform_llimllib_boston_data(df=llimllib_boston_results_2014, year=2014)
boston_results_2015 = transform_rojour_boston_data(df=rojour_boston_results_2015, year=2015)
boston_results_2016 = transform_rojour_boston_data(df=rojour_boston_results_2016, year=2016)
boston_results_2017 = transform_rojour_boston_data(df=rojour_boston_results_2017, year=2017)
# write a csv
# results_all_years.to_csv('boston_all_years_nan.csv', encoding='utf-8', index=False)

# Combine Boston data


# sanity check
# print('number of rows: ' + str(len(results_all_years.index)))
# print(results_all_years.dtypes)
boston_results = combine_boston_data(list_dfs=[boston_results_2013, boston_results_2014, boston_results_2015,
                                               boston_results_2016, boston_results_2017])
