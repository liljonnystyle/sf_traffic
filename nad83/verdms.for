C     SccsID = "$Id: verdms.for 54980 2011-06-12 01:03:53Z Srinivas.Reddy $"  
      SUBROUTINE VERDMS(VAL,ID,IM,S,ISIGN)

*** CONVERT RADIANS TO DEG, MIN, SEC

      IMPLICIT DOUBLE PRECISION(A-H,O-Z)
      COMMON/CONST/RAD,ER,RF,ESQ,PI

    1 IF(VAL.GT.PI) THEN
        VAL=VAL-PI-PI
        GO TO 1
      ENDIF

    2 IF(VAL.LT.-PI) THEN
        VAL=VAL+PI+PI
        GO TO 2
      ENDIF

      IF(VAL.LT.0.D0) THEN
        ISIGN=-1
      ELSE
        ISIGN=+1
      ENDIF

      S=DABS(VAL*RAD)
      ID=IDINT(S)
      S=(S-ID)*60.D0
      IM=IDINT(S)
      S=(S-IM)*60.D0

      RETURN
      END
