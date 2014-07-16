C     SccsID = "$Id: hdpc.for 54960 2011-06-12 01:02:57Z Srinivas.Reddy $"  
      SUBROUTINE HDPC


       INTEGER*4 IPRT
       CHARACTER*8 TITLE,GNUM
       COMMON/FILES/I3,I4,I2,ICON
       COMMON/IPRINT/IPRT
       COMMON/TITLE/GNUM

        IF(IPRT.EQ.1) THEN
           WRITE(3,5) GNUM
    5      FORMAT('1',/,T50,'PRELIMINARY COORDINATE LISTING ',/ ,
     &             T59,'FOR ',A8,//)
        ELSEIF(IPRT.EQ.2) THEN
           WRITE(3,6) GNUM
    6      FORMAT('1',/,T54,'FINAL COORDINATE LISTING ',/,
     &             T60,'FOR ',A8,//)
        ELSE
           WRITE(3,7)
    7      FORMAT('1',/////)
        ENDIF

      WRITE(3,10)
   10 FORMAT(T54,'NATIONAL GEODETIC SURVEY',/,
     *       T58,'PC TO GP PROGRAM',T120,'VERSION 2.0',/,T61,
     *       '1983 DATUM',//,1X,' STATION NAME',T34,'NORTHING (Y)',
     *       T48,'EASTING(X)',T61,'LATITUDE',T78,'LONGITUDE',
     *       T91,'ZONE',T96,'CONVERGENCE',T109,'SCALE',T120,'ELEV',
     *       T128,'GEOID',/,T34,'METER',T48,'METER',T61,'(NORTH)',
     *       T78,'(WEST)',T97,'D',T100,'M',T104,'S',
     *       T109,'FACTOR',T120,'(M)',T128,'HT(M)',//)

      RETURN
      END
