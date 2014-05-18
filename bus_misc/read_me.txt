NOTES about raw AVL data

-All data are be sorted by date, vehicle and time.

-The TRAIN_ASSIGNMENT field is used to determine the block/train to which the vehicle has been assigned (see the attached terminology sheet for more info about trains/blocks)

-The IS_PREDICTABLE field is a quality code and indicates if the Next Bus sytem is able to accurately make prediction about the vehicle at the time the GPS data was recorded.

-The LAST_TIMEPOINT field can be linked to field STOPID GTFS data found at --&gt; http://www.sfmta.com/cms/asite/labsindx.htm.  
	Some Values in field LAST_TIMEPOINT may be prepended with an extra digit causing them to be five digits long.  
	These instances should be shorted (by removing the leading number) to four digits if you wish to link them to the schedule data.

NOTE:  	The LAST_TIMEPOINT field is updated every time a vehicle passes a time point.  
	There may be a few cases where this field is updated slightly before the vehicle passes a time point (up to 5 seconds).



LInking Data to the SFMTA Schedule:
	To link the raw AVL data to a schedule you will need to use (1) the GTFS data at --&gt; http://www.sfmta.com/cms/asite/labsindx.htm, (2) file "lookUpSignUpPeriods.csv" and (3) file "lookUpBlockIDToBlockNumNam.csv".
	File "lookUpBlockIDToBlockNumNam.csv" will allow you to link the block/train numbers in field "TRAIN_ASSIGNMENT" to field "block_id" in file "trips.txt" of the GTFS dataset.
	File "lookUpSignUpPeriods.csv" gives the dates for which each signup ID is valid.



FIRST valid line will be

VEHICLE_TAG,REPORT_TIME,LONGITUDE,LATITUDE,TRAIN_ASSIGNMENT,IS_PREDICTABLE,LAST_TIMEPOINT



  
SAMPLE data

SQL&gt; /
VEHICLE_TAG,REPORT_TIME,LONGITUDE,LATITUDE,TRAIN_ASSIGNMENT,IS_PREDICTABLE,LAST_TIMEPOINT                                                             
1416,04-APR-12 12.01.19 AM,-122.38406,37.7514,9711,0,                                                                                                 
1416,04-APR-12 12.02.49 AM,-122.38406,37.75143,9711,0,                                                                                                
1416,04-APR-12 12.04.19 AM,-122.38407,37.75141,9711,0,                                                                                                
1416,04-APR-12 12.05.49 AM,-122.38409,37.7514,9711,0,
7010,10-APR-12 05.54.48 AM,-122.42371,37.73981,1413,1,                                                                                                
7010,10-APR-12 05.55.19 AM,-122.42408,37.73803,1413,1,                                                                                                
7010,10-APR-12 05.55.46 AM,-122.42446,37.73633,1413,1,                                                                                                
7010,10-APR-12 05.56.22 AM,-122.42542,37.73475,1413,1,                                                                                                
7010,10-APR-12 05.57.00 AM,-122.42678,37.7334,1413,1,                                                                                                 
7010,10-APR-12 05.57.17 AM,-122.42815,37.73201,1413,1,                                                                                                
7010,10-APR-12 05.57.32 AM,-122.4295,37.73065,1413,1,                                                                                                 
7010,10-APR-12 05.57.55 AM,-122.43086,37.72926,1413,1,                                                                                                
7010,10-APR-12 05.58.27 AM,-122.43224,37.72791,1413,1,5621                                                                                            
7010,10-APR-12 05.58.48 AM,-122.43293,37.72728,1413,1,5621                                                                                            
7010,10-APR-12 05.59.20 AM,-122.43351,37.72651,1413,1,5621                                                                                            
7010,10-APR-12 06.00.17 AM,-122.43464,37.725,1413,1,5621                                                                                              
7010,10-APR-12 06.01.26 AM,-122.43578,37.72351,1413,1,5621                                                                                            
7010,10-APR-12 06.01.48 AM,-122.43594,37.7233,1413,1,5621                                                                                             
7010,10-APR-12 06.02.38 AM,-122.43692,37.72198,1413,1,5621                                                                                            
7010,10-APR-12 06.02.56 AM,-122.43805,37.7205,1413,1,5621  