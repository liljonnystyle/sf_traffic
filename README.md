data science project studying San Francisco traffic trends

langugages used: Python, bash

python libraries used: mechanize, BeautifulSoup, datetime, pandas, numpy, matplotlib, os, sys

DATA:
-bus_data includes bus GPS data in SF (time, loc, heading, speed)
	from https://data.sfgov.org/Transportation/Raw-AVL-GPS-data/5fk7-ivit
-uber_data includes 25,000 uber black car GPS data in SF (time, loc)
	from http://www.infochimps.com/datasets/uber-anonymized-gps-logs
-street_data includes street shape files for SF streets
	from https://data.sfgov.org/Geography/Streets-of-San-Francisco-Zipped-Shapefile-Format-/wbm8-ratb
-maybe also go get some weather records for overlapping dates?
	from wunderground?

SCRIPTS:
-bus_scrape.py downloads data files
-bus_eda.ipynb: exploratory data analysis
-uber_eda.ipynb: exploratory data analysis

THINGS TO ANALYZE:
-compute speed, heading for uber data
-speed vs time scatter
-x vs y scatter, color by speed, matrix for diff times
-scatter-hist (x vs y, speed vs time, r vs speed?)
-factor in heading
-cross-reference with bus schedules
-cross-reference with weather conditions
-infer traffic light scheduling?
-latency times, infer police stop?
-specific driver tendencies/behavior
-mean free path
-velocity autocorrelation
-bus-uber speed correlation
-radial distribution function (diff times/locs)
-...
