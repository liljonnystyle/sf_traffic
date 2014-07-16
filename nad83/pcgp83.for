C     SccsID = "$Id: pcgp83.for 54969 2011-06-12 01:03:22Z Srinivas.Reddy $"  
       SUBROUTINE PCGP83
*
***********************************************************************

      IMPLICIT DOUBLE PRECISION(A-H,O-Z)
      DIMENSION SPCC(135,6),IZC(135),UTMC(60)
      CHARACTER*1 YN,AP(135)
      CHARACTER*4 ZN(135)
      COMMON/TAB/SPCC,UTMC,IZC
      COMMON/CHAR/ZN,AP
      COMMON/CONST/RAD,ER,RF,ESQ,PI

      PI=4.D0*DATAN(1.D0)
      RAD=180.D0/PI
      ER=6378137.D0
      RF=298.257222101D0
      F=1.D0/RF
      ESQ=(F+F-F*F)

      CALL TBLSPC(IZC,AP,SPCC,UTMC,ZN)

      WRITE(6,10)
   10 FORMAT('0*** ROUTINE SPC TO GP  ***'//,
     *       ' DO YOU WANT TO RUN INTERACTIVELY (Y/N)?'/,
     *      ' TYPE ANSWER ')
      READ(5,20) YN
   20 FORMAT(A1)

      IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
        CALL INTPC
      ELSE
        CALL BATPC
      ENDIF

      WRITE(6,30)
   30 FORMAT('0END OF ROUTINE SPC TO GP')
      RETURN
      END
