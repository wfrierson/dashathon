from .scraping_methods import scrape_chicago_marathon_urls
from .scraping_methods import scrape_chicago_marathon

headers_chicago = ['year', 'bib', 'age_group', 'gender', 'city', 'state', 'country', 'overall', 'rank_gender',
                   'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']

print('Scraping URLs: 2017 M')
chicago_marathon_urls_2017_M = scrape_chicago_marathon_urls(year=2017,
                                                            event='MAR_999999107FA30900000000A1', gender='M',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2017 M')
scrape_chicago_marathon(path_input='chicago_marathon_2017_M_urls.csv', path_output='chicago_marathon_2017_M.csv',
                        path_error='chicago_marathon_2017_M_error_log.csv', gender='M', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2017_M)

print('Scraping URLs: 2017 W')
chicago_marathon_urls_2017_W = scrape_chicago_marathon_urls(year=2017,
                                                            event='MAR_999999107FA30900000000A1', gender='W',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2017 W')
scrape_chicago_marathon(path_input='chicago_marathon_2017_W_urls.csv', path_output='chicago_marathon_2017_W.csv',
                        path_error='chicago_marathon_2017_W_error_log.csv', gender='W', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2017_W)

print('Scraping URLs: 2016 M')
chicago_marathon_urls_2016_M = scrape_chicago_marathon_urls(year=2016,
                                                            event='MAR_999999107FA309000000008D', gender='M',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2016 M')
scrape_chicago_marathon(path_input='chicago_marathon_2016_M_urls.csv', path_output='chicago_marathon_2016_M.csv',
                        path_error='chicago_marathon_2016_M_error_log.csv', gender='M', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2016_M)

print('Scraping URLs: 2016 W')
chicago_marathon_urls_2016_W = scrape_chicago_marathon_urls(year=2016,
                                                            event='MAR_999999107FA309000000008D', gender='W',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2016 W')
scrape_chicago_marathon(path_input='chicago_marathon_2016_W_urls.csv', path_output='chicago_marathon_2016_W.csv',
                        path_error='chicago_marathon_2016_W_error_log.csv', gender='W', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2016_W)

print('Scraping URLs: 2015 M')
chicago_marathon_urls_2015_M = scrape_chicago_marathon_urls(year=2015,
                                                            event='MAR_999999107FA3090000000079', gender='M',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2015 M')
scrape_chicago_marathon(path_input='chicago_marathon_2015_M_urls.csv', path_output='chicago_marathon_2015_M.csv',
                        path_error='chicago_marathon_2015_M_error_log.csv', gender='M', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2015_M)

print('Scraping URLs: 2015 W')
chicago_marathon_urls_2015_W = scrape_chicago_marathon_urls(year=2015,
                                                            event='MAR_999999107FA3090000000079', gender='W',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2015 W')
scrape_chicago_marathon(path_input='chicago_marathon_2015_W_urls.csv', path_output='chicago_marathon_2015_W.csv',
                        path_error='chicago_marathon_2015_W_error_log.csv', gender='W', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2015_W)

print('Scraping URLs: 2014 M')
chicago_marathon_urls_2014_M = scrape_chicago_marathon_urls(year=2014,
                                                            event='MAR_999999107FA3090000000065', gender='M',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2014 M')
scrape_chicago_marathon(path_input='chicago_marathon_2014_M_urls.csv', path_output='chicago_marathon_2014_M.csv',
                        path_error='chicago_marathon_2014_M_error_log.csv', gender='M', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2014_M)

print('Scraping URLs: 2014 W')
chicago_marathon_urls_2014_W = scrape_chicago_marathon_urls(year=2014,
                                                            event='MAR_999999107FA3090000000065', gender='W',
                                                            num_results_per_page=1000)
print('Scraping Split Times: 2014 W')
scrape_chicago_marathon(path_input='chicago_marathon_2014_W_urls.csv', path_output='chicago_marathon_2014_W.csv',
                        path_error='chicago_marathon_2014_W_error_log.csv', gender='W', headers=headers_chicago,
                        df_urls=chicago_marathon_urls_2014_W)
