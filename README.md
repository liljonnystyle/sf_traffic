#ZipLee: A vehicular routing app for specific driving behaviors

This is a data science project intended to study San Francisco traffic trends. In its final form, it has become a web app designed to aid users in finding optimal routes through San Francisco for their specific driving behaviors.

langugages used:
 * python
 * bash
 * javascript
 * fortran77

python libraries used:
 * numpy
 * scipy
 * pandas
 * datetime
 * networkx
 * json
 * pickle
 * math
 * matplotlib
 * collections
 * sklearn
 * pygeocoder
 * flask
 * requests
 * ipdb

data sources:
 * uber_data
	-includes 25,000 anonymized uber black car GPS data in SF
	-ride id, timestamps, latitude, and longitude
	-rides are anonymized by truncating beginning and end of each ride, as well as modifying the original date; day of week is still preserved
	-repeated datapoints are removed
	-see: http://www.infochimps.com/datasets/uber-anonymized-gps-logs

 * street_data
	-includes street shape files for SF streets
	-each entry contains a street, defined from intersection to consecutive intersection, with one-way and class specified
	-see: https://data.sfgov.org/Geography/Streets-of-San-Francisco-Zipped-Shapefile-Format-/wbm8-ratb

##General Approach

My goal is to build a routing algorithm specific to driver behaviors. To do this, I need to build a network graph of streets, and populate edge weights using (clustered) driver data. So there are essentially two main challenges I am facing. The first is clustering drivers by behavior, and the second is building network graphs based on each of those clusters. While these tasks may seem like a sequential two-step process, in reality, there are many moving parts and the tasks actually intermingle quite a bit. Hopefully I can illuminate most of the process here.

##Loading Data

###Uber Data
The first step, of course, is to load in the data. The Uber data loads in quite simply enough, as it is just a tsv file. The data can be read in with pandas, and simple cleaning is done. This includes:

 * subsetting strictly to the city of San Francisco proper
 * removing rides with less than four datapoints
 * filling in missing values (with the assumption that they are repeated/stationary points that were removed by Uber in post-processing)
 * computing speed and acceleration, and removing any rides that contain physically impossible/improbable speeds and accelerations

While there may be smarter ways to deal with the impossible/improbable data than throwing out the entire ride, I ultimately decided on this due to the complex nature of the future steps and my time constraint.

###Street Data
Loading the street data was quite a bit more involved. The initial form was in a shape file. Using ogr2ogr, I was able to convert into a json, which reads well into python. One or two other methods to read the data directly into python were attempted, but ogr2ogr provided the most straightforward solution.

With the json loaded, specific keys are grabbed to populate a DataFrame in python, namely street name, one way flag, class code, start coordinates, and stop coordinates. The coordinates then provided a very significant challenge, as they were not in the usual latitude/longitude projection system or the standard Mercator system. Ultimately I found that they are recorded in the US State Plane Coordinate System, NAD 83, Zone 3, US Survey Feet. The State Plane Coordinate System contains 128 zones for the entire United States. Each zone is measured in feet (typically in meters) using simple 2D Cartesian space from some arbitrary location. Essentially, this makes conversion into degree-based latitude/longitude very non-trivial.

My first pass involved trying to align the map visually as well as via triangulation. In hindsight, this was obviously fruitless because the two projection systems will never match perfectly. Especially with a map the size of a city, errors are quite obvious at the boundaries.

My second try was to cross-reference google maps API to find coordinates of all street intersections. Not only did this quickly blow out my daily request limit, there were maybe hundreds of drastically misplaced intersections, I had to abandon this routine.

Fortunately I eventually found a 20+ year old code written in Fortran 77 which does this conversion! This code can be found in the nad83 directory of this project repository. While using and interpretting this code was also non-trivial, it made the problem significantly easier and is a definitively robust solution.

##Building a "Street Graph" and a "Transition Graph"

