import pandas as pd
import numpy as np


def convert_minutes_to_seconds(time_minutes):
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
    Transform 2013-2104 Boston Marathon data from llimllib's Github repo into a standard form for downstream processing.
    Namely, split times are converted to integer seconds.

    :param pandas.DataFrame df: DataFrame representing 2013-2014 Boston Marathon data from llimllib's Github repo.
    :param int year: Year of Boston Marathon
    :return: DataFrame of transformed marathon data
    :rtype: pandas.DataFrame
    """

    # Header names for split time field in llimllib marathon data
    headers_split = ['5k', '10k', '20k', 'half', '25k', '30k', '35k', '40k', 'official']

    # Replace nan placeholders with actual nan values
    for header in headers_split:
        df[header].replace('-', np.nan, inplace=True)

    # Cast split times to float
    dtypes_new = dict(zip(headers_split, [float] * len(headers_split)))
    df = df.astype(dtypes_new)

    # Convert split time from decimal minutes to seconds
    for header in headers_split + ['pace']:
        df[header] = df[header].apply(convert_minutes_to_seconds)

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
def convert_string_to_seconds(time_str):
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
    Transform 2015-2107 Boston Marathon data from rojour's Github repo into a standard form for downstream processing.
    Namely, split times are converted to integer seconds.

    :param pandas.DataFrame df: DataFrame representing 2015-2017 Boston Marathon data from rojour's Github repo.
    :param int year: Year of Boston Marathon
    :return: DataFrame of transformed marathon data
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
        df[header] = df[header].apply(convert_string_to_seconds)

    if year == 2015:
        df.dropna(subset=['Official Time'])

    # Create a year field and an empty field for 'genderdiv'
    df['year'] = year
    df['genderdiv'] = np.nan

    # Map of field names to rename headers of df to ensure consistency with transform_llimllib_boston_data
    headers_map = {'Age': 'age', 'Official Time': 'official_time', 'Bib': 'bib', 'Citizen': 'citizen',
                   'Overall': 'overall', 'Pace': 'pace', 'State': 'state', 'Country': 'country', 'City': 'city',
                   'Name': 'name', 'Division': 'division', 'M/F': 'gender', '5K': '5k', '10K': '10k', '15K': '15k',
                   '20K': '20k', 'Half': 'half', '25K': '25k', '30K': '30k', '35K': '35k', '40K': '40k',
                   'Gender': 'gender_place'}

    # The rojour data has an unnamed field that varies depending on the year.
    # We can't drop this field since it's used later to remove certain records.
    if year == 2016:
        headers_map.update({'Unnamed: 8': 'para_status'})
    else:
        headers_map.update({'Unnamed: 9': 'para_status'})

    df = df.rename(columns=headers_map)

    # Drop all runners with a 'para' status and then drop the para_status field
    df = df[df.para_status != 'MI']
    df = df[df.para_status != 'VI']
    df = df.drop('para_status', axis=1)

    return df


def band_age(age):
    """
    Banding method that maps a Boston Marathon runner's (integer) age to a labeled age band and level.

    **Note**: The age brackets on the BAA website are as follows:

    * 14-19*, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, 65-70, 70-74, 75-79, and 80

    This places 70 into two brackets. We have assumed this is a typo and use the bands '65-69' and '70-74'.
    We have also ignored the minimum age in case it has not been the same in every year

    :param int age: Age of Boston Marathon runner
    :return: (banded_level, age_banding) where: banded_level is banded level of age for Boston Marathon runner and
    age_banding is banding of age for Boston Marathon runner in 5 year increments
    :rtype: (int, str)
    """
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


def append_age_banding(df):
    """
    Method that appends a banding of the age field, which is consistent with the method `band_age`.

    **Note**: This method assumes that the DataFrame `df` include the (int) field named 'age', which is

    :param pandas.DataFrame df: DataFrame of transformed marathon data
    :return: DataFrame of transformed marathon data that includes a banding of age consistent with method `band_age`
    :rtype: pandas.DataFrame
    """
    return pd.concat((
        df,
        df['age'].apply(lambda cell: pd.Series(band_age(cell), index=['age_bucket', 'age_range']))
    ), axis=1)


def combine_boston_data(list_dfs):
    """
    Method that takes the union of a list of DataFrames each representing different years of Boston Marathon data. The
    field named 'age' is also used to append a banding for runners' age.

    :param list[pandas.DataFrame] list_dfs: List of DataFrames containing transformed marathon data
    :return: DataFrame of transformed and unioned marathon data that includes a banding of age consistent with method
    `band_age`
    :rtype: pandas.DataFrame
    """
    df_combine = pd.concat(list_dfs, sort=True)
    df_combine = append_age_banding(df_combine)
    df_combine.drop(['pace', 'Proj Time', 'Unnamed: 0'], axis=1, inplace=True)

    return df_combine
