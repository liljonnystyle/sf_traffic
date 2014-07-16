C     SccsID = "$Id: tmgrid.for 54979 2011-06-12 01:03:50Z Srinivas.Reddy $"  
      SUBROUTINE TMGRID(FI,LAM,NORTH,EAST,CONV,KP,ER,ESQ,EPS,CM,
     &                  FE,FN,SF,SO,R,A,B,C,U,V,W)

      IMPLICIT DOUBLE PRECISION(A-H,K-Z)
C
C*****  TRANSVERSE MERCATOR PROJECTION
C       CONVERSION OF GEODETIC COORDINATES TO GRID COORDINATES
C*****  Programmed by T. Vincenty, NGS, in July 1984.
C*****************  SYMBOLS AND DEFINITIONS *************************
C   Latitude positive north, longitude positive west.  All angles are
C     in radian measure.
C   N, E are northing and easting coordinates respectively.
C   LAT, LON are latitude and longitude respectively.
C   CONV is convergence.
C   KP is point scale factor.
C   ER is equatorial radius of the ellipsoid (= major semiaxis).
C   ESQ is the square of first eccentricity of the ellipsoid.
C   EPS is the square of second eccentricity of the ellipsoid.
C   CM is the central meridian of the projection zone.
C   FE is false easting value at the central meridian.
C   FN is "false northing" at the southernmost latitude, usually zero.
C   SF is scale factor at the central meridian.
C   SO is meridional distance (multiplied by the scale factor) from
C     the equator to the southernmost parallel of latitude for the zone.
C   R is the radius of the rectifying sphere (used for computing
C     meridional distance from latitude and vice versa).
C   A, B, C, U, V, W are other precomputed constants for determination
C     of meridional distance from latitude and vice versa.
C
C   The formula used in this subroutine gives geodetic accuracy within
C   zones of 7 degrees in east-west extent.  Within State transverse
C   Mercator projection zones, several minor terms of the equations
C   may be omitted (see a separate NGS publication).  If programmed
C   in full, the subroutine can be used for computations in surveys
C   extending over two zones.
C
C*********************************************************************
      OM=FI + A*SIN(2.*FI) + B*SIN(4.*FI) + C*SIN(6.*FI)
      S=R*OM*SF
      SINFI=SIN(FI)
      COSFI=COS(FI)
      TN=SINFI/COSFI
      TS=TN**2
      ETS=EPS*COSFI**2
      L=(LAM-CM)*COSFI
      LS=L*L
      RN=SF*ER/SQRT(1.-ESQ*SINFI**2)
C
      A2=RN*TN/2.
      A4=(5.-TS+ETS*(9.+4.*ETS))/12.
      A6=(61.+TS*(TS-58.)+ETS*(270.-330.*TS))/360.
      A1=-RN
      A3=(1.-TS+ETS)/6.
      A5=(5.+TS*(TS-18.)+ETS*(14.-58.*TS))/120.
      A7=(61.-479.*TS+179.*TS**2-TS**3)/5040.
      NORTH=S-SO + A2*LS*(1.+LS*(A4+A6*LS)) +FN
      EAST=FE + A1*L*(1.+ LS*(A3+LS*(A5+A7*LS)))
C
C*** CONVERGENCE
      C1=-TN
      C3=(1.+3.*ETS+2.*ETS**2)/3.
      C5=(2.-TS)/15.
      CONV=C1*L*(1.+LS*(C3+C5*LS))
C
C*** POINT SCALE FACTOR
      F2=(1.+ETS)/2.
      F4=(5.-4.*TS+ETS*( 9.-24.*TS))/12.
      KP=SF*(1.+F2*LS*(1.+F4*LS))
C
      RETURN
      END
