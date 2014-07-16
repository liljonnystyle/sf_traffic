C     SccsID = "$Id: lamd1.for 54964 2011-06-12 01:03:08Z Srinivas.Reddy $"  
*********************************************************************
C
      SUBROUTINE LAMD1 (FI,LAM,NORTH,EAST,CONV,KP,ER,ESQ,E,CM,EO,
     &                  NB,SINFO,RB,K)
      IMPLICIT DOUBLE PRECISION(A-H,K-Z)
C
C*****  LAMBERT CONFORMAL CONIC PROJECTION, 2 STANDARD PARALLELS  *****
C       CONVERSION OF GEODETIC COORDINATES TO GRID COORDINATES
C*****  Programmed by T. Vincenty in July 1984.
C************************ SYMBOLS AND DEFINITIONS *********************
C       Latitude positive north, longitude positive west.  All angles
C         are in radian measure.
C       FI, LAM are latitude and longitude respectively.
C       NORTH, EAST are northing and easting coordinates respectively.
C       NORTH EQUALS Y PLANE AND EAST EQUALS THE X PLANE.
C       CONV is convergence.
C       KP is point scale factor.
C       ER is equatorial radius of the ellipsoid (= major semiaxis).
C       ESQ is the square of first eccentricity of the ellipsoid.
C       E is first eccentricity.
C       CM is the central meridian of the projection zone.
C       EO is false easting value at the central meridian.
C       NB is false northing for the southernmost parallel of the
C           projection, usually zero.
C       SINFO = SIN(FO), where FO is the central parallel.  This is a
C         precomputed value.
C       RB is mapping radius at the southernmost latitude. This is a
C         precomputed value.
C       K is mapping radius at the equator.  This is a precomputed
C         value.
C
C***********************************************************************
C
      SINLAT=SIN(FI)
      COSLAT=COS(FI)
      CONV=(CM-LAM)*SINFO
C
      Q=(LOG((1+SINLAT)/(1-SINLAT))-E*LOG((1+E*SINLAT)/(1-E*SINLAT)))/2.
      RPT=K/EXP(SINFO*Q)
      NORTH=NB+RB-RPT*COS(CONV)
      EAST=EO+RPT*SIN(CONV)
      WP=SQRT(1.-ESQ*SINLAT**2)
      KP=WP*SINFO*RPT/(ER*COSLAT)
C
C
 1000 RETURN
      END
