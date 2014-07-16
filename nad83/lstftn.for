C     SccsID = "$Id: lstftn.for 54968 2011-06-12 01:03:20Z Srinivas.Reddy $"  
      SUBROUTINE LSTFTN


      CHARACTER*133 TXT
      CHARACTER*80  FOLD
      CHARACTER*1 FF

      FF=CHAR(12)

      PRINT *,'             '
      PRINT *,'                 '
      PRINT *,'   SUBROUTINE LSTFTN    '
      PRINT *,'                 '
      PRINT *,'   NOTE: MAKE SURE THE PRINTER IS TURNED ON '
      PRINT *,'                  '

      OPEN(2,FILE='PRN',FORM='FORMATTED')

      PRINT *,'   NAME OF INPUT FILE WRITTEN WITH '
      PRINT *,'   FORTRAN OPTIONS.                '

      PRINT *,'                                   '
      PRINT *,'   TYPE NAME:    '
      PRINT *,'                 '

      READ(5,50) FOLD
 50   FORMAT(A80)

      OPEN(3,FILE=FOLD,STATUS='OLD')


 100  READ(3,150,END=900) TXT
 150  FORMAT(A133)


          IF(TXT(1:1).EQ.'1') THEN
             WRITE(2,200) FF
  200        FORMAT(A)
          ELSE
             WRITE(2,150) TXT
          ENDIF
             GO TO 100

 900  WRITE(2,200) FF
      WRITE(2,200) FF

      CLOSE(UNIT=3)
      CLOSE(UNIT=2)

      PRINT *,'  JOB COMPLETED   '
      PRINT *,'                  '
      RETURN
      END
