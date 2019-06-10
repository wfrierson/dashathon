from dashathon.scraping.scraping_methods import scrape_berlin_marathon_urls
from dashathon.scraping.scraping_methods import scrape_berlin_marathon

headers_berlin = ['year', 'bib', 'age_group', 'gender', 'country', 'rank_gender', 'rank_age_group', '5k', '10k', '15k',
                  '20k', 'half', '25k', '30k', '35k', '40k', 'finish']

print('Scraping URLs: 2017 M')
berlin_marathon_urls_2017_M = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2017/', year=2017,
                                                          event='MAL', gender='M', num_results_per_page=100)
print('Scraping Split Times: 2017 M')
scrape_berlin_marathon(path_input='berlin_marathon_2017_M_urls.csv', path_output='berlin_marathon_2017_M.csv',
                       path_error='berlin_marathon_2017_M_error_log.csv', year=2017, gender='M', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2017_M)
print('Scraping URLs: 2017 W')
berlin_marathon_urls_2017_W = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2017/', year=2017,
                                                          event='MAL', gender='W', num_results_per_page=100)
print('Scraping Split Times: 2017 W')
scrape_berlin_marathon(path_input='berlin_marathon_2017_W_urls.csv', path_output='berlin_marathon_2017_W.csv',
                       path_error='berlin_marathon_2017_W_error_log.csv', year=2017, gender='W', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2017_W)
print('Scraping URLs: 2016 M')
berlin_marathon_urls_2016_M = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2016/', year=2016,
                                                          event='MAL_99999905C9AF3F0000000945', gender='M',
                                                          num_results_per_page=100)
print('Scraping Split Times: 2016 M')
scrape_berlin_marathon(path_input='berlin_marathon_2016_M_urls.csv', path_output='berlin_marathon_2016_M.csv',
                       path_error='berlin_marathon_2016_M_error_log.csv', year=2016, gender='M', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2016_M)
print('Scraping URLs: 2016 W')
berlin_marathon_urls_2016_W = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2016/', year=2016,
                                                          event='MAL_99999905C9AF3F0000000945', gender='W',
                                                          num_results_per_page=100)
print('Scraping Split Times: 2016 W')
scrape_berlin_marathon(path_input='berlin_marathon_2016_W_urls.csv', path_output='berlin_marathon_2016_W.csv',
                       path_error='berlin_marathon_2016_W_error_log.csv', year=2016, gender='W', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2016_W)
print('Scraping URLs: 2015 M')
berlin_marathon_urls_2015_M = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2015/', year=2015,
                                                          event='MAL', gender='M', num_results_per_page=100)
print('Scraping Split Times: 2015 M')
scrape_berlin_marathon(path_input='berlin_marathon_2015_M_urls.csv', path_output='berlin_marathon_2015_M.csv',
                       path_error='berlin_marathon_2015_M_error_log.csv', year=2015, gender='M', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2015_M)
print('Scraping URLs: 2015 W')
berlin_marathon_urls_2015_W = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2015/', year=2015,
                                                          event='MAL', gender='W', num_results_per_page=100)
print('Scraping Split Times: 2015 W')
scrape_berlin_marathon(path_input='berlin_marathon_2015_W_urls.csv', path_output='berlin_marathon_2015_W.csv',
                       path_error='berlin_marathon_2015_W_error_log.csv', year=2015, gender='W', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2015_W)
print('Scraping URLs: 2014 M')
berlin_marathon_urls_2014_M = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2014/', year=2014,
                                                          event='MAL', gender='M', num_results_per_page=100)
print('Scraping Split Times: 2014 M')
scrape_berlin_marathon(path_input='berlin_marathon_2014_M_urls.csv', path_output='berlin_marathon_2014_M.csv',
                       path_error='berlin_marathon_2014_M_error_log.csv', year=2014, gender='M', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2014_M)
print('Scraping URLs: 2014 W')
berlin_marathon_urls_2014_W = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2014/', year=2014,
                                                          event='MAL', gender='W', num_results_per_page=100)
print('Scraping Split Times: 2014 W')
scrape_berlin_marathon(path_input='berlin_marathon_2014_W_urls.csv', path_output='berlin_marathon_2014_W.csv',
                       path_error='berlin_marathon_2014_W_error_log.csv', year=2014, gender='W', headers=headers_berlin,
                       df_urls=berlin_marathon_urls_2014_W)
