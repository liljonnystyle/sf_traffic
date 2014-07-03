data science project studying San Francisco traffic trends

langugages used: Python, bash

python libraries used: mechanize, BeautifulSoup, datetime, pandas, numpy, matplotlib, os, sys


DATA:

-bus_data includes bus GPS data in SF (time, loc, heading, speed)

	https://data.sfgov.org/Transportation/Raw-AVL-GPS-data/5fk7-ivit

-uber_data includes 25,000 anonymized uber black car GPS data in SF (time, loc -- dates modified)

	http://www.infochimps.com/datasets/uber-anonymized-gps-logs

-street_data includes street shape files for SF streets

	https://data.sfgov.org/Geography/Streets-of-San-Francisco-Zipped-Shapefile-Format-/wbm8-ratb

-maybe also go get some weather records for dates from wunderground? topology data?

-ny taxi data?

	http://www.andresmh.com/nyctaxitrips/

-other sources?

	lyft? sidecar? cell phones? garmin/tomtom? clippercard tag on/off?


SCRIPTS:

-bus_scrape.py downloads data files

-bus_eda.ipynb: exploratory data analysis

-uber_eda.ipynb: exploratory data analysis


THINGS TO ANALYZE:

-compute speed, heading for uber data

-compute acceleration

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

-quantify aggressiveness?

-create metric for energy efficiency from topology? -- associate with driver/time/location

-can't infer anything driver-specific, data is too anonymized


Thinking out loud... how to normalize out traffic/routing?

Aggregate M-F data into 'weekday' data. Then group by hours into 24 chunks (or maybe 2 hr chunks?). Each chunk will inform the average traffic pattern at that time of the weekday (hopefully all or most streets are covered). Ultimately, every coordinate (and heading) in every chunk will have a set of features (i.e., speed, acceleration) or possibly a distribution of features.

Then for a given ride, divide their time series by the average features at that location (and heading) for the respective time chunk. Interpolation will be required to line up coordinates.

OR... integrate difference between rider time series and average time series? Maybe instead of time series, it should be distance, evaluated intersection to intersection? Seems difficult, but theoretically doable.
