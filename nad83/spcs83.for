C     SccsID = "@(#)spcs83.for	1.2	01/28/02"  
       PROGRAM SPCS83
*
*     THIS PROGRAM CONVERTS GPS TO PLANE COORDINATES
*     AND VICE VERSA FOR THE NAD83 DATUM.
*     THIS PROGRAM WAS WRITTEN BY E. CARLSON
*     SUBROUTINES TMGRID,OCONST,SKEWD,LCONST, TCONST,
*     TMGEOD,LAMR1,SKEWR,TCONPC,
*     LAMD1 WERE WRITTEN BY T. VINCENTY, NGS, IN JULY 1984
*     AND LAST UPDATED IN FEBUARY 1986.
*
*     VERSION NUMBER  -  1    09-17-87
*
*
***********************************************************************
*
*     VERSION NUMBER  -  2    06-27-88
*
*     CORRECTIONS TO THE PROGRAM
*
*       1. THE SCALE FACTOR FOR HAWAII ZONE 5 WAS CORRECTED TO 1.0D0
*       2. THE NAME IS NOW BEING SAVED IN THE OUTFILE IN THE
*          INTERACTIVE MODE.
*
*     ENHANCEMENTS TO PROGRAM
*
*       1. THE OUTPUT SENT TO TO OUTPUT FILE NOW HAS PAGE HEADERS FOR
*          EVERY PAGE.
*       2. THE OUTPUT IN THE OUTFILE HAS BEEN CHANGED TO INCLUDE THE
*          THE GEOID HIEGHTS IF THE BLUE BOOK HAS INCLUDED GEOID HEIGHT
*          RECORDS (*84*).
*       3. THE OUTPUT FILE NOW CAN BE PRINTED OFF WITH THE SUBROUTINE
*          LSTFTN.
*       4. THE PROGRAM NOW COMPUTE THE CONVERENCE AND SCALE FACTOR FOR
*          THE PLANE COORDINATES TO GEODETIC POSITIONS SECTION.
*
***********************************************************************
*
*     VERSION NUMBER  -  2.1  01-28-02
*
*       Turned off GUAM 5400 - It was never really approved.
*       Added GUAM 5401 but not turned on yet.
*       Added Kentucky Single Zone KY1Z 1600.
***********************************************************************
*
*          VERSION  5.2       April 25, 2011  
*
*     ENHANCEMENTS TO THE PROGRAM
*
*        1.  Added old Guam zone 5400 and modified Traverse Mercator 
*            projection values from Dave Doyle's software request: 3353.
*
**************************************************************************    
*
*
*    THIS PROGRAM USES THE FOLLOWING SUBROUTINES:
*
*        GPPC83,BATGP,INTGP,DRGPPC,HDGP,FORMGP
*        PCGP83,BATPC,INTPC,DRPCGP,HDPC,FORMPC
*        TCONST,TCONPC,TMGRID,TMGEOD
*        LCONST,LAMD1,LAMR1
*        OCONST,SKEWD,SKEWR
*        TBLSPC,TODMS,VERDMS,CLAIM,LSTFTN
*
*
*
**********************************************************************
*                  DISCLAIMER                                         *
*                                                                     *
*   THIS PROGRAM AND SUPPORTING INFORMATION IS FURNISHED BY THE       *
* GOVERNMENT OF THE UNITED STATES OF AMERICA, AND IS ACCEPTED AND     *
* USED BY THE RECIPIENT WITH THE UNDERSTANDING THAT THE UNITED STATES *
* GOVERNMENT MAKES NO WARRANTIES, EXPRESS OR IMPLIED, CONCERNING THE  *
* ACCURACY, COMPLETENESS, RELIABILITY, OR SUITABILITY OF THIS         *
* PROGRAM, OF ITS CONSTITUENT PARTS, OR OF ANY SUPPORTING DATA.       *
*                                                                     *
*   THE GOVERNMENT OF THE UNITED STATES OF AMERICA SHALL BE UNDER NO  *
* LIABILITY WHATSOEVER RESULTING FROM ANY USE OF THIS PROGRAM.  THIS  *
* PROGRAM SHOULD NOT BE RELIED UPON AS THE SOLE BASIS FOR SOLVING A   *
* PROBLEM WHOSE INCORRECT SOLUTION COULD RESULT IN INJURY TO PERSON   *
* OR PROPERTY.                                                        *
*                                                                     *
*   THIS PROGRAM IS PROPERTY OF THE GOVERNMENT OF THE UNITED STATES   *
* OF AMERICA.  THEREFORE, THE RECIPIENT FURTHER AGREES NOT TO ASSERT  *
* PROPRIETARY RIGHTS THEREIN AND NOT TO REPRESENT THIS PROGRAM TO     *
* ANYONE AS BEING OTHER THAN A GOVERNMENT PROGRAM.                    *
*                                                                     *
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

   5  WRITE(*,10)
   10 FORMAT('0 ***  PROGRAM SPCS83   *****'//,
     &       '       VERSION NUMBER 5.2'//,
     &       '       LAST UPDATE 04/25/2011 '//,
     &       ' DO YOU WANT TO COMPUTE: '//,
     &       ' 1  GEODETIC POSITIONS TO STATE PLANE COORDINATES'/,
     &       ' 2  STATE PLANE COORDINATES TO GEODETIC POSITIONS'/,
     &       ' 3  PRINT THE OUTPUT FILE ON THE PRINTER'//,
     &       ' TYPE NUMBER '/)
      READ(*,15) INUM
   15 FORMAT(I1)

      IF(INUM.EQ.1) THEN
         CALL GPPC83
         WRITE(6,16)
   16    FORMAT('0  DO YOU WANT TO GO TO ANOTHER '/,
     &          '   FUNCTION (Y/N) '//,
     &           '  TYPE ANSWER '/)
         READ(*,21) YN
          IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
             GO TO 5
          ELSE
             GO TO 25
          ENDIF
      ENDIF

      IF(INUM.EQ.2) THEN
         CALL PCGP83
         WRITE(*,16)
         READ(*,21) YN
          IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
             GO TO 5
          ELSE
             GO TO 25
          ENDIF
      ENDIF

      IF(INUM.EQ.3) THEN
         CALL LSTFTN
         WRITE(*,16)
         READ(*,21) YN
          IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
             GO TO 5
          ELSE
             GO TO 25
          ENDIF
      ENDIF


      WRITE(*,20)
   20 FORMAT('0  YOU ENTER A WRONG NUMBER'/,
     &       ' DO WANT TO TRY AGAIN (Y/N) '//,
     &       ' TYPE ANSWER '/)
      READ(*,21) YN
   21 FORMAT(A1)

      IF((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
          GO TO 5
      ENDIF

   25 WRITE(*,30)
   30 FORMAT('0END OF PROGRAM SPCS83')
      STOP
      END
