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
   * timestamps are generally four seconds apart
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
(found in code/load_data.py)
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

Fortunately I eventually found a 20+ year old code written in Fortran 77 which does this conversion! (Sidenote: the code's readme instructs to load it from a floppy.) This code can be found in the nad83 directory of this project repository. While using and interpretting this code was also non-trivial, it made the problem significantly easier and is a definitively robust solution.

##Building a "Street Graph" and a "Transition Graph"
(found in code/load_data.py)
While I have information on each street (intersection-to-intersection), I actually lack information on legal and illegal turns. Morever, to properly assess ETA's, intersections can not be translated as nodes (otherwise, they would have infinite speed through zero distance, or zero weight). So ultimately what I need is a "transition graph," which contains street edges and transition edges. I am defining transition edges as an abstract edge which connects two intersecting streets.

###Street Graph
First, to build the street graph, I simply take each street from my street data, and assemble directed edges (using networkx). Start and stop coordinates are checked against previously assigned nodes to establish connectivity of the graph. Meanwhile, I assume that the class code of the street signifies a speed limit, which I use in conjunction with the street length to compute an estimated edge weight (i.e., a default for time to traverse the edge).

It is important to note that during assembly of this graph (and the following graph), several dictionaries are stored which make information lookup possible later. Especially important is a coordinate lookup dictionary, which is keyed on two-digit-truncated coordinate tuples, and contains lists of street edges which fall in the vicinity of those coordinates. This makes searching for nearby streets much simpler later, as the search breadth is reduced dramatically.

###Transition Graph
To build a transition graph, each edge from the street graph above is first translated into a street edge. Although the transition edges are actually abstractions, it simplifies the assembly by giving them a physical representation. Concretely, every street edge is shortened; the shortened edge starts at 10% of the original edge and ends at 75% of the original edge. The asymmetrical shortening is a byproduct of a previous attempt to connect street edges while maintaining directionality. The current implementation does not depend on the actual coordinates of the shortened edges. After edges are shortened, they are reconnected through careful bookkeeping of original and updated node numbers.

The original edge weights from the Street Graph are translated directly over to this transition graph, despite the edge shortening. Recall that the transition edges are abstractions, so the street edges technically still should have the same length. The transition edges are given large weights (i.e., 1000 seconds) as default. This is done because the initial assumption is that all transitions are illegal, and will only be deemed legal if actual drivers are observed making that transition. For example, on Market Street, it is generally illegal to make left turns. This information is not given explicitly in my street data, so the model can only learn about legality through observation, which will come into play later.

##Projecting Drivers onto Streets
(found in code/project.py)
This step is quite possibly the most time-consuming, challenging, and rewarding part of the project. I need to project (or map) drivers onto streets so that I can associate speeds (actually times) with roads -- to get edge weights. Even with the pre-cleaning done on the Uber data previously, the raw data is still quite noisy.

Initially, I was mapping drivers in a two-step process: first find the nearest edge (from the street graph) and how far along they are on the street. Second, if they are within the first 10% or last 25% (recall the asymmetrical shortening), then associate them with a transition edge, otherwise associate them with a street edge. This actually did not work very well for a number of reasons:

1. Searching through the entire graph of street edges for all coordinates takes forever (I ran it overnight and it had not finished, so I'm not sure actually how long it would take). Even subsetting each search (with the coord_lookup dictionary described earlier), it still takes a long time.
2. Directionality on each street is unknown, and must be determined after mapping is completed.
3. Mapping is highly prone to noisiness, as consecutive points can be mapped incorrectly onto different streets.

I may even be forgetting one or two reasons. Eventually, I decided to leverage the connectivity of my network graph to accomplish the mapping. To do this, I search for an initial edge, as I had done previously, keeping in mind that it could be directionally incorrect (or worse, completely incorrect). I search one timestamp forward, subsetting my search to edges that are within two connection-radii. If none are found, I expand the search one radius at a time. Eventually I will resort to searching the "old-fashioned" way. If connections are established, they reinforce confidence in my mapping and direction. Moving forward in time, I will search one previous and one forward to adjust my mapping. If a connection is broken, then the search begins anew with a broad search. This implementation actually addresses all of the issues with the previous solution. It performs much faster, establishes directionality/connectivity between consecutive timestamps, and is fairly robust. While it is still prone to some noisiness, it is considerably more robust because it searches based on graph connectivity.

This process also allows me to clean up the data significantly. After mapping coordinates to streets, I can adjust coordinates by placing them exactly onto their respective streets. While I had originally intended to use a Kalman Filter to do this cleaning (or pre-cleaning), I have found that this method works very well and the Kalman Filter conversely makes things worse (at least in some cases). Perhaps in the future, I may revisit the Kalman Filter to see if the two methods can be employed synergistically.

##Clustering Driving Behaviors
(found in code/cluster.py)
My intention for this project was to find clusters of different driving behaviors. I had aspirations to engineer features such as mean/median/max velocities, velocity autocorrelation/fourier transform of velocity profile, mean free path, lane change frequency, quantified aggression, fuel/energy consumption, etc. Ultimately I decided to keep things simple because all these features are derived out of only two time-series (i.e., latitude and longitude) -- not to mention it would be virtually impossible to infer lane changes. While I have computed velocity and acceleration time-series, I really only ended up using the following features per driver:

 * Average Velocity (on surface streets only)
 * Average Acceleration (on surface streets only)
 * Average Deceleration (on surface streets only)
 * Mean Free Path as time (the average time spent moving in between pauses in traffic)

I feel that these four features would appropriately distinguish aggressive and passive drivers, and even simple features like maximum velocity, maximum acceleration, etc. would not add significant value.

Prior to clustering, I divided the data into three time-categories: morning rush hour, afternoon rush hour, and other. Some drivers who straddle the rush hour/non-rush hour cutoff were aggregated into category which they are predominantly in.

For clustering, I did a pre-analysis with hierarchical clustering. I found that visually, there were potentially three to four clusters per time-category, however the dendrogram pruning would be very case-specific and non-trivial. Specifically, clusters would be pruned at different cluster sizes. Not only did this over-complicate the problem, I also realized that some clusters would be so small that coverage in the city would be quite sparse. Therefore, I ultimately decided to use K-Means clustering with two clusters for each time-category.

##Computing Edge Weights for Each Cluster
(found in code/cluster_graphs.py)
If you recall, in the projection implementation, I had only mapped drivers onto street edges, and not onto transition edges. Here, it becomes evident why projection onto transition edges is unnecessary. Recall again that transition edges are abstractions, so mapping a driver onto an abstract edge would be fruitless.

Moreover, this becomes important when computing edge weights for the transition graph. My original plan (when transition edges were physical segments of the street/intersection) was to associate driver velocities at each time stamp with the associated edge that they were currently on. Due to the transition edges being so short, it would be very rare to find a driver actually on a transition edge (unless they were stopped at the intersection). This would result in extremely long wait times at every intersection, even when intersections don't have a traffic light or stop sign (recall that the default weight is 1000 seconds -- so if it is not overwritten by any observations, the default will remain).

Another problem is that a car may not physically be located at the intersection while they are waiting for a light to change. If traffic is backed up for half the block, the car would be sitting in the "street edge" portion and the wait time would be associated incorrectly.

After much deliberation, I decided that the velocity on the street edge should determine how each timestamp should be associated. Any zero velocity should be associated with the upcoming transition edge, and any finite velocity should be associated with the street edge. Note that each street edge has approximately three upcoming transition edges (left turn, straight, right turn). Therefore, the wait time can only be associated to a transition edge if the next consecutive street edge is known.

Also note that the weights are in units of time. They should not be based on mean velocities. See for example:

<t> = (t_1 + t_2 + t_3) / 3
	!= L / ((v_1 + v_2 + v_3) / 3)

It would also be unnecessary to compute the mean of the inverse-velocities because the time is actually right in front of us. Since I have timestamps (spaced four seconds apart), all I need to do is count the number of finite and zero velocity timestamps (on a particular edge) and multiply by four seconds.

In hindsight, it was discovered that some transition edges are not explored by some clusters due to sparseness of data. This results in the default weights, which makes ETA predictions extremely long. As a fix for this problem, the whole dataset is used to pre-compute updated default edge weights. This propogates knowledge of turn-legality and approximate wait times to all clusters. So this step is inserted prior to computing edge weights for each cluster.

##Web App
(found in app/*)
