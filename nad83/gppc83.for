C     SccsID = "$Id: gppc83.for 54959 2011-06-12 01:02:55Z Srinivas.Reddy $"  
       SUBROUTINE GPPC83
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
   10 FORMAT('0*** ROUTINE GPs TO SPCs ***'//,
     *       ' DO YOU WANT TO RUN INTERACTIVELY (Y/N)?')
      READ(5,20) YN
   20 FORMAT(A1)

      IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
        CALL INTGP
      ELSE
        CALL BATGP
      ENDIF

      WRITE(6,30)
   30 FORMAT('0END OF ROUTINE GPs TO SPCs')
      RETURN
      END
