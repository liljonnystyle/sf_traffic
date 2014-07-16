C     SccsID = "$Id: batgp.for 54952 2011-06-12 01:02:35Z Srinivas.Reddy $"  
      SUBROUTINE BATGP
      IMPLICIT REAL*8 (A-H,O-Z)
      CHARACTER*5 GGVAL,GDVAL
      CHARACTER*8 TITLE,GNUM
      DIMENSION ICODE(3)
      DIMENSION GDNUM(1001),GDVAL(1001)
      CHARACTER*30 NAME,PCFIL,GPFIL
      CHARACTER*80 CARDR
      CHARACTER*1 YN
      CHARACTER*1 EW
      LOGICAL FILFLAG
      LOGICAL EWFLAG
      COMMON/LATLON/LD,LM,SLAT,LOD,LOM,SLON
      COMMON/FILES/I3,I4,I2,ICON
      COMMON/IPRINT/IPRT
      COMMON/DONUM/ISN
       COMMON/GEODS/GDNUM,GDVAL
       COMMON/TITLE/GNUM


      FILFLAG=.TRUE.
      EWFLAG = .FALSE.
          ICON = 0
          ISN = 0

    5 WRITE(6,10)
   10 FORMAT(' NAME OF INPUT FILE-')
      READ(5,20) GPFIL
   20 FORMAT(A30)


      OPEN(2,STATUS='OLD',FILE=GPFIL,ERR=900)

      GO TO 25

  900 WRITE(6,901)
  901 FORMAT('  FILE DOES NOT EXITS, DO YOU WANT TO '/,
     &       '  TRY AGAIN (Y/N)'/,
     &       '  TYPE ANSWER '/)

      READ(5,902) YN
  902 FORMAT(A1)

        IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
            GO TO 5
        ELSE
            GO TO 99
        ENDIF

   25 WRITE(6,30)
   30 FORMAT(' NAME OF OUTPUT FILE-')
      READ(5,20) PCFIL


      OPEN(3,STATUS='NEW',FILE=PCFIL,ERR=910)
      GO TO 400

  910 WRITE(6,911)
  911 FORMAT('  FILE ALREADY EXIST, DO YOU WANT TO '/,
     &       '  WRITE OVER IT  (Y/N) '/,
     &       '  TYPE ANSWER : '/)

      READ(5,902) YN

       IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
          OPEN(3,STATUS='UNKNOWN',FILE=PCFIL)
       ELSE
          GO TO 25
       ENDIF


  400 WRITE(6,500)
 500  FORMAT (/,'0ENTER ZONE CODES, AS MANY AS THREE.'/,
     *        ' (4-DIGITS SEPARATED BY BLANKS OR COMMAS):',
     *        ' EXAMPLE  0404,2702,2703 - FOR ZONES '/,
     *        ' CA 4,NV C,NV W '/,
     *        ' TYPE ZONES ??   ')

      READ(5,510)ICODE(1),ICODE(2),ICODE(3)
 510  FORMAT(I4,1X,I4,1X,I4)

      PRINT *,'            '
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
      CALL HDGP

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
             EWFLAG = .FALSE.

          IF(CARDR(7:10).EQ.'*80*') THEN

          READ(CARDR,50,ERR=9000)LD,LM,SLAT,LOD,LOM,SLON,EW
   50     FORMAT(T45,I2,I2,F7.5,1X,I3,I2,F7.5,T69,A1)

           IF(EW.EQ.'E') THEN
             EWFLAG= .TRUE.
           ENDIF

          CALL DRGPPC(CARDR,ICODE,FILFLAG,EWFLAG)

          GO TO 40

          ELSE

          GO TO 40

          ENDIF

          GO TO 99

 9000 WRITE(6,9001) CARDR
 9001 FORMAT('  ERROR IN BLUE BOOK INPUT RECORD '/,A80)

 99   CLOSE(2,STATUS='KEEP')
      CLOSE(3,STATUS='KEEP')


      RETURN
      END
