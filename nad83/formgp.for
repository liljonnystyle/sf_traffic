C     SccsID = "$Id: formgp.for 54957 2011-06-12 01:02:49Z Srinivas.Reddy $"  
      SUBROUTINE FORMGP(CARDR,NORTH,EAST,CONV,KP,ZONE,FILFLAG,J)
      IMPLICIT REAL*8 (A-H,O-Z)
      CHARACTER*5 XGD,GDVAL
      DIMENSION GDVAL(1001),GDNUM(1001)
      LOGICAL FILFLAG
      REAL*8 NORTH,KP
      CHARACTER*1 PM,ESGN,GSGN
      CHARACTER*1 ELEVT
      CHARACTER*2 ORDER
        CHARACTER*1  BUFF(20)
      CHARACTER*6 GD
      CHARACTER*80 CARDR
      INTEGER*4 STANUM
       CHARACTER*7 ELNUM
      CHARACTER*4 ZONE
      CHARACTER*30 NAME
      COMMON/LATLON/LD,LM,SLAT,LOD,LOM,SLON
       COMMON/FILES/I3,I4,I2,ICON
       COMMON/IPRINT/IPRT
       COMMON/DONUM/ISN
       COMMON/GEODS/GDNUM,GDVAL

      IF (CONV.LT.0) THEN
        PM='-'
      ELSE
        PM=' '
      ENDIF

      CALL TODMS(DABS(CONV),IDEG,IMIN,CSEC)

      IF(FILFLAG) THEN
                  IF(ICON.GE.50) THEN
                     CALL HDGP
                     ICON = 0
                  ENDIF

       READ(CARDR,50) STANUM,NAME,ELEV,ELEVT,ORDER
  50   FORMAT(T11,I3,T15,A30,T70,F6.2,A1,T79,A2)

               ELNUM='       '


          IF((ELEVT.EQ.'B').OR.(ELEVT.EQ.'L')) THEN
              CALL CHGDEC (7,2,ELEV,BUFF)
          ELSEIF((ELEVT.EQ.'R').OR.(ELEVT.EQ.'T').OR.
     &           (ELEVT.EQ.'E')) THEN
                CALL CHGDEC(6,1,ELEV,BUFF)
          ELSEIF((ELEVT.EQ.'P').OR.(ELEVT.EQ.'V')) THEN
               CALL CHGDEC (5,0,ELEV,BUFF)
          ELSEIF((ELEVT.EQ.'M')) THEN
               CALL CHGDEC (5,0,ELEV,BUFF)
               BUFF(5)=' '
               BUFF(6)='S'
               BUFF(7)='C'
               BUFF(8)='$'
          ELSE
               GO TO 206
          ENDIF

           DO 205 I=1,7
              IF(BUFF(I).EQ.'$') GO TO 206
              ELNUM(I:I)=BUFF(I)
  205      CONTINUE
  206      CONTINUE

*** DO THE DO LOOP TO FIND THE GEOD HT
            GD='      '
            XGD='     '

         DO 60 I=1,ISN
            IF(GDNUM(I).EQ.STANUM) THEN
               XGD=GDVAL(I)
            ENDIF
   60     CONTINUE

             IF(XGD.NE.'     ') THEN
                READ(XGD,FMT='(F5.1)') GEOD
                 GSGN=' '
              IF(GEOD.LE.0.0D0) THEN
                 GSGN='-'
              ENDIF

                  GEOD=DABS(GEOD)
                  WRITE(GD,FMT='(F6.2)') GEOD
                  GD(1:1)=GSGN
             ENDIF



        IF(J.EQ.1) THEN
          WRITE(3,10) NAME,LD,LM,SLAT,LOD,LOM,SLON,
     &             NORTH,EAST,ZONE,PM,IDEG,IMIN,CSEC,KP,ELNUM,
     &             GD
 10       FORMAT(1X,A30,T34,I2,1X,I2,1X,F8.5,T49,I3.3,1X,I2.2,1X,
     &       F8.5,T67,F11.3,T79,F11.3,T91,A4,T96,A1,I1,1X,I2,1X,F5.2,
     &       T108,F10.8,T119,A7,T127,A6)
                ICON= ICON + 1
        ELSE
          WRITE(3,20) NORTH,EAST,ZONE,PM,IDEG,IMIN,CSEC,KP
  20      FORMAT(T67,F11.3,T79,F11.3,T91,A4,T96,A1,I1,1X,I2,1X,
     &           F5.2,T108,F10.8)
        ENDIF
      ELSE
        WRITE(*,30)
   30   FORMAT('   NORTH(Y)     EAST(X)   ZONE   ',
     *         'CONVERGENCE  SCALE')
        WRITE(*,40)NORTH,EAST,ZONE,PM,IDEG,IMIN,CSEC,KP
   40   FORMAT(1X,F11.3,1X,F11.3,2X,A4,2X,A1,I1,1X,I2,1X,
     *         F5.2,3X,F10.8)
                ICON= ICON + 1
      ENDIF

      RETURN
      END
***********************************************************
      SUBROUTINE CHGDEC (NNN,MMM,SS,CHAR)
C     -----------------------------------------------------
      CHARACTER*1  DASH,ZERO,DOL,BLK1,CHAR(*),IB(20),TT
      CHARACTER*20 JB
C  -------------------------------
C         M T E N  (VERSION 3)
C  -------------------------------
      INTEGER*4   IDG,MIN
      REAL*8      S,SS,DEC,W,SEC,TEN,TOL
C
      EQUIVALENCE (IB,JB)
C
      DATA BLK1,DOL,ZERO,DASH/' ','$','0','-'/,TEN/10.0D0/
C
C        CHAR      1-16      LENGTH OF CHARACTER ARRAY FIELD
C        NR        1-13      LENGTH OF FIELD TO BE USED FROM LEFT
C        NP        7-13      LOCATION OF DECIMAL POINT FROM RIGHT
C        NEG       CHAR(1)   PUT THE MINUS SIGN HERE
C        EXAMPLE:            RANGE NR=14 AND WITH A POINT NP=6
C                            W=  -3600.376541
C
C CHAR FIELD     1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
C BLANK FILLED   B  B  B  B  B  B  B  B  B  B  B  B  B  B  B  B BLANK
C NR ADDED      |B  B  B  B  B  B  B  B  B  B  B  B  B  B| B  B LIMIT
C NP ADDED      |B  B  B  B  B  B  B  .  B  B  B  B  B  B| B  B POINT
C W ENTERED     |B  B  -  3  6  0  0  .  3  7  6  5  4  1| 8  4
C DOL (SIGN)    |B  B  -  3  6  0  0  .  3  7  6  5  4  1| $  4
C NEG (SIGN)    |B  B  -  3  6  0  0  .  3  7  6  5  4  1| $  4
C
C  -------------------------------
C     SETUP OUTSIDE CONSTANTS
C
      NR=NNN
      NP=MMM
      DEC=SS
C
C     CHECK TO SEE IF NR AND NF ARE WITHIN LIMITS
C
      NNP=IABS(NP)
      KTST=0
      M=IABS(NR)
C
C     IF NR IS GREATER THAN ZERO -- DECIMAL NUMBER
C
      IF(NR.GT.0)GOTO 1
C -------------------------------------
C     THIS IS A DEG-MIN-SEC FORMAT
C
      IF(NNP.GT.5)NNP=5
C
C     ENTRY IS DDD-MM-SS.SS
C           OR  HH-MM-SS.SS
C
      DEC=DABS(DEC)
      SEC=DEC*3600.0D0
      IDG=SEC/3600.0D0
      SEC=SEC-DBLE(FLOAT(IDG))*3600.0D0
      MIN=SEC/60.0D0
      SEC=SEC-DBLE(FLOAT(MIN))*60.0D0
      DEC=DBLE(FLOAT(IDG))*1000000.0D0+DBLE(FLOAT(MIN))*1000.0D0+SEC
C
      KTST=1
      M=15
C
C     ROUND THE DECIMAL NUMBER
C
    1 IP=-1*(NNP+1)
      TOL=5.0D0*(TEN**IP)
      W=(DABS(DEC) + TOL)
      IF(DEC.LT.0.0D0) W=-W
      DEC=W
C
      N=NNP
      IF(M.GT.15)M=15
      IF(M.LT.4)M=4
      IF(N.GE.M)N=M-1
      W=DEC
C
C     CONVERT THE DECIMAL NUMBER
C
      WRITE(JB,100) W
  100 FORMAT(F20.10)
C
C     BLANK FILL THE ARRAY
C
      DO 5 IQ=1,16
    5 CHAR(IQ)=BLK1
C
C     LOOK FOR THE FIRST NON-BLANK CHARACTER
C
      DO 6 I=1,10
      TT=IB(I)
    6 IF(TT.NE.BLK1)GOTO 7
C
C     COMPUTE THE PROPER NUMBER LENGTH WITH THE PROPER DECIMALS
C
    7 K=11-I
      K=K+N
      IF(K.GT.M)M=K
      L=10-(M-N)
      IF(L.LE.0)L=0
C
      MM=M+1
      J=0
      IDEC=0
      DO 30 I=1,MM
      K=I+L
      IF(K.GT.20)K=20
      J=J+1
      CHAR(J)=IB(K)
   30 IF(CHAR(J).EQ.'.') IDEC=J
      N=IDEC+NNP+1
C
      IF(KTST.EQ.0)GOTO 40
C
C     FILL-OUT THE DEG-MIN-SEC FIELD
C
      CHAR(4)=DASH
      CHAR(7)=DASH
C
C     ZERO-OUT ALL BLANK CHARACTERS
C
      DO 10 I=1,9
   10 IF(CHAR(I).EQ.BLK1)CHAR(I)=ZERO
C
   40 CHAR(N)=DOL
C
      RETURN
      END
