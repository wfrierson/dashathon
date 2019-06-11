[![Build Status](https://travis-ci.org/wfrierson/dashathon.svg?branch=master)](https://travis-ci.org/wfrierson/dashathon)

# Dashaton: a marathon training tool for runners

## Background
The participation rate in marathons is increasing year by year, rendering a huge market of runners preparing for them. The worldwide growth from 2008 to 2018 was +49.43%. Women are picking up faster than men with a growth of +56.83% while men’s participation rate has increased +46.91%. The Abbott World Marathon Majors is a championship-style competition for marathon runners that started in 2006. A points based competition founded on six major city marathon races, the series currently comprises annual races for the cities of Tokyo, Boston, London, Berlin, Chicago and New York City, with about a million dollars worth in prize money associated with it. This project is a dashboard intended to help runners train better for upcoming marathons, especially the ones in the Abbott World Marathon Majors.

## Team Members
* Edwin Mathew
* Hallie Ertman
* Ishna Kaul
* Will Frierson

## Software Dependencies

* Python 3.0 and above
* HTML
* Javascript
* Dash

## Directory Structure

* analysis : contains EDA for the project
* datathon : contains main files for data, data merging, data scraping, unit tests and building the dashboard
* doc : contains the functional and component specifications
* presentations : contains the presentations related to the project

## License Information


## Organization of the project

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
