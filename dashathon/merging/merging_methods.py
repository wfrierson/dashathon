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

    :param str time_str: Time in a string format 'HH:MM:SS'
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


def pipe_reader(input_file):
    """
    Read datasets without pandas read_csv when we have a pipe delimiter dataset
    with commas inside columns

    :param str input_file: File path
    :return: The pipe delimited file as a DataFrame
    :rtype: pandas.DataFrame
    """
    with open(input_file, 'r') as f:
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


def process_boston_data():
    """
    Method to import, transform, and combine Boston Marathon data.

    :return: DataFrame of transformed and combined Boston Marathon data.
    :rtype: pandas.DataFrame
    """
    # Read in data
    llimllib_boston_results_2013 = pd.read_csv('../data/external_data/llimllib_boston_results_2013.csv',
                                               delimiter=',')
    llimllib_boston_results_2014 = pd.read_csv('../data/external_data/llimllib_boston_results_2014.csv',
                                               delimiter=',')
    rojour_boston_results_2015 = pd.read_csv('../data/external_data/rojour_boston_results_2015.csv',
                                             delimiter=',')
    rojour_boston_results_2016 = pd.read_csv('../data/external_data/rojour_boston_results_2016.csv',
                                             delimiter=',')
    rojour_boston_results_2017 = pd.read_csv('../data/external_data/rojour_boston_results_2017.csv',
                                             delimiter=',')

    # Transform data
    boston_results_2013 = transform_llimllib_boston_data(df=llimllib_boston_results_2013, year=2013)
    boston_results_2014 = transform_llimllib_boston_data(df=llimllib_boston_results_2014, year=2014)
    boston_results_2015 = transform_rojour_boston_data(df=rojour_boston_results_2015, year=2015)
    boston_results_2016 = transform_rojour_boston_data(df=rojour_boston_results_2016, year=2016)
    boston_results_2017 = transform_rojour_boston_data(df=rojour_boston_results_2017, year=2017)

    # Combine Boston data
    boston_results = combine_boston_data(list_dfs=[boston_results_2013, boston_results_2014, boston_results_2015,
                                                   boston_results_2016, boston_results_2017])

    # Append host city to distinguish among other marathon results
    boston_results['host_city'] = 'Boston'

    # Removing gender 'W' from bib in boston base
    boston_results.bib = boston_results.bib.str.replace('W', '')

    return boston_results


def process_nyc_data():
    """
    Method to import, transform, and combine NYC Marathon data.

    :return: DataFrame of transformed and combine NYC Marathon data.
    :rtype: pandas.DataFrame
    """
    andreanr_nyc_results_2015 = pd.read_csv('../data/external_data/andreanr_nyc_results_2015.csv')
    andreanr_nyc_results_2016 = pd.read_csv('../data/external_data/andreanr_nyc_results_2016.csv')
    andreanr_nyc_results_2017 = pd.read_csv('../data/external_data/andreanr_nyc_results_2017.csv')
    andreanr_nyc_results_2018 = pd.read_csv('../data/external_data/andreanr_nyc_results_2018.csv')

    # Merging all nyc datasets first
    andreanr_nyc_results = andreanr_nyc_results_2015.append([andreanr_nyc_results_2016, andreanr_nyc_results_2017,
                                                             andreanr_nyc_results_2018], ignore_index=True)

    # Removing records with missing split times
    headers_nyc_splits = ['splint_10k', 'splint_15k', 'splint_20k', 'splint_25k', 'splint_30k', 'splint_35k',
                          'splint_40k', 'splint_5k', 'splint_half', 'official_time']
    andreanr_nyc_results = andreanr_nyc_results.dropna(subset=headers_nyc_splits + ['age'])

    # Consistent age
    andreanr_nyc_results.age = andreanr_nyc_results.age.astype('int64')

    # Converting HH:MM:SS to seconds
    for header in headers_nyc_splits:
        andreanr_nyc_results[header] = andreanr_nyc_results[header].apply(convert_string_to_seconds)

    # Assuming na values for absent columns in nyc data
    andreanr_nyc_results['citizen'] = None
    andreanr_nyc_results['division'] = None
    andreanr_nyc_results['genderdiv'] = None
    andreanr_nyc_results['age_bucket'] = None
    andreanr_nyc_results['age_range'] = None

    # Extracting and renaming relevant columns
    andreanr_nyc_results = andreanr_nyc_results[['splint_10k', 'splint_15k', 'splint_20k', 'splint_25k', 'splint_30k',
                                                 'splint_35k', 'splint_40k', 'splint_5k', 'age', 'bib', 'citizen',
                                                 'city', 'country', 'division', 'gender', 'place_gender', 'genderdiv',
                                                 'splint_half', 'name', 'official_time', 'place_overall',
                                                 'pace_per_mile', 'state', 'year', 'age_range', 'age_bucket']]

    # Pace_per_mile of NYC data is assumed to be same as pace of Boston data
    andreanr_nyc_results = andreanr_nyc_results.rename(columns={"splint_10k": "10k", "splint_15k": "15k",
                                                                "splint_20k": "20k", "splint_25k": "25k",
                                                                "splint_30k": "30k", "splint_35k": "35k",
                                                                "splint_40k": "40k", "splint_5k": "5k",
                                                                "place_gender": "gender_place", "splint_half": "half",
                                                                "place_overall": "overall", "pace_per_mile": "pace"})

    # Adding host city
    andreanr_nyc_results['host_city'] = 'NYC'

    return andreanr_nyc_results


def process_chicago_data():
    """
    Method to import, transform, and combine Chicago Marathon data.

    :return: DataFrame of transformed and combined Chicago Marathon data.
    :rtype: pandas.DataFrame
    """
    chi14m = pipe_reader('../data/scraped_data/chicago_marathon_2014_M.csv')
    chi14w = pipe_reader('../data/scraped_data/chicago_marathon_2014_W.csv')
    chi15m = pipe_reader('../data/scraped_data/chicago_marathon_2015_M.csv')
    chi15w = pipe_reader('../data/scraped_data/chicago_marathon_2015_W.csv')
    chi16m = pipe_reader('../data/scraped_data/chicago_marathon_2016_M.csv')
    chi16w = pipe_reader('../data/scraped_data/chicago_marathon_2016_W.csv')
    chi17m = pipe_reader('../data/scraped_data/chicago_marathon_2017_M.csv')
    chi17w = pipe_reader('../data/scraped_data/chicago_marathon_2017_W.csv')

    # Merging all chicago datasets first
    chicago_results = chi14m.append([chi14w, chi15m, chi15w, chi16m, chi16w, chi17m, chi17w], ignore_index=True)

    # Bringing around required datatypes
    chicago_results[['year', 'bib', 'rank_gender', 'rank_age_group', 'overall']] = chicago_results[
        ['year', 'bib', 'rank_gender', 'rank_age_group', 'overall']].astype('int64')
    chicago_results[['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']] = chicago_results[
        ['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']].astype('float64')

    chicago_results['age'] = np.nan
    chicago_results['age_bucket'] = None
    chicago_results['citizen'] = None
    chicago_results['division'] = None
    chicago_results['genderdiv'] = None
    chicago_results['name'] = None
    chicago_results['official_time'] = None
    chicago_results['pace'] = None
    chicago_results['host_city'] = 'Chicago'

    chicago_results = chicago_results.rename(columns={'age_group': 'age_range', 'rank_gender': 'gender_place'})
    chicago_results = chicago_results.drop(['rank_age_group', 'finish'], axis=1)

    return chicago_results


def process_london_data():
    """
    Method to import, transform, and combine London Marathon data.

    :return: DataFrame of transformed and combined London Marathon data.
    :rtype: pandas.DataFrame
    """
    # Reading in the datasets
    lon14m = pd.read_csv('../data/scraped_data/london_marathon_2014_M.csv',
                         sep='|', usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                           'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k',
                                           '40k',
                                           'finish'])
    lon14me = pd.read_csv('../data/scraped_data/london_marathon_2014_M_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon14w = pd.read_csv('../data/scraped_data/london_marathon_2014_W.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon14we = pd.read_csv('../data/scraped_data/london_marathon_2014_W_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon15m = pd.read_csv('../data/scraped_data/london_marathon_2015_M.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon15me = pd.read_csv('../data/scraped_data/london_marathon_2015_M_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon15w = pd.read_csv('../data/scraped_data/london_marathon_2015_W.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon15we = pd.read_csv('../data/scraped_data/london_marathon_2015_W_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon16m = pd.read_csv('../data/scraped_data/london_marathon_2016_M.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon16me = pd.read_csv('../data/scraped_data/london_marathon_2016_M_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon16w = pd.read_csv('../data/scraped_data/london_marathon_2016_W.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon16we = pd.read_csv('../data/scraped_data/london_marathon_2016_W_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon17m = pd.read_csv('../data/scraped_data/london_marathon_2017_M.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon17me = pd.read_csv('../data/scraped_data/london_marathon_2017_M_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])
    lon17w = pd.read_csv('../data/scraped_data/london_marathon_2017_W.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    lon17we = pd.read_csv('../data/scraped_data/london_marathon_2017_W_elite.csv', sep='|',
                          usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                   'finish'])

    london_results = lon14m.append([lon14me, lon14w, lon14we, lon15m, lon15me, lon15w, lon15we, lon16m, lon16me, lon16w,
                                    lon16we, lon17m, lon17me, lon17w, lon17we], ignore_index=True)

    london_results['city'] = None
    london_results['state'] = None
    london_results['host_city'] = 'London'

    return london_results


def process_berlin_data():
    """
    Method to import, transform, and combine Berlin Marathon data.

    :return: DataFrame of transformed and combined Berlin Marathon data.
    :rtype: pandas.DataFrame
    """
    ber14m = pd.read_csv('../data/scraped_data/london_marathon_2014_M.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber14w = pd.read_csv('../data/scraped_data/london_marathon_2014_M_elite.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber15m = pd.read_csv('../data/scraped_data/london_marathon_2014_W.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber15w = pd.read_csv('../data/scraped_data/london_marathon_2014_W_elite.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber16m = pd.read_csv('../data/scraped_data/london_marathon_2015_M.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber16w = pd.read_csv('../data/scraped_data/london_marathon_2015_M_elite.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber17m = pd.read_csv('../data/scraped_data/london_marathon_2015_W.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])
    ber17w = pd.read_csv('../data/scraped_data/london_marathon_2015_W_elite.csv', sep='|',
                         usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                  'finish'])

    berlin_results = ber14m.append([ber14w, ber15m, ber15w, ber16m, ber16w, ber17m, ber17w], ignore_index=True)

    berlin_results['city'] = None
    berlin_results['state'] = None
    berlin_results['host_city'] = 'Berlin'

    return berlin_results
