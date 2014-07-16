C     SccsID = "$Id: intpc.for 54963 2011-06-12 01:03:06Z Srinivas.Reddy $"  
      SUBROUTINE INTPC
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION ICODE(3)
      LOGICAL FILFLAG,FILPRT
      CHARACTER*1 YN,YN1
      CHARACTER*30 NAME,GPPFIL,GPFIL
      CHARACTER*80 CARDR
      REAL*8 NORTH
      COMMON/XY/NORTH,EAST

      FILFLAG=.FALSE.
      FILPRT=.FALSE.

      WRITE(*,10)
   10 FORMAT('0DO YOU WANT THE OUTPUT LISTING SAVED ON A FILE (Y/N)?')
      READ(*,20) YN
   20 FORMAT(A1)

      IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
   25   WRITE(*,30)
   30   FORMAT('0FILE NAME: ')
        READ(*,40) GPPFIL
   40   FORMAT(A30)
        OPEN(3,STATUS='NEW',FILE=GPPFIL,ERR=900)
        FILPRT=.TRUE.
        CALL HDPC
      ENDIF
      GO TO 950

 900  WRITE(*,901)
 901  FORMAT('0 FILE ALREADY EXIST, DO YOU WANT TO'/,
     &       '  WRITE OVER IT (Y/N) '/,
     &       '  TYPE ANSWER  '/)
      READ(*,20) YN

         IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
           OPEN(3,STATUS='UNKNOWN',FILE=GPPFIL)
           FILPRT=.TRUE.
           CALL HDPC
         ELSE
           GO TO 25
         ENDIF


  950 WRITE(*,951)
  951 FORMAT('0 DO YOU WANT TO SAVE AN *80* RECORD '/,
     &       '  OUTPUT FILE  (Y/N)'/,
     &       '  TYPE ANSWER  '/)
      READ(5,20) YN

      IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
  959    WRITE(*,960)
  960    FORMAT('0 TYPE FILE NAME:'/)
         READ(*,40) GPFIL
         OPEN(4,STATUS='NEW',FILE=GPFIL,ERR=1000)
         FILFLAG=.TRUE.
      ENDIF

        GO TO 50

 1000  WRITE(*,1001)
 1001  FORMAT('0 FILE ALREADY EXISTS, DO YOU WANT TO '/,
     &        '  WRITE OVER IT (Y/N) '/,
     &        '  TYPE ANSWER  '/)

       READ(*,20) YN

        IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
          OPEN(4,STATUS='UNKNOWN',FILE=GPFIL)
          FILFLAG=.TRUE.
          GO TO 50
        ELSE
          GO TO 959
        ENDIF

   50   WRITE(CARDR,45)
   45   FORMAT(T7,'*81*')

      IF(FILPRT) THEN
        WRITE(*,52)
   52   FORMAT('0ENTER STATION NAME:  ')
        READ(*,40) NAME

        WRITE(CARDR,41) NAME
   41     FORMAT(T15,A30)
      ELSE
        NAME='                              '
         WRITE(CARDR,41) NAME
      ENDIF

      WRITE(*,60)
   60 FORMAT('0ENTER NORTHING OR "Y" IN METERS:'/,
     *       ' NNNNNNNN.NNN'/)
      READ(*,62) NORTH
   62 FORMAT(F12.3)

      WRITE(*,64)
   64 FORMAT('0ENTER EASTING OR "X" IN METERS:'/,
     *       ' EEEEEEE.EEE'/)
      READ(*,66)EAST
   66 FORMAT(F11.3)

      WRITE(*,68)
   68 FORMAT('0ENTER ZONE CODES, AS MANY AS THREE.'/,
     *       ' (4-DIGITS SEPARATED BY BLANKS OR COMMAS):')
      READ(*,70)ICODE(1),ICODE(2),ICODE(3)
   70 FORMAT(I4,1X,I4,1X,I4)

      CALL DRPCGP(CARDR,ICODE,FILFLAG,FILPRT)

      WRITE(*,80)
   80 FORMAT('0ANY MORE COMPUTATIONS (Y/N)?')
      READ(*,20) YN1

      IF((YN1.EQ.'N').OR.(YN1.EQ.'n')) THEN
         IF(FILPRT) THEN
           CLOSE(3,STATUS='KEEP')
         ENDIF
         IF(FILFLAG) THEN
           CLOSE(4,STATUS='KEEP')
         ENDIF
      ELSE
            GO TO 50
      ENDIF


      RETURN
      END
