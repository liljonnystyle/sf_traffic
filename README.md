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
   * includes 25,000 anonymized uber black car GPS data in SF
   * ride id, timestamps, latitude, and longitude
   * rides are anonymized by truncating beginning and end of each ride, as well as modifying the original date; day of week is still preserved
   * repeated datapoints are removed
   * see: http://www.infochimps.com/datasets/uber-anonymized-gps-logs

 * street_data
   * includes street shape files for SF streets
   * each entry contains a street, defined from intersection to consecutive intersection, with one-way and class specified
   * see: https://data.sfgov.org/Geography/Streets-of-San-Francisco-Zipped-Shapefile-Format-/wbm8-ratb

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
While I have information on each street (intersection-to-intersection), I actually lack information on legal and illegal turns. Morever, to properly assess ETA's, intersections can not be translated as nodes (otherwise, they would have infinite speed through zero distance, or zero weight). So ultimately what I need is a "transition graph," which contains street edges and transition edges. I am defining transition edges as an abstract edge which connects two intersecting streets.

###Street Graph
First, to build the street graph, I simply take each street from my street data, and assemble directed edges (using networkx). Start and stop coordinates are checked against previously assigned nodes to establish connectivity of the graph. Meanwhile, I assume that the class code of the street signifies a speed limit, which I use in conjunction with the street length to compute an estimated edge weight (i.e., a default for time to traverse the edge).

It is important to note that during assembly of this graph (and the following graph), several dictionaries are stored which make information lookup possible later. Especially important is a coordinate lookup dictionary, which is keyed on two-digit-truncated coordinate tuples, and contains lists of street edges which fall in the vicinity of those coordinates. This makes searching for nearby streets much simpler later, as the search breadth is reduced dramatically.

###Transition Graph
To build a transition graph, each edge from the street graph above is first translated into a street edge. Although the transition edges are actually abstractions, it simplifies the assembly by giving them a physical representation. Concretely, every street edge is shortened; the shortened edge starts at 10% of the original edge and ends at 75% of the original edge. The asymmetrical shortening is a byproduct of a previous attempt to connect street edges while maintaining directionality. The current implementation does not depend on the actual coordinates of the shortened edges. After edges are shortened, they are reconnected through careful bookkeeping of original and updated node numbers.

The original edge weights from the Street Graph are translated directly over to this transition graph, despite the edge shortening. Recall that the transition edges are abstractions, so the street edges technically still should have the same length. The transition edges are given large weights (i.e., 1000 seconds) as default. This is done because the initial assumption is that all transitions are illegal, and will only be deemed legal if actual drivers are observed making that transition. For example, on Market Street, it is generally illegal to make left turns. This information is not given explicitly in my street data, so the model can only learn about legality through observation, which will come into play later.

##Projecting Drivers onto Streets

##Clustering Driving Behaviors

##Computing Edge Weights for Each Cluster

##Web App
