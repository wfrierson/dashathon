import numpy as np
import pandas as pd
import time
import datetime

# Boston datasets read in
base = pd.read_csv('dashathon/data/combined_data/boston_all_years_nan.csv')

base['host_city'] = 'Boston'

# Removing gender 'W' from bib in boston base
base.bib = base.bib.str.replace('W', '')

# Merging with NYC
andreanr_nyc_results_2015 = pd.read_csv('dashathon/data/external_data/andreanr_nyc_results_2015.csv')
andreanr_nyc_results_2016 = pd.read_csv('dashathon/data/external_data/andreanr_nyc_results_2016.csv')
andreanr_nyc_results_2017 = pd.read_csv('dashathon/data/external_data/andreanr_nyc_results_2017.csv')
andreanr_nyc_results_2018 = pd.read_csv('dashathon/data/external_data/andreanr_nyc_results_2018.csv')


def converttime(t):
    """
    Converting time to seconds
    :param t: time in HH:MM:SS format
    :return: time returned as total seconds
    """
    t = str(t)
    x = time.strptime(t, '%H:%M:%S')
    return int(datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds())


# Merging all nyc datasets first
andreanr_nyc_results = andreanr_nyc_results_2015.append([andreanr_nyc_results_2016, andreanr_nyc_results_2017,
                                                         andreanr_nyc_results_2018], ignore_index=True)

# Removing records with missing split times
andreanr_nyc_results = andreanr_nyc_results.dropna(subset=['splint_10k', 'splint_15k', 'splint_20k', 'splint_25k',
                                                           'splint_30k', 'splint_35k', 'splint_40k', 'splint_5k',
                                                           'splint_half', 'age', 'official_time'])

# Consistent age
andreanr_nyc_results.age = andreanr_nyc_results.age.astype('int64')

# Converting HH:MM:SS to seconds
andreanr_nyc_results['splint_10k'] = andreanr_nyc_results['splint_10k'].apply(converttime)
andreanr_nyc_results['splint_15k'] = andreanr_nyc_results['splint_15k'].apply(converttime)
andreanr_nyc_results['splint_20k'] = andreanr_nyc_results['splint_20k'].apply(converttime)
andreanr_nyc_results['splint_25k'] = andreanr_nyc_results['splint_25k'].apply(converttime)
andreanr_nyc_results['splint_30k'] = andreanr_nyc_results['splint_30k'].apply(converttime)
andreanr_nyc_results['splint_35k'] = andreanr_nyc_results['splint_35k'].apply(converttime)
andreanr_nyc_results['splint_40k'] = andreanr_nyc_results['splint_40k'].apply(converttime)
andreanr_nyc_results['splint_5k'] = andreanr_nyc_results['splint_5k'].apply(converttime)
andreanr_nyc_results['splint_half'] = andreanr_nyc_results['splint_half'].apply(converttime)
andreanr_nyc_results['official_time'] = andreanr_nyc_results['official_time'].apply(converttime)

# Assuming na values for absent columns in nyc data
andreanr_nyc_results['citizen'] = None
andreanr_nyc_results['division'] = None
andreanr_nyc_results['genderdiv'] = None
andreanr_nyc_results['age_bucket'] = None
andreanr_nyc_results['age_range'] = None

# Extracting and renaming relevant columns
andreanr_nyc_results = andreanr_nyc_results[['splint_10k', 'splint_15k', 'splint_20k', 'splint_25k', 'splint_30k',
                                             'splint_35k', 'splint_40k', 'splint_5k', 'age', 'bib', 'citizen', 'city',
                                             'country', 'division', 'gender', 'place_gender', 'genderdiv',
                                             'splint_half', 'name', 'official_time', 'place_overall', 'pace_per_mile',
                                             'state', 'year', 'age_range', 'age_bucket']]

# Pace_per_mile of NYC data is assumed to be same as pace of Boston data
andreanr_nyc_results = andreanr_nyc_results.rename(columns={"splint_10k": "10k", "splint_15k": "15k",
                                                            "splint_20k": "20k", "splint_25k": "25k",
                                                            "splint_30k": "30k", "splint_35k": "35k",
                                                            "splint_40k": "40k", "splint_5k": "5k",
                                                            "place_gender": "gender_place", "splint_half": "half",
                                                            "place_overall": "overall", "pace_per_mile": "pace"})

# Adding host city
andreanr_nyc_results['host_city'] = 'NYC'

# Merge with base data
df = base.append(andreanr_nyc_results, ignore_index=True)


# Merging with Chicago


def pipe_reader(link):
    """
    Reads datasets without pandas read_csv when we have a pipe delimiter dataset with commas inside columns
    :param link: The local address link of the pipe delimited .CSV file to read in
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


# chi17m = pd.read_csv('dashathon/data/scraped_data/chicago_marathon_2017_M.csv',
#                      sep='|', usecols=['year', 'bib', 'age_group', 'gender', 'city', 'state', 'country', 'overall',
#                                        'rank_gender', 'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k',
#                                        '30k', '35k', '40k', 'finish'])

chi14m = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2014_M.csv')
chi14w = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2014_W.csv')
chi15m = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2015_M.csv')
chi15w = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2015_W.csv')
chi16m = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2016_M.csv')
chi16w = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2016_W.csv')
chi17m = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2017_M.csv')
chi17w = pipe_reader('dashathon/data/scraped_data/chicago_marathon_2017_W.csv')

# Merging all chicago datasets first
chi = chi14m.append([chi14w, chi15m, chi15w, chi16m, chi16w, chi17m, chi17w], ignore_index=True)

# Bringing around required datatypes
chi[['year', 'bib', 'rank_gender', 'rank_age_group', 'overall']] = chi[
    ['year', 'bib', 'rank_gender', 'rank_age_group', 'overall']].astype('int64')
chi[['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']] = chi[
    ['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']].astype('float64')

# chi.head()
chi['age'] = np.nan
chi['age_bucket'] = None
chi['citizen'] = None
chi['division'] = None
chi['genderdiv'] = None
chi['name'] = None
chi['official_time'] = None
chi['pace'] = None
chi['host_city'] = 'Chicago'

chi = chi.rename(columns={'age_group': 'age_range', 'rank_gender': 'gender_place'})
chi = chi.drop(['rank_age_group', 'finish'], axis=1)

df = df.append(chi, ignore_index=True)

# Merging with London
# Reading in the datasets
lon14m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_M.csv',
                     sep='|', usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                                       'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                                       'finish'])
lon14me = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_M_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon14w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_W.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon14we = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_W_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon15m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_M.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon15me = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_M_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon15w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_W.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon15we = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_W_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon16m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2016_M.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon16me = pd.read_csv('dashathon/data/scraped_data/london_marathon_2016_M_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon16w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2016_W.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon16we = pd.read_csv('dashathon/data/scraped_data/london_marathon_2016_W_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon17m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2017_M.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon17me = pd.read_csv('dashathon/data/scraped_data/london_marathon_2017_M_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])
lon17w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2017_W.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
lon17we = pd.read_csv('dashathon/data/scraped_data/london_marathon_2017_W_elite.csv', sep='|',
                      usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                               'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                               'finish'])

lon = lon14m.append([lon14me, lon14w, lon14we, lon15m, lon15me, lon15w, lon15we, lon16m, lon16me, lon16w, lon16we,
                     lon17m, lon17me, lon17w, lon17we], ignore_index=True)

lon['city'] = None
lon['state'] = None
lon['host_city'] = 'London'

# Merging with Berlin
ber14m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_M.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber14w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_M_elite.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber15m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_W.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber15w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2014_W_elite.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber16m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_M.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber16w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_M_elite.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber17m = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_W.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])
ber17w = pd.read_csv('dashathon/data/scraped_data/london_marathon_2015_W_elite.csv', sep='|',
                     usecols=['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                              'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k',
                              'finish'])

ber = ber14m.append([ber14w, ber15m, ber15w, ber16m, ber16w, ber17m, ber17w], ignore_index=True)

ber['city'] = None
ber['state'] = None
ber['host_city'] = 'Berlin'

# Merging together London and Berlin as they have similar formats
lonber = lon.append(ber, ignore_index=True)

lonber['age'] = np.nan
lonber['age_bucket'] = None
lonber['citizen'] = None
lonber['division'] = None
lonber['genderdiv'] = None
lonber['name'] = None
lonber['official_time'] = None
lonber['pace'] = None

lonber = lonber.rename(columns={'age_group': 'age_range', 'rank_gender': 'gender_place'})
lonber = lonber.drop(['rank_age_group', 'finish'], axis=1)

df = df.append(lonber, ignore_index=True)

# Aggregated changes
df['genderdiv'] = df['genderdiv'].astype('float64')
df['official_time'] = df['official_time'].astype('float64')

# Dropping age_bucket
df = df.drop(columns=['age_bucket'])

# Creating a new age_range column on basis of age
df = df.drop(columns={'age_range'})
age_map = pd.read_csv('age_map.csv')
df = pd.merge(df, age_map, on='age', how='left')

# Make gender consistent across all datasets
df['gender'] = df['gender'].replace('W', 'F')

# Dropping pace column for now
df = df.drop(columns={'pace'})

# Converting three letter country names to full country names
country_code = pd.read_csv('country_code_web.csv', usecols=['country', 'code'], encoding='latin-1')
country_code = country_code.rename(columns={'country': 'country_name'})
df = pd.merge(df, country_code, left_on='country', right_on='code', how='left')
df.country_name = df.country_name.fillna(df.country, inplace=True)
df = df.drop(['country'], axis=1)

df.to_csv('data_agg.csv', index=False)
