C     SccsID = "$Id: lconst.for 54966 2011-06-12 01:03:14Z Srinivas.Reddy $"  
*********************************************************************
      SUBROUTINE LCONST(ER,RF,FIS,FIN,FIB,ESQ,E,SINFO,RB,K,KO,NO,
     &            G,NB)
      IMPLICIT DOUBLE PRECISION(A-H,K-Z)
      Q(E,S)=(LOG((1+S)/(1-S))-E*LOG((1+E*S)/(1-E*S)))/2.
C
C*****  LAMBERT CONFORMAL CONIC PROJECTION, 2 STANDARD PARALLELS  *****
C        PRECOMPUTATION OF CONSTANTS
C*****  Programmed by T. Vincenty in July 1984.
C************************ SYMBOLS AND DEFINITIONS *********************
C       Latitude positive north, in radian measure.
C       ER is equatorial radius of the ellipsoid (= major semiaxis).
C       RF is reciprocal of flattening of the ellipsoid.
C       FIS, FIN, FIB are respecitvely the latitudes of the south
C         standard parallel, the north standard parallel, and the
C         southernmost parallel.
C       ESQ is the square of first eccentricity of the ellipsoid.
C       E is first eccentricity.
C       SINFO = SIN(FO), where FO is the central parallel.
C       RB is mapping radius at the southernmost latitude.
C       K is mapping radius at the equator.
C       NB is false northing for the southernmost parallel.
C       KO is scale factor at the central parallel.
C       NO is northing of intersection of central meridian and parallel.
C       G is a constant for computing chord-to-arc corrections.
C***********************************************************************
C
      F=1./RF
      ESQ=F+F-F**2
      E=SQRT(ESQ)
      SINFS=SIN(FIS)
      COSFS=COS(FIS)
      SINFN=SIN(FIN)
      COSFN=COS(FIN)
      SINFB=SIN(FIB)
C
      QS=Q(E,SINFS)
      QN=Q(E,SINFN)
      QB=Q(E,SINFB)
      W1=SQRT(1.-ESQ*SINFS**2)
      W2=SQRT(1.-ESQ*SINFN**2)
      SINFO=LOG(W2*COSFS/(W1*COSFN))/(QN-QS)
      K=ER*COSFS*EXP(QS*SINFO)/(W1*SINFO)
      RB=K/EXP(QB*SINFO)
      QO=Q(E,SINFO)
      RO=K/EXP(QO*SINFO)
      COSFO=SQRT(1.-SINFO**2)
      KO=SQRT(1.-ESQ*SINFO**2)*(SINFO/COSFO)*RO/ER
      NO=RB+NB-RO
      G=(1-ESQ*SINFO**2)**2/(2*(ER*KO)**2)*(1-ESQ)
C
      RETURN
      END
