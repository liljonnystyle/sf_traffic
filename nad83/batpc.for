C     SccsID = "$Id: batpc.for 54953 2011-06-12 01:02:38Z Srinivas.Reddy $"  
      SUBROUTINE BATPC
      IMPLICIT REAL*8 (A-H,O-Z)
      CHARACTER*8 TITLE,GNUM
      CHARACTER*5 GGVAL,GDVAL
      DIMENSION GDNUM(1001),GDVAL(1001)
      DIMENSION ICODE(3)
      CHARACTER*30 GPPFIL,PCFIL,GPFIL
      CHARACTER*80 CARDR
      CHARACTER*1 ANS,YN
      LOGICAL FILFLAG,FILPRT
      REAL*8 NORTH
      COMMON/XY/NORTH,EAST
      COMMON/FILES/I3,I4,I2,ICON
      COMMON/GEODS/GDNUM,GDVAL
      COMMON/TITLE/GNUM
      COMMON/IPRINT/IPRT
      COMMON/DOMUN/ISN


      FILFLAG=.TRUE.
      FILPRT=.FALSE.

        ICON=0

    5 WRITE(6,10)
   10 FORMAT('0NAME OF INPUT BLUEBOOK FILE WITH *81* RECORDS-')
      READ(5,20) PCFIL
   20 FORMAT(A30)

      OPEN(2,STATUS='OLD',FILE=PCFIL,ERR=900)

      GO TO 25

 900  WRITE(6,901)
 901  FORMAT('0 FILE DOES NOT EXISTS, DO YOU WANT TO '/,
     &       '  TRY AGAIN (Y/N) '/,
     &       '  TYPE ANSWER '/)

      READ(5,902) YN
 902  FORMAT(A1)

         IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
            GO TO 5
         ELSE
            GO TO 99
         ENDIF

   25 WRITE(6,30)
   30 FORMAT('0NAME OF BLUEBOOK OUTPUT FILE WITH *80* RECORDS-')
      READ(5,20) GPFIL

      OPEN(4,STATUS='NEW',FILE=GPFIL,ERR=910)
      GO TO 400

 910  WRITE(6,911)
 911  FORMAT('0 FILE ALREADY EXIST, DO YOU WANT TO '/,
     &       '  WRITE OVER IT (Y/N) '/,
     &       '  TYPE ANSWER : '/)

      READ(5,902) YN

           IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
               OPEN(4,STATUS='UNKNOWN',FILE=PCFIL)
           ELSE
               GO TO 25
           ENDIF


 400  WRITE(6,31)
 31   FORMAT('0DO YOU WANT THE OUTPUT LISTING SAVED ON A FILE (Y/N)')
      READ(5,32) ANS
 32   FORMAT(A1)

       IF ((ANS.EQ.'Y').OR.(ANS.EQ.'y')) THEN
           FILPRT=.TRUE.
 401       WRITE(6,33)
 33        FORMAT('0  OUTPUT FILE NAME: ')
           READ(5,34) GPPFIL
 34        FORMAT(A30)
           OPEN(3,STATUS='NEW',FILE=GPPFIL,ERR=920)
            GO TO 405

 920  WRITE(6,911)

      READ(5,902) YN

           IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
               OPEN(3,STATUS='UNKNOWN',FILE=GPPFIL)
           ELSE
               GO TO 401
           ENDIF
       ENDIF


 405  PRINT *,'            '
      PRINT *,'            '
      PRINT *,' THE TYPE OF COORDINATE LISING :  '
      PRINT *,'             '
      PRINT *,' 1 - PRELIMINARY (BEFORE FINAL ADJUSTMENT)'
      PRINT *,' 2 - FINAL (AFTER A COMPLETED PROJECT)'
      PRINT *,'         '
      PRINT *,' TYPE NUMBER:   '

      READ(5,FMT='(I1)') IPRT

       PRINT *,'            '
       PRINT *,'            '
       PRINT *,'  TYPE THE PROJECT NUMBER  IE; G-12345 OR'
       PRINT *,'   GPS-1234 (8 CHARACTERS MAX) '
       PRINT *,'              '
       PRINT *, '  TYPE THE NUMBER :  '

       READ(5,FMT='(A8)') GNUM


            PRINT *,'                  '
            PRINT *,'                  '
            PRINT *, '   PROGRAM IS EXCUTING NOW !!!!!!! '
            PRINT *,'                      '

      CALL CLAIM

            PRINT *,'                      '
      CALL HDPC

***    READ INPUT FILE AND SET ARRAYS FOR THE GEOD HTS

  100 READ(2,45,END=199) CARDR

        IF(CARDR(7:10).EQ.'*84*') THEN
           ISN = ISN + 1

           GGVAL='     '

           READ(CARDR,FMT='(T11,I3)') IGDNUM
           READ(CARDR,FMT='(T72,A5)') GGVAL
           GDNUM(ISN)= IGDNUM
           GDVAL(ISN)= GGVAL
           GO TO 100
        ELSE
           GO TO 100
        ENDIF

  199  REWIND(2)




   40 READ(2,45,END=99) CARDR
   45 FORMAT(A80)

          IF(CARDR(7:10).EQ.'*81*') THEN

            READ(CARDR,50,ERR=9000) EAST,NORTH,ICODE(1)
   50       FORMAT(T45,F10.3,T55,F11.3,T66,I4)

            CALL DRPCGP(CARDR,ICODE,FILFLAG,FILPRT)

          ELSE
            WRITE(4,45) CARDR

          ENDIF

          GO TO 40

 9000 WRITE(6,9001) CARDR
 9001 FORMAT('0 ERROR IN BLUE BOOK INPUT RECORD '/,A80)

 99   CLOSE(2,STATUS='KEEP')
      IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
          CLOSE(3,STATUS='KEEP')
          CLOSE(4,STATUS='KEEP')
      ENDIF
      RETURN
      END
