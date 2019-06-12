import unittest

import pandas as pd
import os
import dashathon.scraping.scraping_methods as scrape

headers_chicago = ['year', 'bib', 'age_group', 'gender', 'city', 'state', 'country', 'overall', 'rank_gender',
                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']

headers_london = headers_chicago.copy()
for unavailable_column in ['city', 'state']:
    headers_london.remove(unavailable_column)

headers_berlin = headers_chicago.copy()
for unavailable_column in ['city', 'state', 'overall']:
    headers_berlin.remove(unavailable_column)


class ScrapingMethodsTest(unittest.TestCase):

    def setUp(self):
        with open('test_file.txt', 'w') as f:
            f.write('this is the first line.\n')

    def tearDown(self):
        os.remove('test_file.txt')

    def test_strip_special_latin_char(self):
        test_string = 'thƝis ƛis a teōst: ÆæœƔþðßøÞĿØĳƧaÐŒƒ¿Ǣ'
        assert scrape.strip_special_latin_char(test_string) == 'this is a test: AEaeoethdssoTHOaDOEf'


    def test_strip_accents(self):
        test_string = 'thîš ìŝ ã tëśt'
        assert scrape.strip_accents(test_string) == 'this is a test'


    def test_convert_to_ascii(self):
        test_string = 'thƝîš ƛìŝ ã tëśt: ÆæœƔþðßøÞĿØĳƧaÐŒƒ¿Ǣ'
        assert scrape.convert_to_ascii(test_string) == 'this is a test: AEaeoethdssoTHOaDOEfAE'


    def test_row_count_csv(self):
        assert scrape.row_count_csv('test_file.txt') == 1


    def test_get_last_line_csv(self):
        assert scrape.get_last_line_csv('test_file.txt') == 'this is the first line.\n'


    def test_delete_last_line_csv(self):
        # Add dummy line of text
        open('test_delete_last_line.txt', 'wb').write(open('test_file.txt', 'rb').read())
        original_row_count = scrape.row_count_csv('test_delete_last_line.txt')
        scrape.delete_last_line_csv('test_delete_last_line.txt')
        deleted_row_count = os.stat('test_delete_last_line.txt').st_size
        assert original_row_count == 1 and deleted_row_count == 0


    # noinspection PyTypeChecker
    def test_scrape_chicago_marathon_urls(self):
        scraped_df = scrape.scrape_chicago_marathon_urls(url='http://chicago-history.r.mikatiming.de/2015/', year=2017,
                                                         event="MAR_999999107FA30900000000A1", gender='M',
                                                         num_results_per_page=1000, unit_test_ind=True)
        expected_scraped_df = pd.DataFrame(columns=['urls', 'city', 'state'])
        expected_scraped_df.loc[0] = [('http://chicago-history.r.mikatiming.de/2015/?content=detail&fpid=list&pid=list&idp='
                                       '999999107FA30900001CF732&lang=EN_CAP&event=MAR_999999107FA30900000000A1&lang=EN_CAP'
                                       '&num_results=1000&search%5Bsex%5D=M&search%5Bage_class%5D=%25&search_event='
                                       'MAR_999999107FA30900000000A1'), 'Portland', 'OR']
        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_london_marathon_urls(self):
        scraped_df = scrape.scrape_london_marathon_urls(url='http://results-2017.virginmoneylondonmarathon.com/2017/',
                                                        event='MAS', year=2017, gender='M', num_results_per_page=1000,
                                                        unit_test_ind=True)
        expected_scraped_df = pd.DataFrame(columns=['urls'])
        expected_scraped_df.loc[0] = [('http://results-2017.virginmoneylondonmarathon.com/2017/?content=detail&fpid=list&'
                                       'pid=list&idp=9999990F5ECC85000024C3F9&lang=EN_CAP&event=MAS&num_results=1000&search'
                                       '%5Bage_class%5D=%25&search%5Bsex%5D=M&search_event=MAS')]
        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_berlin_marathon_urls(self):
        scraped_df = scrape.scrape_berlin_marathon_urls(url='http://results.scc-events.com/2016/',
                                                        event='MAL_99999905C9AF3F0000000945', year=2016, gender='M',
                                                        num_results_per_page=100, unit_test_ind=True)
        expected_scraped_df = pd.DataFrame(columns=['urls'])
        expected_scraped_df.loc[0] = [('http://results.scc-events.com/2016/?content=detail&fpid=list&pid=list&idp='
                                       '00001705C9AF4A0000412F85&lang=DE&event=MAL_99999905C9AF3F0000000945&num_results='
                                       '100&search%5Bsex%5D=M&search_event=MAL_99999905C9AF3F0000000945')]
        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_chicago_runner_details(self):
        test_runner_info = [2016, '54250', '20-24', 'M', 'Portland', 'OR', 'USA', '40558', '22034', '1136']
        test_runner_info = [[cell] * 10 for cell in test_runner_info]
        test_split_times = [6160, 9775, 12867, None, None, 20341, None, None, None, 35276]
        test_runner_dict = dict(zip(headers_chicago[:10], test_runner_info))
        expected_scraped_df = pd.DataFrame()
        expected_scraped_df['split'] = headers_chicago[10:]
        expected_scraped_df['time'] = test_split_times
        expected_scraped_df[headers_chicago[:10]] = pd.DataFrame.from_dict(test_runner_dict)
        expected_scraped_df = pd.pivot_table(expected_scraped_df, index=headers_chicago[:10], columns='split',
                                             values='time', aggfunc='first').reset_index()
        expected_scraped_df = expected_scraped_df.reindex(headers_chicago, axis='columns')

        scraped_df = scrape.scrape_chicago_runner_details(url=('http://chicago-history.r.mikatiming.de/2015/?content=detail'
                                                               '&fpid=search&pid=search&idp=999999107FA309000019D3BA&lang='
                                                               'EN_CAP&event=MAR_999999107FA309000000008D&lang=EN_CAP&'
                                                               'search%5Bstart_no%5D=54250&search_event=ALL_EVENT_GROUP_'
                                                               '2016'), gender='M', city='Portland', state='OR')

        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_london_runner_details(self):
        test_runner_info = [2017, '1154', '18-39', 'M', 'GBR', '1', '1', '1']
        test_runner_info = [[cell] * 10 for cell in test_runner_info]
        test_split_times = [948, 1899, 2848, 3799, 4000, 4742, 5698, 6670, 7653, 8089]
        test_runner_dict = dict(zip(headers_london[:8], test_runner_info))
        expected_scraped_df = pd.DataFrame()
        expected_scraped_df['split'] = headers_london[8:]
        expected_scraped_df['time'] = test_split_times
        expected_scraped_df[headers_london[:8]] = pd.DataFrame.from_dict(test_runner_dict)
        expected_scraped_df = pd.pivot_table(expected_scraped_df, index=headers_london[:8], columns='split', values='time',
                                             aggfunc='first').reset_index()
        expected_scraped_df = expected_scraped_df.reindex(headers_london, axis='columns')

        scraped_df = scrape.scrape_london_runner_details(url=('http://results-2017.virginmoneylondonmarathon.com/2017/'
                                                              '?content=detail&fpid=list&pid=list&idp=9999990F5ECC85000024C'
                                                              '3F9&lang=EN_CAP&event=MAS&num_results=1000&search%5B'
                                                              'age_class%5D=%25&search%5Bsex%5D=M&search_event=MAS'),
                                                         year=2017, gender='M')
        # pd.DataFrame.equals is behaving strangely. For ease, casting the scraped values as integers, which they are
        # anyway.
        for split_time in headers_london[8:]:
            scraped_df[split_time] = scraped_df[split_time].astype('int64')

        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_berlin_runner_details(self):
        test_runner = [2016, '30529', '50-54', 'M', 'AUT', '26771', '4084', 2374, 4975, 7774, 10743, 11428, 14518, 18183,
                       None, None, 26648]
        test_runner = [[cell] for cell in test_runner]
        test_runner_dict = dict(zip(headers_berlin, test_runner))
        expected_scraped_df = pd.DataFrame.from_dict(test_runner_dict)
        expected_scraped_df = expected_scraped_df.reindex(headers_berlin, axis='columns')

        scraped_df = scrape.scrape_berlin_runner_details(url=('http://results.scc-events.com/2016/?content=detail&fpid='
                                                              'search&pid=search&idp=99999905C9AF460000404FFD&lang=EN&event'
                                                              '=MAL_99999905C9AF3F0000000945&search%5Bstart_no%5D=30529'
                                                              '&search_sort=name&search_event='
                                                              'MAL_99999905C9AF3F0000000945'), year=2016, gender='M')
        # pd.DataFrame.equals is behaving strangely. For ease, casting the scraped values as integers, which they are
        # anyway.
        for split_time in headers_berlin[7:]:
            scraped_df[split_time] = scraped_df[split_time].astype('int64', errors='ignore')
        scraped_df = scraped_df.replace({pd.np.nan: None})

        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_chicago_marathon(self):
        scraped_df_url = scrape.scrape_chicago_marathon_urls(url='http://chicago-history.r.mikatiming.de/2015/', year=2017,
                                                             event="MAR_999999107FA30900000000A1", gender='M',
                                                             num_results_per_page=1000, unit_test_ind=True)

        scrape.scrape_chicago_marathon(path_input='test_input_chicago.csv', path_output='test_output_chicago.csv',
                                       path_error='test_error_log_chicago.csv', gender='M', headers=headers_chicago,
                                       df_urls=scraped_df_url)

        scraped_df = pd.read_csv('test_output_chicago.csv', header=0, sep='|')
        for split_time in headers_chicago[10:]:
            scraped_df[split_time] = scraped_df[split_time].astype('int64')

        remove_list = ['test_input_chicago.csv', 'test_output_chicago.csv',
                       'test_error_log_chicago.csv']
        for file_to_remove in remove_list:
            os.remove(file_to_remove)

        test_runner_info = [2017, 10, '30-34', 'M', 'Portland', 'OR', 'USA', 1, 1, 1]
        test_runner_info = [[cell] * 10 for cell in test_runner_info]
        test_split_times = [944, 1888, 2823, 3765, 3971, 4696, 5601, 6523, 7388, 7760]
        test_runner_dict = dict(zip(headers_chicago[:10], test_runner_info))
        expected_scraped_df = pd.DataFrame()
        expected_scraped_df['split'] = headers_chicago[10:]
        expected_scraped_df['time'] = test_split_times
        expected_scraped_df[headers_chicago[:10]] = pd.DataFrame.from_dict(test_runner_dict)
        expected_scraped_df = pd.pivot_table(expected_scraped_df, index=headers_chicago[:10], columns='split',
                                             values='time', aggfunc='first').reset_index()
        expected_scraped_df = expected_scraped_df.reindex(headers_chicago, axis='columns')

        scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                       expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_london_marathon(self):
        scraped_df_url = scrape.scrape_london_marathon_urls(url='http://results-2017.virginmoneylondonmarathon.com/2017/',
                                                            event='MAS', year=2017, gender='M', num_results_per_page=1000,
                                                            unit_test_ind=True)

        scrape.scrape_london_marathon(path_input='test_input_london.csv', path_output='test_output_london.csv',
                                      path_error='test_error_log_london.csv', year=2017, gender='M', headers=headers_london,
                                      df_urls=scraped_df_url)

        scraped_df = pd.read_csv('test_output_london.csv', header=0, sep='|')
        for split_time in headers_london[8:]:
            scraped_df[split_time] = scraped_df[split_time].astype('int64')

        remove_list = ['test_input_london.csv', 'test_output_london.csv',
                       'test_error_log_london.csv']
        for file_to_remove in remove_list:
            os.remove(file_to_remove)

        test_runner_info = [2017, 1154, '18-39', 'M', 'GBR', 1, 1, 1]
        test_runner_info = [[cell] * 10 for cell in test_runner_info]
        test_split_times = [948, 1899, 2848, 3799, 4000, 4742, 5698, 6670, 7653, 8089]
        test_runner_dict = dict(zip(headers_london[:8], test_runner_info))
        expected_scraped_df = pd.DataFrame()
        expected_scraped_df['split'] = headers_london[8:]
        expected_scraped_df['time'] = test_split_times
        expected_scraped_df[headers_london[:8]] = pd.DataFrame.from_dict(test_runner_dict)
        expected_scraped_df = pd.pivot_table(expected_scraped_df, index=headers_london[:8], columns='split', values='time',
                                             aggfunc='first').reset_index()
        expected_scraped_df = expected_scraped_df.reindex(headers_london, axis='columns')

        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)


    # noinspection PyTypeChecker
    def test_scrape_berlin_marathon(self):
        scraped_df_url = scrape.scrape_berlin_marathon_urls(url='http://results.scc-events.com/2016/',
                                                            event='MAL_99999905C9AF3F0000000945', year=2016, gender='M',
                                                            num_results_per_page=100, unit_test_ind=True)

        scrape.scrape_berlin_marathon(path_input='test_input_berlin.csv', path_output='test_output_berlin.csv',
                                      path_error='test_error_log_berlin.csv', year=2016, gender='M', headers=headers_berlin,
                                      df_urls=scraped_df_url)

        scraped_df = pd.read_csv('test_output_berlin.csv', header=0, sep='|')
        for split_time in headers_berlin[7:]:
            scraped_df[split_time] = scraped_df[split_time].astype('int64')

        remove_list = ['test_input_berlin.csv', 'test_output_berlin.csv',
                       'test_error_log_berlin.csv']
        for file_to_remove in remove_list:
            os.remove(file_to_remove)

        test_runner = [2016, 5, '30-34', 'M', 'ETH', 1, 1, 861, 1740, 2617, 3482, 3671, 4367, 5250, 6121, 7015, 7383]
        test_runner = [[cell] for cell in test_runner]
        test_runner_dict = dict(zip(headers_berlin, test_runner))
        expected_scraped_df = pd.DataFrame.from_dict(test_runner_dict)
        expected_scraped_df = expected_scraped_df.reindex(headers_berlin, axis='columns')

        assert scraped_df.equals(expected_scraped_df) and all(scraped_df.columns.values ==
                                                              expected_scraped_df.columns.values)
