[![Build Status](https://travis-ci.org/wfrierson/dashathon.svg?branch=master)](https://travis-ci.org/wfrierson/dashathon) [![Coverage Status](https://coveralls.io/repos/github/wfrierson/dashathon/badge.svg?branch=master)](https://coveralls.io/github/wfrierson/dashathon?branch=master) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](/LICENSE) ![contributors](https://img.shields.io/github/contributors/wfrierson/dashathon.svg) ![codesize](https://img.shields.io/github/languages/code-size/wfrierson/dashathon.svg)

# Dashathon: a marathon training tool for runners

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
The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). As a permissive license, it puts only very limited restriction on reuse and has therefore an excellent license compatibility. For detailed description of the contents of license please refer to the file LICENSE.

## Getting the dashboard
* Install dependencies (listed in the requirements file)
* Clone the repo
* Run the app_final.py in dashathon/dashboard

## Organization of the project

The project has the following structure:

```
dashathon/
│-  .gitignore
│-  .travis.yml
│-  dashathon_layout.txt
│-  dashathon_layout_cmd.txt
│-  LICENSE
│-  README.md
│-  requirements.txt
│-  setup.py
│   
├───analysis/
│   │-  app4.py
│   │-  app_pylint_checked.py
│   │-  app_split_ratio.py
│   │-  boston_all_years_nan.csv
│   │-  data_agg.csv
│   │-  EDA.R
│   │-  Project EDA.ipynb
│           
├───dashathon/
│   │-  __init__.py
│   │   
│   ├───dashboard/
│   │   │-  app_final.py
│   │   │-  dash_functions.py
│   │   │-  __init__.py
│   │    
│   ├───data/
│   │   ├───combined_data/
│   │   │-      all_marathon_results.csv
│   │   │-      berlin_marathon_results_2014_2017.csv
│   │   │-      boston_marathon_results_2013_2017.csv
│   │   │-      chicago_marathon_results_2014_2017.csv
│   │   │-      london_marathon_results_2014_2017.csv
│   │   │-      nyc_marathon_results_2015_2018.csv
│   │   │       
│   │   ├───external_data/
│   │   │-      andreanr_nyc_results_2015.csv
│   │   │-      andreanr_nyc_results_2016.csv
│   │   │-      andreanr_nyc_results_2017.csv
│   │   │-      andreanr_nyc_results_2018.csv
│   │   │-      external_data_sources.txt
│   │   │-      llimllib_boston_results_2013.csv
│   │   │-      llimllib_boston_results_2014.csv
│   │   │-      rojour_boston_results_2015.csv
│   │   │-      rojour_boston_results_2016.csv
│   │   │-      rojour_boston_results_2017.csv
│   │   │       
│   │   ├───scraped_data/
│   │   │-      berlin_marathon_2014_M.csv
│   │   │-      berlin_marathon_2014_W.csv
│   │   │-      berlin_marathon_2015_M.csv
│   │   │-      berlin_marathon_2015_W.csv
│   │   │-      berlin_marathon_2016_M.csv
│   │   │-      berlin_marathon_2016_W.csv
│   │   │-      berlin_marathon_2017_M.csv
│   │   │-      berlin_marathon_2017_W.csv
│   │   │-      chicago_marathon_2014_M.csv
│   │   │-      chicago_marathon_2014_W.csv
│   │   │-      chicago_marathon_2015_M.csv
│   │   │-      chicago_marathon_2015_W.csv
│   │   │-      chicago_marathon_2016_M.csv
│   │   │-      chicago_marathon_2016_W.csv
│   │   │-      chicago_marathon_2017_M.csv
│   │   │-      chicago_marathon_2017_W.csv
│   │   │-      london_marathon_2014_M.csv
│   │   │-      london_marathon_2014_M_elite.csv
│   │   │-      london_marathon_2014_W.csv
│   │   │-      london_marathon_2014_W_elite.csv
│   │   │-      london_marathon_2015_M.csv
│   │   │-      london_marathon_2015_M_elite.csv
│   │   │-      london_marathon_2015_W.csv
│   │   │-      london_marathon_2015_W_elite.csv
│   │   │-      london_marathon_2016_M.csv
│   │   │-      london_marathon_2016_M_elite.csv
│   │   │-      london_marathon_2016_W.csv
│   │   │-      london_marathon_2016_W_elite.csv
│   │   │-      london_marathon_2017_M.csv
│   │   │-      london_marathon_2017_M_elite.csv
│   │   │-      london_marathon_2017_W.csv
│   │   │-      london_marathon_2017_W_elite.csv
│   │           
│   ├───merging/
│   │-      age_map.csv
│   │-      country_code_web.csv
│   │-      export_processed_data.py
│   │-      merging_methods.py
│   │-      __init__.py
│   │
│   ├───scraping/
│   │-      scrape_berlin_data.py
│   │-      scrape_chicago_data.py
│   │-      scrape_london_data.py
│   │-      scraping_methods.py
│   │-      __init__.py
│   │       
│   ├───tests/
│   │-      test_dash_functions.py
│   │-      test_delete_last_line.txt
│   │-      test_file.txt
│   │-      test_merging_methods.py
│   │-      test_scraping_methods.py
│   │-      __init__.py
│   
├───doc/
│-      component_specifications.md
│-      functional_specifications.md
│       
├───presentations/
│-      Project Summary Presentation 1.pdf
│-      Technology Review.pptx

