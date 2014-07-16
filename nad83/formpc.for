C     SccsID = "$Id: formpc.for 54958 2011-06-12 01:02:52Z Srinivas.Reddy $"  
      SUBROUTINE FORMPC(CARDR,LAT,LON,FILFLAG,J,FILPRT,ZONE,CONV,KP)
      IMPLICIT REAL*8 (A-H,O-Z)

      LOGICAL FILFLAG,FILPRT

      REAL*8 NORTH,KP,LAT,LON

      CHARACTER*2 AD1,AM1,AM2
      CHARACTER*3 AD2
      CHARACTER*7 AS1,AS2
      CHARACTER*1 ADIR1,ADIR2
      CHARACTER*4 ZONE
      CHARACTER*30 NAME
      CHARACTER*80 CARDR
      CHARACTER*5 XGD,GDVAL
      CHARACTER*1 PM,ESGN,GSGN
      CHARACTER*1 ELEVT
      CHARACTER*2 ORDER
      CHARACTER*2 ELXX
      CHARACTER*6 GD
      CHARACTER*4 ELEV
      CHARACTER*7 ELNUM

      INTEGER*4 STANUM

      DIMENSION GDVAL(1001),GDNUM(1001)

      COMMON/IPRINT/IPRT
      COMMON/DONUM/ISN
      COMMON/GEODS/GDNUM,GDVAL
      COMMON/XY/NORTH,EAST
      COMMON/FILES/I3,I4,I2,ICON

      IF (CONV.LT.0) THEN
        PM='-'
      ELSE
        PM=' '
      ENDIF

      CALL TODMS(DABS(CONV),IDEG,IMIN,CSEC)

      CALL TODMS(LAT,LD,LM,SLAT)
      CALL TODMS(LON,LOD,LOM,SLON)

      IF(FILPRT) THEN
                  IF(ICON.GE.48) THEN
                     CALL HDGP
                     ICON = 0
                  ENDIF

       READ(CARDR,50) STANUM,NAME,ELEV,ELXX,ELEVT,ORDER
  50   FORMAT(T11,I3,T15,A30,T70,A4,A2,A1,T79,A2)

          IF((ORDER(1:1).EQ.'4').OR.(ELEV.EQ.'    ')) THEN
               ELNUM='       '
          ELSEIF((ELEVT.EQ.'B').OR.(ELEVT.EQ.'L')) THEN
               WRITE(ELNUM,200) ELEV,ELXX
  200          FORMAT(A4,'.',A2)
          ELSEIF((ELEVT.EQ.'R').OR.(ELEVT.EQ.'T')) THEN
               WRITE(ELNUM,205) ELEV,ELXX(1:1)
  205          FORMAT(A4,'.',A1,' ')
          ELSEIF((ELEVT.EQ.'P').OR.(ELEVT.EQ.'E').OR.
     &           (ELEVT.EQ.'V')) THEN
               WRITE(ELNUM,210) ELEV
  210          FORMAT(A4,'.  ')
          ELSE
               WRITE(ELNUM,215) ELEV
  215          FORMAT(A4,' SC')
          ENDIF

*** DO THE DO LOOP TO FIND THE GEOD HT
            GD='      '
            XGD='     '

         DO 60 I=1,ISN
            IF(GDNUM(I).EQ.STANUM) THEN
               XGD=GDVAL(I)
            ENDIF
   60     CONTINUE

             IF(XGD.NE.'     ') THEN
                READ(XGD,FMT='(F5.1)') GEOD
                 GSGN=' '
              IF(GEOD.LE.0.0D0) THEN
                 GSGN='-'
              ENDIF

                  GEOD=DABS(GEOD)
                  WRITE(GD,FMT='(F6.2)') GEOD
                  GD(1:1)=GSGN
             ENDIF





         READ(CARDR,5) NAME
  5      FORMAT(T15,A30)

        IF(J.EQ.1) THEN
         WRITE(3,10) NAME,NORTH,EAST,LD,LM,SLAT,LOD,LOM,SLON,
     &             ZONE,PM,IDEG,IMIN,CSEC,KP,ELNUM,GD
 10      FORMAT(A30,T33,F12.3,T46,F11.3,T60,I2.2,1X,I2.2,1X,F8.5,
     &       T75,I3.3,1X,I2.2,1X,F8.5,T91,A4,T96,A1,I1,1X,I2,1X,F5.2,
     &       T108,F10.8,T119,A7,T127,A6)
        ELSE
         WRITE(3,20) LD,LM,SLAT,LOD,LOM,SLON,ZONE,PM,IDEG,IMIN,CSEC,KP
  20     FORMAT(T60,I2.2,1X,I2.2,1X,F8.5,
     &       T75,I3.3,1X,I2.2,1X,F8.5,T91,A4,T96,A1,I1,1X,I2,1X,F5.2,
     &       T108,F10.8)
        ENDIF
      ELSE
        WRITE(*,30)
   30   FORMAT('0  LATITUDE',T20,'LONGITUDE',T37,'ZONE   ',
     *          T45,'CONVERGENCE    SCALE FACTOR'/,
     *          T4,'NORTH',T20,'WEST',/)

        WRITE(*,40)LD,LM,SLAT,LOD,LOM,SLON,ZONE,PM,IDEG,IMIN,CSEC,KP
   40   FORMAT(1X,I2.2, 1X,I2.2,1X,F8.5,T19,I3.3,1X,I2.2,1X,F8.5,
     *         T37,A4,T45,A1,I1,1X,I2,1X,F5.2,6X,F10.8)
      ENDIF


        IF(FILFLAG) THEN


*** UPDATE RECORD

      CARDR(7:10)='*80*'

      CALL VERDMS(LAT,ID1,IM1,S1,ISIGN)
      IF(ISIGN.GT.0) THEN
        ADIR1='N'
      ELSE
        ADIR1='S'
      ENDIF
      CALL VERDMS(LON,ID2,IM2,S2,ISIGN)
      IF(ISIGN.GT.0) THEN
        ADIR2='W'
      ELSE
        ADIR2='E'
      ENDIF
      IS1=S1*100000.D0+0.499999
      IS2=S2*100000.D0+0.499999

      WRITE(AD1,4) ID1
      WRITE(AM1,4) IM1
      WRITE(AS1,2) IS1
      WRITE(AD2,3) ID2
      WRITE(AM2,4) IM2
      WRITE(AS2,2) IS2
 4    FORMAT(I2.2)
 2    FORMAT(I7.7)
 3    FORMAT(I3.3)

      CARDR(45:46)=AD1
      CARDR(47:48)=AM1
      CARDR(49:55)=AS1
      CARDR(56:56)=ADIR1
      CARDR(57:59)=AD2
      CARDR(60:61)=AM2
      CARDR(62:68)=AS2
      CARDR(69:69)=ADIR2

*** PROCESS THE NEW *80* RECORD

      WRITE(4,150) CARDR
 150  FORMAT(A80)

        ENDIF

      ICON= ICON + 1
      RETURN
      END
