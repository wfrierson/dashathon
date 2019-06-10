### Organization of the project

The project has the following structure:

```
dashathon/
  |- README.md
  |- analysis
  |- dashathon/
     |- dashboards/
     |- data/
		|- combined_data/
		|- external_data/
		|- scraped_data/
     |- scraping/
        |-merging_methods.py
        |-scrape_berlin_data.py
        |-scrape_chicago_data.py
        |-scrape_london_data.py
        |-scraping_methods
     |- tests/
        |- ...
  |- doc/
     |- ...
  |- setup.py
  |- LICENSE
  |- requirements.txt