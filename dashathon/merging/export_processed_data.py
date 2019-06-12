import pandas as pd
import dashathon.merging.merging_methods as merge

# Process all marathon results
boston_results = merge.process_boston_data()
nyc_results = merge.process_nyc_data()
chicago_results = merge.process_chicago_data()
london_results = merge.process_london_data()
berlin_results = merge.process_berlin_data()
dashathon_data = merge.process_all_data()

# Export processed marathon results
boston_results.to_csv('../data/combined_data/boston_marathon_results_2013_2017.csv', index=False)
nyc_results.to_csv('../data/combined_data/nyc_marathon_results_2015_2018.csv', index=False)
chicago_results.to_csv('../data/combined_data/chicago_marathon_results_2014_2017.csv', index=False)
london_results.to_csv('../data/combined_data/london_marathon_results_2014_2017.csv', index=False)
berlin_results.to_csv('../data/combined_data/berlin_marathon_results_2014_2017.csv', index=False)
dashathon_data.to_csv('../data/combined_data/all_marathon_results.csv', index=False)
