C     SccsID = "$Id: claim.for 54954 2011-06-12 01:02:41Z Srinivas.Reddy $"  
        SUBROUTINE CLAIM

        COMMON/FILES/ITHREE,IFOUR,ITWO,ICON


        WRITE(3,100)

 100    FORMAT(1H1//////////T56,'EXPLANATION OF DATA'///
     &T35,'Elevations are referenced to NGVD 1929. They are considered'/
     & T35,'accurate to the nearest listed decimal. However if the'/
     & T35,'observations were obtained from GPS, then a combination'/
     & T35,'of the elevation accuracy and the geoid height accuracy'/
     & T35,'will mean that the elevations are accurate to 1 meter.'//
     & T35,'Geoid heights were obtained using RAPPS 180 X 180 model'/
     &T35,'and are considered accurate to the nearest meter in the an'/
     & T35,'absolute sense and relatively to the nearest decimeter.'//
     & T35,'Note that State Plane Coordinate System values for the'/
     & T35,'Northing (Y) and Easting (X) are given in meters in the'/
     & T35,'NAD 83 system.')


       RETURN
       END
