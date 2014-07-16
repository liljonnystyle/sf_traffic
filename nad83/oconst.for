C     SccsID = "$Id: oconst.for 54967 2011-06-12 01:03:17Z Srinivas.Reddy $"  
*********************************************************************
*
*     OBLICQUE CONSTANTS
*
      SUBROUTINE OCONST(ER,RF,A,B,C,D,SGO,CGO,GAMC,SGC,CGC,XI,KC,
     &                  LONO,F0,F2,F4,F6,LATC,LONC,ESQ)

***    OBLIQUE MERCATOR PROJECTION                          ***
*** COMPUTATIONS OF CONSTANTS
*** REVISED SUBROUTINE OF T. VINCENTY   FEB. 25, 1985

      IMPLICIT DOUBLE PRECISION(A-H,K-Z)


      QQ(X,E)=(DLOG((1.D0+X)/(1.D0-X))-E*DLOG((1.D0+E*X)/
     &        (1.D0-E*X)))/2.D0
      COSHI(X)=DLOG(X+DSQRT(X*X-1))

      E=DSQRT(ESQ)
      EPS=ESQ/(1.D0-ESQ)
      E2=ESQ
      E4=E2*E2
      E6=E2**3
      E8=E2**4

      C2=E2/2.D0+5.D0*E4/24.D0+E6/12.D0+13.D0*E8/360.D0
      C4=7.D0*E4/48.D0+29.D0*E6/240.D0+811.D0*E8/11520.D0
      C6=7.D0*E6/120.D0+81.D0*E8/1120.D0
      C8=4279.D0*E8/161280.D0

      F0=2.D0*C2-4.D0*C4+6.D0*C6-8.D0*C8
      F2=8.D0*C4-32.D0*C6+80.D0*C8
      F4=32.D0*C6-192.D0*C8
      F6=128.D0*C8

      SINB=DSIN(LATC)
      COSB=DCOS(LATC)
      B=DSQRT(1.D0+EPS*COSB**4)
      W=DSQRT(1.D0-ESQ*SINB*SINB)
      A=B*ER*DSQRT(1.D0-ESQ)/(W*W)
      QC=QQ(SINB,E)
      C=COSHI(B*DSQRT(1.D0-ESQ)/W/COSB)-B*QC
      D=A*KC/B

      SGC=DSIN(GAMC)
      CGC=DCOS(GAMC)
      SGO=SGC*COSB*ER/(A*W)
      CGO=DSQRT(1.D0-SGO*SGO)
      LONO=LONC+DASIN(SGO*DSINH(B*QC+C)/CGO)/B
      EF=-SGO
      G=CGO
      H=EF/G
      XI=A*KC/ER

      RETURN
      END
