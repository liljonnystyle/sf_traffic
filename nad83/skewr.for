C     SccsID = "$Id: skewr.for 54970 2011-06-12 01:03:25Z Srinivas.Reddy $"  
      SUBROUTINE SKEWR(NORTH,EAST,LAT,LON,B,C,D,SGO,CGO,SGC,
     &                 CGC,LONO,FE,FN,F0,F2,F4,F6,ESQ,CONV,KP,
     &                 GAMC,XI)
***    OBLIQUE MERCATOR PROJECTION                          ***
*** CONVERSION OF GRID COORDS TO GEODETIC COORDS
*** REVISED SUBROUTINE OF T. VINCENTY   FEB. 25, 1985
***************************************************************

      IMPLICIT DOUBLE PRECISION(A-H,K-Z)

      U=SGC*(EAST-FE)+CGC*(NORTH-FN)
      V=CGC*(EAST-FE)-SGC*(NORTH-FN)
      R=DSINH(V/D)
      S=DCOSH(V/D)
      SINE=DSIN(U/D)
      Q=(DLOG((S-SGO*R+CGO*SINE)/(S+SGO*R-CGO*SINE))/2.D0-C)/B
      EX=DEXP(Q)
      XR=DATAN((EX-1.D0)/(EX+1.D0))*2.D0
      CS=DCOS(XR)

      LAT=XR+(F0+F2*CS*CS+F4*CS**4+F6*CS**6)*CS*DSIN(XR)
      LON=LONO-DATAN((SGO*SINE+CGO*R)/DCOS(U/D))/B
****************************************
*
*
*
C
      FI = LAT
      LAM = LON

      E=DSQRT(ESQ)
      SINB=SIN(FI)
      COSB=COS(FI)
      DL=(LAM-LONO)*B
      SINDL=SIN(DL)
      COSDL=COS(DL)
      Q=(LOG((1+SINB)/(1-SINB)) - E*LOG((1+E*SINB)/(1-E*SINB)))/2.
      R=SINH(B*Q+C)
      S=COSH(B*Q+C)
      U=D*ATAN((CGO*R-SGO*SINDL)/COSDL)
      V=D*LOG((S-SGO*R-CGO*SINDL)/(S+SGO*R+CGO*SINDL))/2.
      CONV=ATAN((SGO-CGO*SINDL*R)/(CGO*COSDL*S))-GAMC
      KP=XI*SQRT(1-ESQ*SINB**2)*COS(U/D)/COSB/COSDL

      RETURN
      END
