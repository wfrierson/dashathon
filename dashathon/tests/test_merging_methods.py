import pandas as pd
import dashathon.merging.merging_methods as merge


list_test_ages = [15, 19, 20, 24, 25, 30, 34, 35, 40, 44, 45, 50, 54, 55, 60, 64, 65, 70, 74, 75, 80, 81]


def test_convert_minutes_to_seconds():
    assert merge.convert_minutes_to_seconds(41.683) == 2500.98


def test_transform_llimllib_boston_data():
    test_llimllib = pd.read_csv('../data/external_data/llimllib_boston_results_2013.csv', delimiter=',', nrows=1)
    test_transformed_llimllib = merge.transform_llimllib_boston_data(test_llimllib, 2013)

    # Dropping name column because it's weird to use someone's name in a unit test...
    # Also, the 'name' isn't used in the dashboard.
    test_transformed_llimllib.drop('name', axis='columns', inplace=True)

    expected_llimllib_dict = {'25k': {0: 2992.2}, 'age': {0: 28}, 'division': {0: 9},
                              '10k': {0: 1090.8}, 'gender': {0: 'M'}, 'half': {0: 2455.8}, 'official_time': {0: 5454.0},
                              'bib': {0: 'W1'}, 'citizen': {0: pd.np.nan}, 'country': {0: 'CAN'}, 'overall': {0: 9},
                              'pace': {0: 208.20000000000002}, 'state': {0: 'ON'}, '30k': {0: 3724.2}, '5k': {0: 534.0},
                              'genderdiv': {0: 9}, '20k': {0: 2328.0}, '35k': {0: 4483.8}, 'city': {0: 'Toronto'},
                              '40k': {0: 5133.0}, 'year': {0: 2013}, '15k': {0: pd.np.nan},
                              'gender_place': {0: pd.np.nan}}

    df_expected_llimllib = pd.DataFrame.from_dict(expected_llimllib_dict)
    assert df_expected_llimllib.equals(test_transformed_llimllib)


def test_convert_string_to_seconds():
    assert merge.convert_string_to_seconds('00:41:41') == 2501


def test_transform_rojour_boston_data():
    test_rojour = pd.read_csv('../data/external_data/rojour_boston_results_2015.csv', delimiter=',', nrows=1)
    test_transformed_rojour = merge.transform_rojour_boston_data(test_rojour, 2015)

    # Dropping name column because it's weird to use someone's name in a unit test...
    # Also, the 'name' isn't used in the dashboard.
    test_transformed_rojour.drop('name', axis='columns', inplace=True)

    expected_rojour_dict = {'Unnamed: 0': {0: 0}, 'bib': {0: 3}, 'age': {0: 25},
                            'gender': {0: 'M'}, 'city': {0: 'Ambo'}, 'state': {0: pd.np.nan}, 'country': {0: 'ETH'},
                            'citizen': {0: pd.np.nan}, '5k': {0: 883}, '10k': {0: 1783}, '15k': {0: 2697},
                            '20k': {0: 3629}, 'half': {0: 3842}, '25k': {0: 4567}, '30k': {0: 5520}, '35k': {0: 6479},
                            '40k': {0: 7359}, 'pace': {0: '0:04:56'}, 'Proj Time': {0: '-'}, 'official_time': {0: 7757},
                            'overall': {0: 1}, 'gender_place': {0: 1}, 'division': {0: 1}, 'year': {0: 2015},
                            'genderdiv': {0: pd.np.nan}}

    df_expected_rojour = pd.DataFrame.from_dict(expected_rojour_dict)
    assert df_expected_rojour.equals(test_transformed_rojour)


def test_band_age():
    list_test_band_age = [list(merge.band_age(age)) for age in list_test_ages]
    df_test_band_age = pd.DataFrame.from_dict(dict(zip(list_test_ages, list_test_band_age)), orient='index')

    dict_expected = {15: [1, '<= 19'], 19: [1, '<= 19'], 20: [2, '20-24'], 24: [2, '20-24'], 25: [3, '25-29'],
                     30: [4, '30-34'], 34: [4, '30-34'], 35: [5, '35-39'], 40: [6, '40-44'], 44: [6, '40-44'],
                     45: [7, '45-49'], 50: [8, '50-54'], 54: [8, '50-54'], 55: [9, '55-59'], 60: [10, '60-64'],
                     64: [10, '60-64'], 65: [11, '65-69'], 70: [12, '70-74'], 74: [12, '70-74'], 75: [13, '75-79'],
                     80: [14, '80+'], 81: [14, '80+']}

    df_expected = pd.DataFrame.from_dict(dict_expected, orient='index')
    assert df_expected.equals(df_test_band_age)


def test_append_age_banding():
    df_age = pd.DataFrame().from_dict({'age': list_test_ages})
    df_test = merge.append_age_banding(df_age)

    dict_expected = {15: [1, '<= 19'], 19: [1, '<= 19'], 20: [2, '20-24'], 24: [2, '20-24'], 25: [3, '25-29'],
                     30: [4, '30-34'], 34: [4, '30-34'], 35: [5, '35-39'], 40: [6, '40-44'], 44: [6, '40-44'],
                     45: [7, '45-49'], 50: [8, '50-54'], 54: [8, '50-54'], 55: [9, '55-59'], 60: [10, '60-64'],
                     64: [10, '60-64'], 65: [11, '65-69'], 70: [12, '70-74'], 74: [12, '70-74'], 75: [13, '75-79'],
                     80: [14, '80+'], 81: [14, '80+']}

    df_expected = pd.DataFrame.from_dict(dict_expected, orient='index')
    df_expected.index.name = 'age'
    df_expected.reset_index(inplace=True)
    df_expected = df_expected.rename({0: 'age_bucket', 1: 'age_range'}, axis='columns')

    assert df_expected.equals(df_test)


def test_combine_boston_data():
    test_llimllib = pd.read_csv('../data/external_data/llimllib_boston_results_2013.csv', delimiter=',', nrows=1)
    test_transformed_llimllib = merge.transform_llimllib_boston_data(test_llimllib, 2013)
    test_rojour = pd.read_csv('../data/external_data/rojour_boston_results_2015.csv', delimiter=',', nrows=1)
    test_transformed_rojour = merge.transform_rojour_boston_data(test_rojour, 2015)
    df_test = merge.combine_boston_data([test_transformed_llimllib, test_transformed_rojour])
    df_test.drop('name', axis='columns', inplace=True)

    expected_llimllib_dict = {'25k': {0: 2992.2}, 'age': {0: 28}, 'division': {0: 9},
                              '10k': {0: 1090.8}, 'gender': {0: 'M'}, 'half': {0: 2455.8}, 'official_time': {0: 5454.0},
                              'bib': {0: 'W1'}, 'citizen': {0: pd.np.nan}, 'country': {0: 'CAN'}, 'overall': {0: 9},
                              'state': {0: 'ON'}, '30k': {0: 3724.2}, '5k': {0: 534.0},
                              'genderdiv': {0: 9}, '20k': {0: 2328.0}, '35k': {0: 4483.8}, 'city': {0: 'Toronto'},
                              '40k': {0: 5133.0}, 'year': {0: 2013}, '15k': {0: pd.np.nan},
                              'gender_place': {0: pd.np.nan}, 'age_bucket': {0: 3}}

    df_expected_llimllib = pd.DataFrame.from_dict(expected_llimllib_dict)
    expected_rojour_dict = {'bib': {0: 3}, 'age': {0: 25},
                            'gender': {0: 'M'}, 'city': {0: 'Ambo'}, 'state': {0: pd.np.nan}, 'country': {0: 'ETH'},
                            'citizen': {0: pd.np.nan}, '5k': {0: 883}, '10k': {0: 1783}, '15k': {0: 2697},
                            '20k': {0: 3629}, 'half': {0: 3842}, '25k': {0: 4567}, '30k': {0: 5520}, '35k': {0: 6479},
                            '40k': {0: 7359}, 'official_time': {0: 7757}, 'overall': {0: 1}, 'gender_place': {0: 1},
                            'division': {0: 1}, 'year': {0: 2015}, 'genderdiv': {0: pd.np.nan}}

    df_expected_rojour = pd.DataFrame.from_dict(expected_rojour_dict)
    df_expected = pd.concat([df_expected_llimllib, df_expected_rojour])
    df_expected['age_bucket'] = [3] * 2
    df_expected['age_range'] = ['25-29']*2

    headers = ['10k', '15k', '20k', '25k', '30k', '35k', '40k', '5k', 'Proj Time', 'Unnamed: 0', 'age', 'bib',
               'citizen', 'city', 'country', 'division', 'gender', 'gender_place', 'genderdiv', 'half', 'official_time',
               'overall', 'pace', 'state', 'year', 'age_bucket', 'age_range']

    # For ease, reorder columns in each DataFrame
    df_expected = df_expected.reindex(columns=headers)
    df_test = df_test.reindex(columns=headers)

    assert df_expected.equals(df_test)


def test_pipe_reader():
    assert merge.pipe_reader('../data/scraped_data/chicago_marathon_2017_M.csv').shape == (22824, 20)
