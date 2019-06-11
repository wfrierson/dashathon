import pandas as pd
import numpy as np

#read in data from GitHub
results_2013 = pd.read_csv('github/results_2013.csv', delimiter=',')
results_2014 = pd.read_csv('github/results_2014.csv', delimiter=',')

# missing splits are represented with a string character '-'
# this causes pd to read the split cols in as strings
# I changed the '-' placeholder to a numpy nan
results_2013['5k'].replace('-', np.nan, inplace=True)
results_2013['10k'].replace('-', np.nan, inplace=True)
results_2013['20k'].replace('-', np.nan, inplace=True)
results_2013['half'].replace('-',np.nan, inplace=True)
results_2013['25k'].replace('-', np.nan, inplace=True)
results_2013['30k'].replace('-', np.nan, inplace=True)
results_2013['35k'].replace('-', np.nan, inplace=True)
results_2013['40k'].replace('-', np.nan, inplace=True)

results_2014['5k'].replace('-', np.nan, inplace=True)
results_2014['10k'].replace('-', np.nan, inplace=True)
results_2014['20k'].replace('-', np.nan, inplace=True)
results_2014['half'].replace('-', np.nan, inplace=True)
results_2014['25k'].replace('-', np.nan, inplace=True)
results_2014['30k'].replace('-', np.nan, inplace=True)
results_2014['35k'].replace('-', np.nan, inplace=True)
results_2014['40k'].replace('-', np.nan, inplace=True)

# now can explicitely convert these columns to float even with nan vals
results_2013 = results_2013.astype({"5k": float, "10k": float, 
                                    "20k": float, "half": float,
                                    "25k": float, "30k": float,
                                    "35k": float, "40k": float,
                                    "official": float})
results_2014 = results_2014.astype({"5k": float, "10k": float, 
                                    "20k": float, "half": float,
                                    "25k": float, "30k": float,
                                    "35k": float, "40k": float,
                                    "official": float})

# in this data the all times were given as total minutes in standard decimals
# we decided to use total seconds as a better base unit
def convert_time(m):
    s = m * 60
    return (s)

results_2013['official'] = results_2013['official'].apply(convert_time)
results_2013['pace'] = results_2013['pace'].apply(convert_time)
results_2013['5k'] = results_2013['5k'].apply(convert_time)
results_2013['10k'] = results_2013['10k'].apply(convert_time)
results_2013['20k'] = results_2013['20k'].apply(convert_time)
results_2013['half'] = results_2013['half'].apply(convert_time)
results_2013['25k'] = results_2013['25k'].apply(convert_time)
results_2013['30k'] = results_2013['30k'].apply(convert_time)
results_2013['35k'] = results_2013['35k'].apply(convert_time)
results_2013['40k'] = results_2013['40k'].apply(convert_time)

results_2014['official'] = results_2014['official'].apply(convert_time)
results_2014['pace'] = results_2014['pace'].apply(convert_time)
results_2014['5k'] = results_2014['5k'].apply(convert_time)
results_2014['10k'] = results_2014['10k'].apply(convert_time)
results_2014['20k'] = results_2014['20k'].apply(convert_time)
results_2014['half'] = results_2014['half'].apply(convert_time)
results_2014['25k'] = results_2014['25k'].apply(convert_time)
results_2014['30k'] = results_2014['30k'].apply(convert_time)
results_2014['35k'] = results_2014['35k'].apply(convert_time)
results_2014['40k'] = results_2014['40k'].apply(convert_time)

# append cols to indicate year so data can be combined
results_2013['year'] = 2013
results_2014['year'] = 2014

# append a col for 15k split for easier merging of data
# default value will be a numpy nan
results_2013['15k'] = np.nan
results_2014['15k'] = np.nan

# append a col for gender placing
# default value will be a numpy nan
results_2013['gender_place'] = np.nan
results_2014['gender_place'] = np.nan


# read in data from kaggle
results_2015 = pd.read_csv('kaggle/results_2015.csv', delimiter=',')
results_2016 = pd.read_csv('kaggle/results_2016.csv', delimiter=',')
results_2017 = pd.read_csv('kaggle/results_2017.csv', delimiter=',')

# drop columns: 2015, 2017 contain an unnecessary column which simply indexes the rows
# 2015, 2016, 2017 all contain a 'Proj Time' col which does not contain any valid data
results_2015 = results_2015.drop([results_2015.columns[0],'Proj Time'], 1)
results_2016 = results_2016.drop('Proj Time', axis=1)
results_2017 = results_2017.drop([results_2017.columns[0],'Proj Time'], axis=1)

# the times in the kaggle data are formatted as strings hh:mm:ss
# we want these times in totqal seconds
# again I have used numpy nans for missing values

# at least one row in 2015 had an incomprehensible official finish time: 0.124548611111111
# I believe there was only one, but the try/catch below should handle 
# missing values, placeholder '-', and bad values
def get_sec(time_str):
    try:
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    except:
        return np.nan

#2015
results_2015['Official Time'] =  results_2015['Official Time'].apply(get_sec)
results_2015.dropna(subset = ['Official Time'])
results_2015['Pace'] =  results_2015['Pace'].apply(get_sec)
results_2015['5K'] =  results_2015['5K'].apply(get_sec)
results_2015['10K'] =  results_2015['10K'].apply(get_sec)
results_2015['15K'] =  results_2015['15K'].apply(get_sec)
results_2015['20K'] =  results_2015['20K'].apply(get_sec)
results_2015['Half'] =  results_2015['Half'].apply(get_sec)
results_2015['25K'] =  results_2015['25K'].apply(get_sec)
results_2015['30K'] =  results_2015['30K'].apply(get_sec)
results_2015['35K'] =  results_2015['35K'].apply(get_sec)
results_2015['40K'] =  results_2015['40K'].apply(get_sec)

# 2016
# no similar problems in 2016 as far as I can tell
results_2016['Official Time'] =  results_2016['Official Time'].apply(get_sec)
results_2016['Pace'] =  results_2016['Pace'].apply(get_sec)
results_2016['5K'] =  results_2016['5K'].apply(get_sec)
results_2016['10K'] =  results_2016['10K'].apply(get_sec)
results_2016['15K'] =  results_2016['15K'].apply(get_sec)
results_2016['20K'] =  results_2016['20K'].apply(get_sec)
results_2016['Half'] =  results_2016['Half'].apply(get_sec)
results_2016['25K'] =  results_2016['25K'].apply(get_sec)
results_2016['30K'] =  results_2016['30K'].apply(get_sec)
results_2016['35K'] =  results_2016['35K'].apply(get_sec)
results_2016['40K'] =  results_2016['40K'].apply(get_sec)

# 2017
# no similar problems in 2017 as far as I can tell
results_2017['Official Time'] =  results_2017['Official Time'].apply(get_sec)
results_2017['Pace'] =  results_2017['Pace'].apply(get_sec)
results_2017['5K'] =  results_2017['5K'].apply(get_sec)
results_2017['10K'] =  results_2017['10K'].apply(get_sec)
results_2017['15K'] =  results_2017['15K'].apply(get_sec)
results_2017['20K'] =  results_2017['20K'].apply(get_sec)
results_2017['Half'] =  results_2017['Half'].apply(get_sec)
results_2017['25K'] =  results_2017['25K'].apply(get_sec)
results_2017['30K'] =  results_2017['30K'].apply(get_sec)
results_2017['35K'] =  results_2017['35K'].apply(get_sec)
results_2017['40K'] =  results_2017['40K'].apply(get_sec)

# append cols to indicate year so data can be combined
results_2015['year'] = 2015
results_2016['year'] = 2016
results_2017['year'] = 2017

# add an empty genderdiv col to ensure col match
results_2015['genderdiv'] = np.nan
results_2016['genderdiv'] = np.nan
results_2017['genderdiv'] = np.nan

# rename a bunch of cols in the kaggle data to ensure exaxt match
# lower case names are just a personal preference
results_2015 = results_2015.rename(columns={'Age':'age', 'Official Time':'official_time',
                             'Bib':'bib', 'Citizen':'citizen', 'Overall':'overall',
                             'Pace':'pace', 'State':'state', 'Country':'country',
                             'City':'city', 'Name':'name', 'Division':'division',
                             'M/F':'gender', '5K':'5k', '10K':'10k', '15K':'15k',
                             '20K':'20k', 'Half':'half', '25K':'25k', '30K':'30k',
                             '35K':'35k', '40K':'40k', 'Unnamed: 9':'para_status',
                             'Gender':'gender_place'})    
    
results_2016 = results_2016.rename(columns={'Age':'age', 'Official Time':'official_time',
                             'Bib':'bib', 'Citizen':'citizen', 'Overall':'overall',
                             'Pace':'pace', 'State':'state', 'Country':'country',
                             'City':'city', 'Name':'name', 'Division':'division',
                             'M/F':'gender', '5K':'5k', '10K':'10k', '15K':'15k',
                             '20K':'20k', 'Half':'half', '25K':'25k', '30K':'30k',
                             '35K':'35k', '40K':'40k', 'Unnamed: 8':'para_status',
                             'Gender':'gender_place'})
    
results_2017 = results_2017.rename(columns={'Age':'age', 'Official Time':'official_time',
                             'Bib':'bib', 'Citizen':'citizen', 'Overall':'overall',
                             'Pace':'pace', 'State':'state', 'Country':'country',
                             'City':'city', 'Name':'name', 'Division':'division',
                             'M/F':'gender', '5K':'5k', '10K':'10k', '15K':'15k',
                             '20K':'20k', 'Half':'half', '25K':'25k', '30K':'30k',
                             '35K':'35k', '40K':'40k', 'Unnamed: 9':'para_status',
                             'Gender':'gender_place'})

# as discussed, this section is dropping all runners with a para status
# then dropping those cols as they will be empty
results_2015 = results_2015[results_2015.para_status != 'MI']
results_2015 = results_2015[results_2015.para_status != 'VI']
results_2016 = results_2016[results_2016.para_status != 'MI']
results_2016 = results_2016[results_2016.para_status != 'VI']
results_2017 = results_2017[results_2017.para_status != 'MI']
results_2017 = results_2017[results_2017.para_status != 'VI']

results_2015 = results_2015.drop('para_status', axis=1)
results_2016 = results_2016.drop('para_status', axis=1)
results_2017 = results_2017.drop('para_status', axis=1)

# change a few col names in the GH data to ensure good merge
# lower case and under score is just my personal preference
results_2013 = results_2013.rename(columns={'official':'official_time',
                             'ctz':'citizen'})

results_2014 = results_2014.rename(columns={'official':'official_time',
                             'ctz':'citizen'})


# do the actuaL merge
# I used a concat to easily join all previous data frames and preserve all rows
# this should work because I already ensured column id match
results_all_years = pd.concat([results_2013, results_2014, results_2015,
                               results_2016, results_2017], sort=True)


# bucket the ages: I have included a str column for the age range 
# and an int col that will give us an id for each bucket
    
# NOTE: The age brackets on the BAA website are as follows:
# 14-19*, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 
# 55-59, 60-64, 65-70, 70-74, 75-79, and 80
# This places 70 into two brackets! I have assumed a typo and followed the pattern
# I have also ignored the minimum age in case it has not been the same in every year
def bin_ages(age):
    try:
        if (age <= 19):
            bid = 1
            bstr = '<= 19'
        elif (age <= 24):
            bid = 2
            bstr = '20-24'
        elif (age <= 29):
            bid = 3
            bstr = '25-29'
        elif (age <= 34):
            bid = 4
            bstr = '30-34'
        elif (age <= 39):
            bid = 5
            bstr = '35-39'
        elif (age <= 44):
            bid = 6
            bstr = '40-44'
        elif (age <= 49):
            bid = 7
            bstr = '45-49'
        elif (age <= 54):
            bid = 8
            bstr = '50-54'
        elif (age <= 59):
            bid = 9
            bstr = '55-59'
        elif (age <= 64):
            bid = 10
            bstr = '60-64'
        elif (age <= 69):
            bid = 11
            bstr = '65-69'
        elif (age <= 74):
            bid = 12
            bstr = '70-74'
        elif (age <= 79):
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
    return pd.concat((
        df,
        df[val].apply(
            lambda cell: pd.Series(func(cell), index=col_names))), axis=1) 

results_all_years = apply_and_concat(results_all_years, 'age', bin_ages, ['age_bucket', 'age_range'])

# write a csv
results_all_years.to_csv('boston_all_years_nan.csv', encoding='utf-8', index=False)

#sanity check
print('number of rows: ' + str(len(results_all_years.index)))
print(results_all_years.dtypes)










