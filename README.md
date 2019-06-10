[![Build Status](https://travis-ci.org/wfrierson/dashathon.svg?branch=master)](https://travis-ci.org/wfrierson/dashathon)

### Organization of the project

The project has the following structure:

```
dashathon/
  |- analysis
  |- dashathon/
     |- __init__.py
     |- dashboards/
        |- __init__.py
        |- ...
     |- data/
        |- combined_data/
        |- external_data/
           |- andreanr_nyc_results_2015.csv
           |- andreanr_nyc_results_2016.csv
           |- andreanr_nyc_results_2017.csv
           |- andreanr_nyc_results_2018.csv
           |- external_data_sources.txt
           |- llimllib_boston_results_2013.csv
           |- llimllib_boston_results_2014.csv
           |- rojour_boston_results_2015.csv
           |- rojour_boston_results_2016.csv
           |- rojour_boston_results_2017.csv
        |- scraped_data/
     |- merging/
        |- __init__.py
        |- merging_methods.py
     |- scraping/
        |- __init__.py
        |-merging_methods.py
        |-scrape_berlin_data.py
        |-scrape_chicago_data.py
        |-scrape_london_data.py
        |-scraping_methods
     |- tests/
        |- __init__.py
        |- test_delete_last_line.txt
        |- test_file.txt
        |- test_scraping_methods.py
        |- 
  |- doc/
     |- functional_specifications.md
  |- presentations/
     |- ...
  |- .travis.yml
  |- LICENSE
  |- README.md
  |- requirements.txt
  |- setup.py