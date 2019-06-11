import pandas as pd
import dashathon.merging.merging_methods as merge
# from merging.merging_methods import transform_llimllib_boston_data
# from web_scraping.merging_methods import transform_rojour_boston_data
# from web_scraping.merging_methods import combine_boston_data

# Read in data
llimllib_boston_results_2013 = pd.read_csv('dashathon/data/external_data/llimllib_boston_results_2013.csv',
                                           delimiter=',')
llimllib_boston_results_2014 = pd.read_csv('dashathon/data/external_data/llimllib_boston_results_2014.csv',
                                           delimiter=',')
rojour_boston_results_2015 = pd.read_csv('dashathon/data/external_data/rojour_boston_results_2015.csv', delimiter=',')
rojour_boston_results_2016 = pd.read_csv('dashathon/data/external_data/rojour_boston_results_2016.csv', delimiter=',')
rojour_boston_results_2017 = pd.read_csv('dashathon/data/external_data/rojour_boston_results_2017.csv', delimiter=',')

# Transform data
boston_results_2013 = merge.transform_llimllib_boston_data(df=llimllib_boston_results_2013, year=2013)
boston_results_2014 = merge.transform_llimllib_boston_data(df=llimllib_boston_results_2014, year=2014)
boston_results_2015 = merge.transform_rojour_boston_data(df=rojour_boston_results_2015, year=2015)
boston_results_2016 = merge.transform_rojour_boston_data(df=rojour_boston_results_2016, year=2016)
boston_results_2017 = merge.transform_rojour_boston_data(df=rojour_boston_results_2017, year=2017)

# Combine Boston data
boston_results = merge.combine_boston_data(list_dfs=[boston_results_2013, boston_results_2014, boston_results_2015,
                                                     boston_results_2016, boston_results_2017])
