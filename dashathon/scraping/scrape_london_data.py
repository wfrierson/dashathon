from .scraping_methods import scrape_london_marathon_urls
from .scraping_methods import scrape_london_marathon

headers_london = ['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender',
                  'rank_age_group', '5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']

print('Scraping URLs: 2017 M')
london_marathon_urls_2017_M = scrape_london_marathon_urls(url='http://results-2017.virginmoneylondonmarathon.com/2017/',
                                                          year=2017, event='MAS', gender='M', num_results_per_page=1000)
london_marathon_urls_2017_M_elite = scrape_london_marathon_urls(url=('http://results-2017.virginmoneylondonmarathon.com'
                                                                     '/2017/'), year=2017, event='ELIT', gender='M',
                                                                num_results_per_page=1000)

print('Scraping Split Times: 2017 M')
scrape_london_marathon(path_input='london_marathon_2017_M_urls.csv', path_output='london_marathon_2017_M.csv',
                       path_error='london_marathon_2017_M_error_log.csv', year=2017, gender='M', headers=headers_london,
                       df_urls=london_marathon_urls_2017_M)
scrape_london_marathon(path_input='london_marathon_2017_M_elite_urls.csv',
                       path_output='london_marathon_2017_M_elite.csv',
                       path_error='london_marathon_2017_M_elite_error_log.csv', year=2017, gender='M',
                       headers=headers_london, df_urls=london_marathon_urls_2017_M_elite)

print('Scraping URLs: 2017 W')
london_marathon_urls_2017_W = scrape_london_marathon_urls(url='http://results-2017.virginmoneylondonmarathon.com/2017/',
                                                          year=2017, event='MAS', gender='W', num_results_per_page=1000)
london_marathon_urls_2017_W_elite = scrape_london_marathon_urls(url=('http://results-2017.virginmoneylondonmarathon.com'
                                                                     '/2017/'), year=2017, event='ELIT', gender='W',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2017 W')
scrape_london_marathon(path_input='london_marathon_2017_W_urls.csv', path_output='london_marathon_2017_W.csv',
                       path_error='london_marathon_2017_W_error_log.csv', year=2017, gender='W', headers=headers_london,
                       df_urls=london_marathon_urls_2017_W)
scrape_london_marathon(path_input='london_marathon_2017_W_elite_urls.csv',
                       path_output='london_marathon_2017_W_elite.csv',
                       path_error='london_marathon_2017_W_elite_error_log.csv', year=2017, gender='W',
                       headers=headers_london, df_urls=london_marathon_urls_2017_W_elite)

print('Scraping URLs: 2016 M')
london_marathon_urls_2016_M = scrape_london_marathon_urls(url='http://results-2016.virginmoneylondonmarathon.com/2016/',
                                                          year=2016, event='MAS', gender='M', num_results_per_page=1000)
london_marathon_urls_2016_M_elite = scrape_london_marathon_urls(url=('http://results-2016.virginmoneylondonmarathon.com'
                                                                     '/2016/'), year=2016, event='ELIT', gender='M',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2016 M')
scrape_london_marathon(path_input='london_marathon_2016_M_urls.csv', path_output='london_marathon_2016_M.csv',
                       path_error='london_marathon_2016_M_error_log.csv', year=2016, gender='M', headers=headers_london,
                       df_urls=london_marathon_urls_2016_M)
scrape_london_marathon(path_input='london_marathon_2016_M_elite_urls.csv',
                       path_output='london_marathon_2016_M_elite.csv',
                       path_error='london_marathon_2016_M_elite_error_log.csv', year=2016, gender='M',
                       headers=headers_london, df_urls=london_marathon_urls_2016_M_elite)

print('Scraping URLs: 2016 W')
london_marathon_urls_2016_W = scrape_london_marathon_urls(url='http://results-2016.virginmoneylondonmarathon.com/2016/',
                                                          year=2016, event='MAS', gender='W', num_results_per_page=1000)
london_marathon_urls_2016_W_elite = scrape_london_marathon_urls(url=('http://results-2016.virginmoneylondonmarathon.com'
                                                                     '/2016/'), year=2016, event='ELIT', gender='W',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2016 W')
scrape_london_marathon(path_input='london_marathon_2016_W_urls.csv', path_output='london_marathon_2016_W.csv',
                       path_error='london_marathon_2016_W_error_log.csv', year=2016, gender='W', headers=headers_london,
                       df_urls=london_marathon_urls_2016_W)
scrape_london_marathon(path_input='london_marathon_2016_W_elite_urls.csv',
                       path_output='london_marathon_2016_W_elite.csv',
                       path_error='london_marathon_2016_W_elite_error_log.csv', year=2016, gender='W',
                       headers=headers_london, df_urls=london_marathon_urls_2016_W_elite)

print('Scraping URLs: 2015 M')
london_marathon_urls_2015_M = scrape_london_marathon_urls(url='http://results-2015.virginmoneylondonmarathon.com/2015/',
                                                          year=2015, event='MAS', gender='M', num_results_per_page=1000)
london_marathon_urls_2015_M_elite = scrape_london_marathon_urls(url=('http://results-2015.virginmoneylondonmarathon.com'
                                                                     '/2015/'), year=2015, event='ELIT', gender='M',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2015 M')
scrape_london_marathon(path_input='london_marathon_2015_M_urls.csv', path_output='london_marathon_2015_M.csv',
                       path_error='london_marathon_2015_M_error_log.csv', year=2015, gender='M', headers=headers_london,
                       df_urls=london_marathon_urls_2015_M)
scrape_london_marathon(path_input='london_marathon_2015_M_elite_urls.csv',
                       path_output='london_marathon_2015_M_elite.csv',
                       path_error='london_marathon_2015_M_elite_error_log.csv', year=2015, gender='M',
                       headers=headers_london, df_urls=london_marathon_urls_2015_M_elite)

print('Scraping URLs: 2015 W')
london_marathon_urls_2015_W = scrape_london_marathon_urls(url='http://results-2015.virginmoneylondonmarathon.com/2015/',
                                                          year=2015, event='MAS', gender='W', num_results_per_page=1000)
london_marathon_urls_2015_W_elite = scrape_london_marathon_urls(url=('http://results-2015.virginmoneylondonmarathon.com'
                                                                     '/2015/'), year=2015, event='ELIT', gender='W',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2015 W')
scrape_london_marathon(path_input='london_marathon_2015_W_urls.csv', path_output='london_marathon_2015_W.csv',
                       path_error='london_marathon_2015_W_error_log.csv', year=2015, gender='W', headers=headers_london,
                       df_urls=london_marathon_urls_2015_W)
scrape_london_marathon(path_input='london_marathon_2015_W_elite_urls.csv',
                       path_output='london_marathon_2015_W_elite.csv',
                       path_error='london_marathon_2015_W_elite_error_log.csv', year=2015, gender='W',
                       headers=headers_london, df_urls=london_marathon_urls_2015_W_elite)

print('Scraping URLs: 2014 M')
london_marathon_urls_2014_M = scrape_london_marathon_urls(url='http://results-2014.virginmoneylondonmarathon.com/2014/',
                                                          year=2014, event='MAS', gender='M', num_results_per_page=1000)
london_marathon_urls_2014_M_elite = scrape_london_marathon_urls(url=('http://results-2014.virginmoneylondonmarathon.com'
                                                                     '/2014/'), year=2014, event='ELIT', gender='M',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2014 M')
scrape_london_marathon(path_input='london_marathon_2014_M_urls.csv', path_output='london_marathon_2014_M.csv',
                       path_error='london_marathon_2014_M_error_log.csv', year=2014, gender='M', headers=headers_london,
                       df_urls=london_marathon_urls_2014_M)
scrape_london_marathon(path_input='london_marathon_2014_M_elite_urls.csv',
                       path_output='london_marathon_2014_M_elite.csv',
                       path_error='london_marathon_2014_M_elite_error_log.csv', year=2014, gender='M',
                       headers=headers_london, df_urls=london_marathon_urls_2014_M_elite)

print('Scraping URLs: 2014 W')
london_marathon_urls_2014_W = scrape_london_marathon_urls(url='http://results-2014.virginmoneylondonmarathon.com/2014/',
                                                          year=2014, event='MAS', gender='W', num_results_per_page=1000)
london_marathon_urls_2014_W_elite = scrape_london_marathon_urls(url=('http://results-2014.virginmoneylondonmarathon.com'
                                                                     '/2014/'), year=2014, event='ELIT', gender='W',
                                                                num_results_per_page=1000)
print('Scraping Split Times: 2014 W')
scrape_london_marathon(path_input='london_marathon_2014_W_urls.csv', path_output='london_marathon_2014_W.csv',
                       path_error='london_marathon_2014_W_error_log.csv', year=2014, gender='W', headers=headers_london,
                       df_urls=london_marathon_urls_2014_W)
scrape_london_marathon(path_input='london_marathon_2014_W_elite_urls.csv',
                       path_output='london_marathon_2014_W_elite.csv',
                       path_error='london_marathon_2014_W_elite_error_log.csv', year=2014, gender='W',
                       headers=headers_london, df_urls=london_marathon_urls_2014_W_elite)
