C     SccsID = "$Id: tconst.for 54977 2011-06-12 01:03:44Z Srinivas.Reddy $"  
*********************************************************************
      SUBROUTINE TCONST (ER,RF,SF,OR,ESQ,EPS,R,A,B,C,U,V,W,SO,
     &                   CM,FE,FN)
      IMPLICIT DOUBLE PRECISION(A-H,O-Z)
C
C***** TRANSVERSE MERCATOR PROJECTION
C      PRECOMPUTATION OF CONSTANTS
C***** Programmed by T. Vincenty, NGS, in July 1984.
C******************** SYMBOLS AND DEFINITIONS  **********************
C   ER is equatorial radius of the ellipsoid (= major semiaxis).
C   RF is reciprocal of flattening of the ellipsoid.
C   SF is scale factor of the central meridian.
C   OR is southernmost parallel of latitude (in radians) for which
C     the northing coordinate is zero at the central meridian.
C   R, A, B, C, U, V, W are ellipsoid constants used for computing
C     meridional distance from latitude and vice versa.
C   SO is meridional distance (multiplied by the scale factor) from
C     the equator to the southernmost parallel of latitude.
C******************************************************************
C
      F=1./RF
      ESQ=(F+F-F**2)
      EPS=ESQ/(1.-ESQ)
      PR=(1.-F)*ER
      EN=(ER-PR)/(ER+PR)
      A=-1.5D0*EN + (9./16.)*EN**3
      B= 0.9375D0*EN**2 - (15./32.)*EN**4
      C=-(35./48.)*EN**3
      U=1.5D0*EN - (27./32.)*EN**3
      V=1.3125D0*EN**2 - (55./32.)*EN**4
      W=(151./96.)*EN**3
      R=ER*(1.-EN)*(1.-EN**2)*(1.+2.25D0*EN**2+(225./64.)*EN**4)
      OMO=OR + A*SIN(2.*OR) + B*SIN(4.*OR) + C*SIN(6.*OR)
      SO=SF*R*OMO
C
      RETURN
      END
