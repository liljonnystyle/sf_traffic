C     SccsID = "$Id: skewd.for 54971 2011-06-12 01:03:28Z Srinivas.Reddy $"  
*********************************************************************
*
*
*
        SUBROUTINE SKEWD(FI,LAM,U,V,NORTH,EAST,CONV,KP,B,C,D,SGO,CGO,
     &              GAMC,CGC,SGC,XI,E,ESQ,LONO,FN,FE)
      IMPLICIT DOUBLE PRECISION(A-H,K-Z)
C

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
      NORTH=U*CGC-V*SGC+FN
      EAST=U*SGC+V*CGC+FE
      CONV=ATAN((SGO-CGO*SINDL*R)/(CGO*COSDL*S))-GAMC
      KP=XI*SQRT(1-ESQ*SINB**2)*COS(U/D)/COSB/COSDL
      RETURN
      END
