C     SccsID = "@(#)tblspc.for	1.2	01/28/02"  
      SUBROUTINE TBLSPC(IZC,AP,SPCC,UTMC,ZN)

*** CREATE THE STATE PLANE COORDINATE TABLES

      IMPLICIT DOUBLE PRECISION(A-H,O-Z)
      CHARACTER*1 AP
      CHARACTER*4 ZN
      INTEGER*4 IZC
      DIMENSION ZN(135)
      DIMENSION SPCC(135,6)
      DIMENSION IZC(135)
      DIMENSION AP(135)
      DIMENSION UTMC(60)

      T(X,Y)=X+Y/60.D0

*** LOAD THE TABLE OF SPC STATE ZONE CODES

      IZC(1)=101
      IZC(2)=102
      IZC(3)=5001
      IZC(4)=5002
      IZC(5)=5003
      IZC(6)=5004
      IZC(7)=5005
      IZC(8)=5006
      IZC(9)=5007
      IZC(10)=5008
      IZC(11)=5009
      IZC(12)=5010
      IZC(13)=201
      IZC(14)=202
      IZC(15)=203
      IZC(16)=301
      IZC(17)=302
      IZC(18)=401
      IZC(19)=402
      IZC(20)=403
      IZC(21)=404
      IZC(22)=405
      IZC(23)=406
      IZC(24)=501
      IZC(25)=502
      IZC(26)=503
      IZC(27)=600
      IZC(28)=700
      IZC(29)=901
      IZC(30)=902
      IZC(31)=903
      IZC(32)=1001
      IZC(33)=1002
      IZC(34)=5101
      IZC(35)=5102
      IZC(36)=5103
      IZC(37)=5104
      IZC(38)=5105
      IZC(39)=1101
      IZC(40)=1102
      IZC(41)=1103
      IZC(42)=1201
      IZC(43)=1202
      IZC(44)=1301
      IZC(45)=1302
      IZC(46)=1401
      IZC(47)=1402
      IZC(48)=1501
      IZC(49)=1502
      IZC(50)=1601
      IZC(51)=1602
      IZC(52)=1701
      IZC(53)=1702
      IZC(54)=1703
      IZC(55)=1801
      IZC(56)=1802
      IZC(57)=1900
      IZC(58)=2001
      IZC(59)=2002
      IZC(60)=0
      IZC(61)=0
      IZC(62)=0
      IZC(63)=2111
      IZC(64)=2112
      IZC(65)=2113
      IZC(66)=2201
      IZC(67)=2202
      IZC(68)=2203
      IZC(69)=2301
      IZC(70)=2302
      IZC(71)=2401
      IZC(72)=2402
      IZC(73)=2403
      IZC(74)=2500
      IZC(75)=0
      IZC(76)=0
      IZC(77)=2600
      IZC(78)=0
      IZC(79)=2701
      IZC(80)=2702
      IZC(81)=2703
      IZC(82)=2800
      IZC(83)=2900
      IZC(84)=3001
      IZC(85)=3002
      IZC(86)=3003
      IZC(87)=3101
      IZC(88)=3102
      IZC(89)=3103
      IZC(90)=3104
      IZC(91)=3200
      IZC(92)=3301
      IZC(93)=3302
      IZC(94)=3401
      IZC(95)=3402
      IZC(96)=3501
      IZC(97)=3502
      IZC(98)=3601
      IZC(99)=3602
      IZC(100)=3701
      IZC(101)=3702
      IZC(102)=3800
      IZC(103)=3900
      IZC(104)=4001
      IZC(105)=4002
      IZC(106)=4100
      IZC(107)=4201
      IZC(108)=4202
      IZC(109)=4203
      IZC(110)=4204
      IZC(111)=4205
      IZC(112)=4301
      IZC(113)=4302
      IZC(114)=4303
      IZC(115)=4400
      IZC(116)=4501
      IZC(117)=4502
      IZC(118)=4601
      IZC(119)=4602
      IZC(120)=4701
      IZC(121)=4702
      IZC(122)=4801
      IZC(123)=4802
      IZC(124)=4803
      IZC(125)=4901
      IZC(126)=4902
      IZC(127)=4903
      IZC(128)=4904
      IZC(129)=5200
      IZC(130)=0
      IZC(131)=0
      IZC(132)=5300
      IZC(133)=5400

C     ----------------------------------------------
C     New Kentucky Single Zone
C     ----------------------------------------------
      IZC(134)=1600


C     -------------------------------------------
C     New GUAM zone 5401 not on line yet
C     --------------------------------------------
C     IZC(135)=5401

*** LOAD THE PROPER TYPE OF PROJECTION
***          L=LAMBERT CONIC PROJECTION
***          T=TRANSVERSE MERCATOR PROJECTION
***          O=OBLIQUE MERCATOR PROJECTION
***          N=CONSTANTS NOT YET AVAILABLE (NEEDS PERIODIC UPDATING)

      AP(1)='T'
      AP(2)='T'
      AP(3)='O'
      AP(4)='T'
      AP(5)='T'
      AP(6)='T'
      AP(7)='T'
      AP(8)='T'
      AP(9)='T'
      AP(10)='T'
      AP(11)='T'
      AP(12)='L'
      AP(13)='T'
      AP(14)='T'
      AP(15)='T'
      AP(16)='L'
      AP(17)='L'
      AP(18)='L'
      AP(19)='L'
      AP(20)='L'
      AP(21)='L'
      AP(22)='L'
      AP(23)='L'
      AP(24)='L'
      AP(25)='L'
      AP(26)='L'
      AP(27)='L'
      AP(28)='T'
      AP(29)='T'
      AP(30)='T'
      AP(31)='L'
      AP(32)='T'
      AP(33)='T'
      AP(34)='T'
      AP(35)='T'
      AP(36)='T'
      AP(37)='T'
      AP(38)='T'
      AP(39)='T'
      AP(40)='T'
      AP(41)='T'
      AP(42)='T'
      AP(43)='T'
      AP(44)='T'
      AP(45)='T'
      AP(46)='L'
      AP(47)='L'
      AP(48)='L'
      AP(49)='L'
      AP(50)='L'
      AP(51)='L'
      AP(52)='L'
      AP(53)='L'
      AP(54)='L'
      AP(55)='T'
      AP(56)='T'
      AP(57)='L'
      AP(58)='L'
      AP(59)='L'
      AP(60)='N'
      AP(61)='N'
      AP(62)='N'
      AP(63)='L'
      AP(64)='L'
      AP(65)='L'
      AP(66)='L'
      AP(67)='L'
      AP(68)='L'
      AP(69)='T'
      AP(70)='T'
      AP(71)='T'
      AP(72)='T'
      AP(73)='T'
      AP(74)='L'
      AP(75)='N'
      AP(76)='N'
      AP(77)='L'
      AP(78)='N'
      AP(79)='T'
      AP(80)='T'
      AP(81)='T'
      AP(82)='T'
      AP(83)='T'
      AP(84)='T'
      AP(85)='T'
      AP(86)='T'
      AP(87)='T'
      AP(88)='T'
      AP(89)='T'
      AP(90)='L'
      AP(91)='L'
      AP(92)='L'
      AP(93)='L'
      AP(94)='L'
      AP(95)='L'
      AP(96)='L'
      AP(97)='L'
      AP(98)='L'
      AP(99)='L'
      AP(100)='L'
      AP(101)='L'
      AP(102)='T'
      AP(103)='L'
      AP(104)='L'
      AP(105)='L'
      AP(106)='L'
      AP(107)='L'
      AP(108)='L'
      AP(109)='L'
      AP(110)='L'
      AP(111)='L'
      AP(112)='L'
      AP(113)='L'
      AP(114)='L'
      AP(115)='T'
      AP(116)='L'
      AP(117)='L'
      AP(118)='L'
      AP(119)='L'
      AP(120)='L'
      AP(121)='L'
      AP(122)='L'
      AP(123)='L'
      AP(124)='L'
      AP(125)='T'
      AP(126)='T'
      AP(127)='T'
      AP(128)='T'
      AP(129)='L'
      AP(130)='N'
      AP(131)='N'
      AP(132)='N'
      AP(133)='T'
      AP(134)='L'
      AP(135)='T'

*** INITIALIZE CONSTANTS TABLES
***
*** THESE CONSTANTS ARE FROM JIM STEM.
***  VERSION= 1.4
***  DATE = JUNE 91, 1987
***

      DO 10 I=1,135
      DO 10 J=1,6
 10   SPCC(I,J)=0.D0

*** LOAD CONSTANTS BY EACH STATE APHABETICALLY
*** TRANSVERSE MERCATOR WILL HAVE 4 CONSTANTS
***          1 - CENTRAL MERIDIAN (CM)
***          2 - FALSE EASTING VALUE AT THE CM (METERS)
***          3 - SOUTHERNMOST PARALLEL
***          4 - SCALE FACTOR
***          5 - FALSE NORTHING VALUE AT SOUTHERMOST PARALLEL (METERS)
*** LAMBERT CONIC WILL HAVE 6 CONSTANTS
***          1 - C. M.
***          2 - FALSE EASTING AT CM (METERS)
***          3 - FALSE NORTHING FOR SOUTHERNMOST PARALLEL (METERS),
***              USUALLY EQUALS ZERO
***          4 - LATITUDE OF SO. STD. PARALLEL
***          5 - LATITUDE OF NO. STD. PARALLEL
***          6 - LATITUDE OF SOUTHERNMOST PARALLEL
*** OBLIQUE MERCATOR HAS 6 CONSTANTS
***          1 - C. M.
***          2 - FALSE EASTING (METERS)
***          3 - FALSE NORTHING (METERS)
***          4 - AXIS AZIMUTH
***          5 - SOUTHERNMOST PARALLEL
***          6 - SCALE FACTOR

****           AL EAST
      SPCC(1,1)=T(85.D0,50.D0)
      SPCC(1,2)=200000.D0
      SPCC(1,3)=T(30.D0,30.D0)
      SPCC(1,4)=25000.D0
      SPCC(1,5)=0.D0
****           AL WEST
      SPCC(2,1)=T(87.D0,30.D0)
      SPCC(2,2)=600000.D0
      SPCC(2,3)=30.D0
      SPCC(2,4)=15000.D0
      SPCC(2,5)=0.D0
****           AK 1
      SPCC(3,1)=T(133.D0,40.D0)
      SPCC(3,2)=5000000.D0
      SPCC(3,3)=-5000000.D0
      SPCC(3,4)=DATAN(-0.75D0)
      SPCC(3,5)=57.D0
      SPCC(3,6)=10000.D0
****           AK 2
      SPCC(4,1)=142.D0
      SPCC(4,2)=500000.D0
      SPCC(4,3)=54.D0
      SPCC(4,4)=10000.D0
      SPCC(4,5)=0.D0
****           AK 3
      SPCC(5,1)=146.D0
      SPCC(5,2)=500000.D0
      SPCC(5,3)=54.D0
      SPCC(5,4)=10000.D0
      SPCC(5,5)=0.D0
****           AK 4
      SPCC(6,1)=150.D0
      SPCC(6,2)=500000.D0
      SPCC(6,3)=54.D0
      SPCC(6,4)=10000.D0
      SPCC(6,5)=0.D0
****           AK 5
      SPCC(7,1)=154.D0
      SPCC(7,2)=500000.D0
      SPCC(7,3)=54.D0
      SPCC(7,4)=10000.D0
      SPCC(7,5)=0.D0
****           AK 6
      SPCC(8,1)=158.D0
      SPCC(8,2)=500000.D0
      SPCC(8,3)=54.D0
      SPCC(8,4)=10000.D0
      SPCC(8,5)=0.D0
****           AK 7
      SPCC(9,1)=162.D0
      SPCC(9,2)=500000.D0
      SPCC(9,3)=54.D0
      SPCC(9,4)=10000.D0
      SPCC(9,5)=0.D0
****           AK 8
      SPCC(10,1)=166.D0
      SPCC(10,2)=500000.D0
      SPCC(10,3)=54.D0
      SPCC(10,4)=10000.D0
      SPCC(10,5)=0.D0
****           AK 9
      SPCC(11,1)=170.D0
      SPCC(11,2)=500000.D0
      SPCC(11,3)=54.D0
      SPCC(11,4)=10000.D0
      SPCC(11,5)=0.D0
****           AK 10
      SPCC(12,1)=176.D0
      SPCC(12,2)=1000000.D0
      SPCC(12,3)=0.D0
      SPCC(12,4)=T(51.D0,50.D0)
      SPCC(12,5)=T(53.D0,50.D0)
      SPCC(12,6)=51.D0
****           AZ WEST
      SPCC(15,1)=T(113.D0,45.D0)
      SPCC(15,2)=213360.D0
      SPCC(15,3)=31.D0
      SPCC(15,4)=15000.D0
      SPCC(15,5)=0.D0
****           AZ CENTRAL
      SPCC(14,1)=T(111.D0,55.D0)
      SPCC(14,2)=213360.D0
      SPCC(14,3)=31.D0
      SPCC(14,4)=10000.D0
      SPCC(14,5)=0.D0
****           AZ EAST
      SPCC(13,1)=T(110.D0,10.D0)
      SPCC(13,2)=213360.D0
      SPCC(13,3)=31.D0
      SPCC(13,4)=10000.D0
      SPCC(13,5)=0.D0
****           AR NORTH
      SPCC(16,1)=92.D0
      SPCC(16,2)=400000.D0
      SPCC(16,3)=0.D0
      SPCC(16,4)=T(34.D0,56.D0)
      SPCC(16,5)=T(36.D0,14.D0)
      SPCC(16,6)=T(34.D0,20.D0)
****           AR SOUTH
      SPCC(17,1)=92.D0
      SPCC(17,2)=400000.D0
      SPCC(17,3)=400000.D0
      SPCC(17,4)=T(33.D0,18.D0)
      SPCC(17,5)=T(34.D0,46.D0)
      SPCC(17,6)=T(32.D0,40.D0)
****           CA 1
      SPCC(18,1)=122.D0
      SPCC(18,2)=2000000.D0
      SPCC(18,3)=500000.D0
      SPCC(18,4)=40.D0
      SPCC(18,5)=T(41.D0,40.D0)
      SPCC(18,6)=T(39.D0,20.D0)
****           CA 2
      SPCC(19,1)=122.D0
      SPCC(19,2)=2000000.D0
      SPCC(19,3)=500000.D0
      SPCC(19,4)=T(38.D0,20.D0)
      SPCC(19,5)=T(39.D0,50.D0)
      SPCC(19,6)=T(37.D0,40.D0)
      SPCC(20,1)=120.5D0
****           CA 3
      SPCC(20,2)=2000000.D0
      SPCC(20,3)=500000.D0
      SPCC(20,4)=T(37.D0,4.D0)
      SPCC(20,5)=T(38.D0,26.D0)
      SPCC(20,6)=36.5D0
****           CA 4
      SPCC(21,1)=119.D0
      SPCC(21,2)=2000000.D0
      SPCC(21,3)=500000.D0
      SPCC(21,4)=36.D0
      SPCC(21,5)=37.25D0
      SPCC(21,6)=T(35.D0,20.D0)
****           CA 5
      SPCC(22,1)=118.D0
      SPCC(22,2)=2000000.D0
      SPCC(22,3)=500000.D0
      SPCC(22,4)=T(34.D0,2.D0)
      SPCC(22,5)=T(35.D0,28.D0)
      SPCC(22,6)=33.5D0
****           CA 6
      SPCC(23,1)=116.25D0
      SPCC(23,2)=2000000.D0
      SPCC(23,3)=500000.D0
      SPCC(23,4)=T(32.D0,47.D0)
      SPCC(23,5)=T(33.D0,53.D0)
      SPCC(23,6)=T(32.D0,10.D0)
      SPCC(24,1)=105.5D0
****           CO NORTH
      SPCC(24,2)=914401.8289D0
      SPCC(24,3)=304800.6096D0
      SPCC(24,4)=T(39.D0,43.D0)
      SPCC(24,5)=T(40.D0,47.D0)
      SPCC(24,6)=T(39.D0,20.D0)
****           CO CENTRAL
      SPCC(25,1)=105.5D0
      SPCC(25,2)=914401.8289D0
      SPCC(25,3)=304800.6096D0
      SPCC(25,4)=T(38.D0,27.D0)
      SPCC(25,5)=T(39.D0,45.D0)
      SPCC(25,6)=T(37.D0,50.D0)
****           CO SOUTH
      SPCC(26,1)=105.5D0
      SPCC(26,2)=914401.8289D0
      SPCC(26,3)=304800.6096D0
      SPCC(26,4)=T(37.D0,14.D0)
      SPCC(26,5)=T(38.D0,26.D0)
      SPCC(26,6)=T(36.D0,40.D0)
      SPCC(27,1)=T(72.D0,45.D0)
****           CT
      SPCC(27,2)=304800.6096D0
      SPCC(27,3)=152400.3048D0
      SPCC(27,4)=T(41.D0,12.D0)
      SPCC(27,5)=T(41.D0,52.D0)
      SPCC(27,6)=T(40.D0,50.D0)
****           DE
      SPCC(28,1)=T(75.D0,25.D0)
      SPCC(28,2)=200000.D0
      SPCC(28,3)=38.D0
      SPCC(28,4)=200000.D0
      SPCC(28,5)=0.D0
****           FL EAST
      SPCC(29,1)=81.D0
      SPCC(29,2)=200000.D0
      SPCC(29,3)=T(24.D0,20.D0)
      SPCC(29,4)=17000.D0
      SPCC(29,5)=0.D0
****           FL WEST
      SPCC(30,1)=82.D0
      SPCC(30,2)=200000.D0
      SPCC(30,3)=T(24.D0,20.D0)
      SPCC(30,4)=17000.D0
      SPCC(30,5)=0.D0
****           FL NORTH
      SPCC(31,1)=T(84.D0,30.D0)
      SPCC(31,2)=600000.D0
      SPCC(31,3)=0.D0
      SPCC(31,4)=T(29.D0,35.D0)
      SPCC(31,5)=T(30.D0,45.D0)
      SPCC(31,6)=29.D0
      SPCC(32,1)=T(82.D0,10.D0)
****           GA EAST
      SPCC(32,2)=200000.D0
      SPCC(32,3)=30.D0
      SPCC(32,4)=10000.D0
      SPCC(32,5)=0.D0
****           GA WEST
      SPCC(33,1)=T(84.D0,10.D0)
      SPCC(33,2)=700000.D0
      SPCC(33,3)=30.D0
      SPCC(33,4)=10000.D0
      SPCC(33,5)=0.D0
****           HI 1
      SPCC(34,1)=T(155.D0,30.D0)
      SPCC(34,2)=500000.D0
      SPCC(34,3)=T(18.D0,50.D0)
      SPCC(34,4)=30000.D0
      SPCC(34,5)=0.D0
****           HI 2
      SPCC(35,1)=T(156.D0,40.D0)
      SPCC(35,2)=500000.D0
      SPCC(35,3)=T(20.D0,20.D0)
      SPCC(35,4)=30000.D0
      SPCC(35,5)=0.D0
****           HI 3
      SPCC(36,1)=158.D0
      SPCC(36,2)=500000.D0
      SPCC(36,3)=T(21.D0,10.D0)
      SPCC(36,4)=100000.D0
      SPCC(36,5)=0.D0
****           HI 4
      SPCC(37,1)=T(159.D0,30.D0)
      SPCC(37,2)=500000.D0
      SPCC(37,3)=T(21.D0,50.D0)
      SPCC(37,4)=100000.D0
      SPCC(37,5)=0.D0
****           HI 5
      SPCC(38,1)=T(160.D0,10.D0)
      SPCC(38,2)=500000.D0
      SPCC(38,3)=T(21.D0,40.D0)
      SPCC(38,4)=1.D0
      SPCC(38,5)=0.D0
****           ID EAST
      SPCC(39,1)=T(112.D0,10.D0)
      SPCC(39,2)=200000.D0
      SPCC(39,3)=T(41.D0,40.D0)
      SPCC(39,4)=19000.D0
      SPCC(39,5)=0.D0
****           ID CENTRAL
      SPCC(40,1)=114.D0
      SPCC(40,2)=500000.D0
      SPCC(40,3)=T(41.D0,40.D0)
      SPCC(40,4)=19000.D0
      SPCC(40,5)=0.D0
****           ID WEST

      SPCC(41,1)=T(115.D0,45.D0)
      SPCC(41,2)=800000.D0
      SPCC(41,3)=T(41.D0,40.D0)
      SPCC(41,4)=15000.D0
      SPCC(41,5)=0.D0
****           IL EAST

      SPCC(42,1)=T(88.D0,20.D0)
      SPCC(42,2)=300000.D0
      SPCC(42,3)=T(36.D0,40.D0)
      SPCC(42,4)=40000.D0
      SPCC(42,5)=0.D0
****           IL WEST
      SPCC(43,1)=T(90.D0,10.D0)
      SPCC(43,2)=700000.D0
      SPCC(43,3)=T(36.D0,40.D0)
      SPCC(43,4)=17000.D0
      SPCC(43,5)=0.D0
****           IN EAST
      SPCC(44,1)=T(85.D0,40.D0)
      SPCC(44,2)=100000.D0
      SPCC(44,3)=37.5D0
      SPCC(44,4)=30000.D0
      SPCC(44,5)=250000.D0
****           IN WEST
      SPCC(45,1)=T(87.D0,5.D0)
      SPCC(45,2)=900000.D0
      SPCC(45,3)=37.5D0
      SPCC(45,4)=30000.D0
      SPCC(45,5)=250000.D0
****           IA NORTH
      SPCC(46,1)=93.5D0
      SPCC(46,2)=1500000.D0
      SPCC(46,3)=1000000.D0
      SPCC(46,4)=T(42.D0,4.D0)
      SPCC(46,5)=T(43.D0,16.D0)
      SPCC(46,6)=41.5D0
****           IA SOUTH
      SPCC(47,1)=93.5D0
      SPCC(47,2)=500000.D0
      SPCC(47,3)=0.D0
      SPCC(47,4)=T(40.D0,37.D0)
      SPCC(47,5)=T(41.D0,47.D0)
      SPCC(47,6)=40.D0
****           KS NORTH
      SPCC(48,1)=98.D0
      SPCC(48,2)=400000.D0
      SPCC(48,3)=0.D0
      SPCC(48,4)=T(38.D0,43.D0)
      SPCC(48,5)=T(39.D0,47.D0)
      SPCC(48,6)=T(38.D0,20.D0)
****           KS SOUTH
      SPCC(49,1)=98.5D0
      SPCC(49,2)=400000.D0
      SPCC(49,3)=400000.D0
      SPCC(49,4)=T(37.D0,16.D0)
      SPCC(49,5)=T(38.D0,34.D0)
      SPCC(49,6)=T(36.D0,40.D0)
****           KY NORTH
      SPCC(50,1)=T(84.D0,15.D0)
      SPCC(50,2)=500000.D0
      SPCC(50,3)=0.D0
      SPCC(50,4)=T(37.D0,58.D0)
      SPCC(50,5)=T(38.D0,58.D0)
      SPCC(50,6)=37.5D0
****           KY SOUTH

      SPCC(51,1)=T(85.D0,45.D0)
      SPCC(51,2)=500000.D0
      SPCC(51,3)=500000.D0
      SPCC(51,4)=T(36.D0,44.D0)
      SPCC(51,5)=T(37.D0,56.D0)
      SPCC(51,6)=T(36.D0,20.D0)

****           LA NORTH


      SPCC(52,1)=92.5D0
      SPCC(52,2)=1000000.D0
      SPCC(52,3)=0.D0
      SPCC(52,4)=T(31.D0,10.D0)
      SPCC(52,5)=T(32.D0,40.D0)
      SPCC(52,6)=30.5D0
****           LA S
      SPCC(53,1)=T(91.D0,20.D0)
      SPCC(53,2)=1000000.D0
      SPCC(53,3)=0.D0
      SPCC(53,4)=T(29.D0,18.D0)
      SPCC(53,5)=T(30.D0,42.D0)
      SPCC(53,6)=28.5D0
****           LA OFF

      SPCC(54,1)=T(91.D0,20.D0)
      SPCC(54,2)=1000000.D0
      SPCC(54,3)=0.D0
      SPCC(54,4)=T(26.D0,10.D0)
      SPCC(54,5)=T(27.D0,50.D0)
      SPCC(54,6)=25.5D0
****           ME EAST

      SPCC(55,1)=68.5D0
      SPCC(55,2)=300000.D0
      SPCC(55,3)=T(43.D0,40.D0)
      SPCC(55,4)=10000.D0
      SPCC(55,5)=0.D0
****           ME WEST

      SPCC(56,1)=T(70.D0,10.D0)
      SPCC(56,2)=900000.D0
      SPCC(56,3)=T(42.D0,50.D0)
      SPCC(56,4)=30000.D0
      SPCC(56,5)=0.D0
****           MD
      SPCC(57,1)=77.D0
      SPCC(57,2)=400000.D0
      SPCC(57,3)=0.D0
      SPCC(57,4)=T(38.D0,18.D0)
      SPCC(57,5)=T(39.D0,27.D0)
      SPCC(57,6)=T(37.D0,40.D0)
****           MA M

      SPCC(58,1)=71.5D0
      SPCC(58,2)=200000.D0
      SPCC(58,3)=750000.D0
      SPCC(58,4)=T(41.D0,43.D0)
      SPCC(58,5)=T(42.D0,41.D0)
      SPCC(58,6)=41.D0
****           MA ISLAND

      SPCC(59,1)=70.5D0
      SPCC(59,2)=500000.D0
      SPCC(59,3)=0.D0
      SPCC(59,4)=T(41.D0,17.D0)
      SPCC(59,5)=T(41.D0,29.D0)
      SPCC(59,6)=41.D0
****           MI NORTH
      SPCC(63,1)=87.D0
      SPCC(63,2)=8000000.D0
      SPCC(63,3)=0.D0
      SPCC(63,4)=T(45.D0,29.D0)
      SPCC(63,5)=T(47.D0,5.D0)
      SPCC(63,6)=T(44.D0,47.D0)
****           MI CENTRAL

      SPCC(64,1)=T(84.D0,22.D0)
      SPCC(64,2)=6000000.D0
      SPCC(64,3)=0.D0
      SPCC(64,4)=T(44.D0,11.D0)
      SPCC(64,5)=T(45.D0,42.D0)
      SPCC(64,6)=T(43.D0,19.D0)
****           MI SOUTH

      SPCC(65,1)=T(84.D0,22.D0)
      SPCC(65,2)=4000000.D0
      SPCC(65,3)=0.D0
      SPCC(65,4)=T(42.D0,06.D0)
      SPCC(65,5)=T(43.D0,40.D0)
      SPCC(65,6)=41.5D0
****           MN NORTH
      SPCC(66,1)=T(93.D0,6.D0)
      SPCC(66,2)=800000.D0
      SPCC(66,3)=100000.D0
      SPCC(66,4)=T(47.D0,2.D0)
      SPCC(66,5)=T(48.D0,38.D0)
      SPCC(66,6)=46.5D0
****           MN CENTRAL

      SPCC(67,1)=T(94.D0,15.D0)
      SPCC(67,2)=800000.D0
      SPCC(67,3)=100000.D0
      SPCC(67,4)=T(45.D0,37.D0)
      SPCC(67,5)=T(47.D0,3.D0)
      SPCC(67,6)=45.D0
****           MN SOUTH

      SPCC(68,1)=94.D0
      SPCC(68,2)=800000.D0
      SPCC(68,3)=100000.D0
      SPCC(68,4)=T(43.D0,47.D0)
      SPCC(68,5)=T(45.D0,13.D0)
      SPCC(68,6)=43.D0
****           MS EAST
      SPCC(69,1)=T(88.D0,50.D0)
      SPCC(69,2)=300000.D0
      SPCC(69,3)=29.5D0
      SPCC(69,4)=20000.D0
      SPCC(69,5)=0.D0
****           MS WEST

      SPCC(70,1)=T(90.D0,20.D0)
      SPCC(70,2)=700000.D0
      SPCC(70,3)=29.5D0
      SPCC(70,4)=20000.D0
      SPCC(70,5)=0.D0
****           MO EAST

      SPCC(71,1)=90.5D0
      SPCC(71,2)=250000.D0
      SPCC(71,3)=T(35.D0,50.D0)
      SPCC(71,4)=15000.D0
      SPCC(71,5)=0.D0
****           MO CENTRAL

      SPCC(72,1)=92.5D0
      SPCC(72,2)=500000.D0
      SPCC(72,3)=T(35.D0,50.D0)
      SPCC(72,4)=15000.D0
      SPCC(72,5)=0.D0
****           MO WEST

      SPCC(73,1)=94.5D0
      SPCC(73,2)=850000.D0
      SPCC(73,3)=T(36.D0,10.D0)
      SPCC(73,4)=17000.D0
      SPCC(73,5)=0.D0
****           MT

      SPCC(74,1)=T(109.D0,30.D0)
      SPCC(74,2)=600000.D0
      SPCC(74,3)=0.D0
      SPCC(74,4)=45.D0
      SPCC(74,5)=49.D0
      SPCC(74,6)=T(44.D0,15.D0)
****           NE

      SPCC(77,1)=100.D0
      SPCC(77,2)=500000.D0
      SPCC(77,3)=0.D0
      SPCC(77,4)=40.D0
      SPCC(77,5)=43.D0
      SPCC(77,6)=T(39.D0,50.D0)
****           NV EAST
      SPCC(79,1)=T(115.D0,35.D0)
      SPCC(79,2)=200000.D0
      SPCC(79,3)=34.75D0
      SPCC(79,4)=10000.D0
      SPCC(79,5)=8000000.D0
****           NV CENTRAL
      SPCC(80,1)=T(116.D0,40.D0)
      SPCC(80,2)=500000.D0
      SPCC(80,3)=34.75D0
      SPCC(80,4)=10000.D0
      SPCC(80,5)=6000000.D0
****           NV WEST
      SPCC(81,1)=T(118.D0,35.D0)
      SPCC(81,2)=800000.D0
      SPCC(81,3)=34.75D0
      SPCC(81,4)=10000.D0
      SPCC(81,5)=4000000.D0
****           NH
      SPCC(82,1)=T(71.D0,40.D0)
      SPCC(82,2)=300000.D0
      SPCC(82,3)=42.5D0
      SPCC(82,4)=30000.D0
      SPCC(82,5)=0.D0
****           NJ

      SPCC(83,1)=74.5D0
      SPCC(83,2)=150000.D0
      SPCC(83,3)=T(38.D0,50.D0)
      SPCC(83,4)=10000.D0
      SPCC(83,5)=0.D0
****           NM EAST
      SPCC(84,1)=T(104.D0,20.D0)
      SPCC(84,2)=165000.D0
      SPCC(84,3)=31.D0
      SPCC(84,4)=11000.D0
      SPCC(84,5)=0.D0
****           NM CENTRAL

      SPCC(85,1)=T(106.D0,15.D0)
      SPCC(85,2)=500000.D0
      SPCC(85,3)=31.D0
      SPCC(85,4)=10000.D0
      SPCC(85,5)=0.D0
****           NM WEST

      SPCC(86,1)=T(107.D0,50.D0)
      SPCC(86,2)=830000.D0
      SPCC(86,3)=31.D0
      SPCC(86,4)=12000.D0
      SPCC(86,5)=0.D0
****           NY EAST

      SPCC(87,1)=74.5D0
      SPCC(87,2)=150000.D0
      SPCC(87,3)=T(38.D0,50.D0)
      SPCC(87,4)=10000.D0
      SPCC(87,5)=0.D0
****           NY CENTRAL
      SPCC(88,1)=T(76.D0,35.D0)
      SPCC(88,2)=250000.D0
      SPCC(88,3)=40.D0
      SPCC(88,4)=16000.D0
      SPCC(88,5)=0.D0
****           NY WEST

      SPCC(89,1)=T(78.D0,35.D0)
      SPCC(89,2)=350000.D0
      SPCC(89,3)=40.D0
      SPCC(89,4)=16000.D0
      SPCC(89,5)=0.D0
****           NY LI

      SPCC(90,1)=74.D0
      SPCC(90,2)=300000.D0
      SPCC(90,3)=0.D0
      SPCC(90,4)=T(40.D0,40.D0)
      SPCC(90,5)=T(41.D0,2.D0)
      SPCC(90,6)=T(40.D0,10.D0)
****           NC
      SPCC(91,1)=79.D0
      SPCC(91,2)=609601.22D0
      SPCC(91,3)=0.D0
      SPCC(91,4)=T(34.D0,20.D0)
      SPCC(91,5)=T(36.D0,10.D0)
      SPCC(91,6)=33.75D0
****           ND NORTH

      SPCC(92,1)=100.5D0
      SPCC(92,2)=600000.D0
      SPCC(92,3)=0.D0
      SPCC(92,4)=T(47.D0,26.D0)
      SPCC(92,5)=T(48.D0,44.D0)
      SPCC(92,6)=47.D0
****           ND SOUTH
      SPCC(93,1)=100.5D0
      SPCC(93,2)=600000.D0
      SPCC(93,3)=0.D0
      SPCC(93,4)=T(46.D0,11.D0)
      SPCC(93,5)=T(47.D0,29.D0)
      SPCC(93,6)=T(45.D0,40.D0)
****           OH NORTH
      SPCC(94,1)=82.5D0
      SPCC(94,2)=600000.D0
      SPCC(94,3)=0.D0
      SPCC(94,4)=T(40.D0,26.D0)
      SPCC(94,5)=T(41.D0,42.D0)
      SPCC(94,6)=T(39.D0,40.D0)
****           OH SOUTH

      SPCC(95,1)=82.5D0
      SPCC(95,2)=600000.D0
      SPCC(95,3)=0.D0
      SPCC(95,4)=T(38.D0,44.D0)
      SPCC(95,5)=T(40.D0,2.D0)
      SPCC(95,6)=38.D0
****           OK NORTH

      SPCC(96,1)=98.D0
      SPCC(96,2)=600000.D0
      SPCC(96,3)=0.D0
      SPCC(96,4)=T(35.D0,34.D0)
      SPCC(96,5)=T(36.D0,46.D0)
      SPCC(96,6)=35.D0
****           OK SOUTH

      SPCC(97,1)=98.D0
      SPCC(97,2)=600000.D0
      SPCC(97,3)=0.D0
      SPCC(97,4)=T(33.D0,56.D0)
      SPCC(97,5)=T(35.D0,14.D0)
      SPCC(97,6)=T(33.D0,20.D0)
****           OR NORTH
      SPCC(98,1)=120.5D0
      SPCC(98,2)=2500000.D0
      SPCC(98,3)=0.D0
      SPCC(98,4)=T(44.D0,20.D0)
      SPCC(98,5)=46.D0
      SPCC(98,6)=T(43.D0,40.D0)
****           OR SOUTH
      SPCC(99,1)=120.5D0
      SPCC(99,2)=1500000.D0
      SPCC(99,3)=0.D0
      SPCC(99,4)=T(42.D0,20.D0)
      SPCC(99,5)=44.D0
      SPCC(99,6)=T(41.D0,40.D0)
****           PA NORTH

      SPCC(100,1)=T(77.D0,45.D0)
      SPCC(100,2)=600000.D0
      SPCC(100,3)=0.D0
      SPCC(100,4)=T(40.D0,53.D0)
      SPCC(100,5)=T(41.D0,57.D0)
      SPCC(100,6)=T(40.D0,10.D0)
****           PA SOUTH
      SPCC(101,1)=T(77.D0,45.D0)
      SPCC(101,2)=600000.D0
      SPCC(101,3)=0.D0
      SPCC(101,4)=T(39.D0,56.D0)
      SPCC(101,5)=T(40.D0,58.D0)
      SPCC(101,6)=T(39.D0,20.D0)
****           RI
      SPCC(102,1)=71.5D0
      SPCC(102,2)=100000.D0
      SPCC(102,3)=T(41.D0,5.D0)
      SPCC(102,4)=160000.D0
      SPCC(102,5)=0.D0
****           SC

      SPCC(103,1)=81.D0
      SPCC(103,2)=609600.D0
      SPCC(103,3)=0.D0
      SPCC(103,4)=32.5D0
      SPCC(103,5)=T(34.D0,50.D0)
      SPCC(103,6)=T(31.D0,50.D0)
****           SD NORTH

      SPCC(104,1)=100.D0
      SPCC(104,2)=600000.D0
      SPCC(104,3)=0.D0
      SPCC(104,4)=T(44.D0,25.D0)
      SPCC(104,5)=T(45.D0,41.D0)
      SPCC(104,6)=T(43.D0,50.D0)
****           SD SOUTH
      SPCC(105,1)=T(100.D0,20.D0)
      SPCC(105,2)=600000.D0
      SPCC(105,3)=0.D0
      SPCC(105,4)=T(42.D0,50.D0)
      SPCC(105,5)=T(44.D0,24.D0)
      SPCC(105,6)=T(42.D0,20.D0)
****           TN
      SPCC(106,1)=86.D0
      SPCC(106,2)=600000.D0
      SPCC(106,3)=0.D0
      SPCC(106,4)=T(35.D0,15.D0)
      SPCC(106,5)=T(36.D0,25.D0)
      SPCC(106,6)=T(34.D0,20.D0)
****           TX NORTH
      SPCC(107,1)=101.5D0
      SPCC(107,2)=200000.D0
      SPCC(107,3)=1000000.D0
      SPCC(107,4)=T(34.D0,39.D0)
      SPCC(107,5)=T(36.D0,11.D0)
      SPCC(107,6)=34.D0
****           TX NCENTRAL
      SPCC(108,1)=98.5D0
      SPCC(108,2)=600000.D0
      SPCC(108,3)=2000000.D0
      SPCC(108,4)=T(32.D0,8.D0)
      SPCC(108,5)=T(33.D0,58.D0)
      SPCC(108,6)=T(31.D0,40.D0)
****           TX C

      SPCC(109,1)=T(100.D0,20.D0)
      SPCC(109,2)=700000.D0
      SPCC(109,3)=3000000.D0
      SPCC(109,4)=T(30.D0,7.D0)
      SPCC(109,5)=T(31.D0,53.D0)
      SPCC(109,6)=T(29.D0,40.D0)
****           TX SCENTRAL

      SPCC(110,1)=99.D0
      SPCC(110,2)=600000.D0
      SPCC(110,3)=4000000.D0
      SPCC(110,4)=T(28.D0,23.D0)
      SPCC(110,5)=T(30.D0,17.D0)
      SPCC(110,6)=T(27.D0,50.D0)
****           TX S
      SPCC(111,1)=98.5D0
      SPCC(111,2)=300000.D0
      SPCC(111,3)=5000000.D0
      SPCC(111,4)=T(26.D0,10.D0)
      SPCC(111,5)=T(27.D0,50.D0)
      SPCC(111,6)=T(25.D0,40.D0)
****           UT NORTH
      SPCC(112,1)=111.5D0
      SPCC(112,2)=500000.D0
      SPCC(112,3)=1000000.D0
      SPCC(112,4)=T(40.D0,43.D0)
      SPCC(112,5)=T(41.D0,47.D0)
      SPCC(112,6)=T(40.D0,20.D0)
****           UT CENTRAL
      SPCC(113,1)=111.5D0
      SPCC(113,2)=500000.D0
      SPCC(113,3)=2000000.D0
      SPCC(113,4)=T(39.D0,1.D0)
      SPCC(113,5)=T(40.D0,39.D0)
      SPCC(113,6)=T(38.D0,20.D0)
****           UT SOUTH

      SPCC(114,1)=111.5D0
      SPCC(114,2)=500000.D0
      SPCC(114,3)=3000000.D0
      SPCC(114,4)=T(37.D0,13.D0)
      SPCC(114,5)=T(38.D0,21.D0)
      SPCC(114,6)=T(36.D0,40.D0)
****           VT

      SPCC(115,1)=T(72.D0,30.D0)
      SPCC(115,2)=500000.D0
      SPCC(115,3)=T(42.D0,30.D0)
      SPCC(115,4)=28000.D0
      SPCC(115,5)=0.D0
****           VA NORTH

      SPCC(116,1)=78.5D0
      SPCC(116,2)=3500000.D0
      SPCC(116,3)=2000000.D0
      SPCC(116,4)=T(38.D0,2.D0)
      SPCC(116,5)=T(39.D0,12.D0)
      SPCC(116,6)=T(37.D0,40.D0)
****           VA SOUTH
      SPCC(117,1)=78.5D0
      SPCC(117,2)=3500000.D0
      SPCC(117,3)=1000000.D0
      SPCC(117,4)=T(36.D0,46.D0)
      SPCC(117,5)=T(37.D0,58.D0)
      SPCC(117,6)=T(36.D0,20.D0)
****           WA NORTH
      SPCC(118,1)=T(120.D0,50.D0)
      SPCC(118,2)=500000.D0
      SPCC(118,3)=0.D0
      SPCC(118,4)=47.5D0
      SPCC(118,5)=T(48.D0,44.D0)
      SPCC(118,6)=47.D0
****           WA SOUTH
      SPCC(119,1)=120.5D0
      SPCC(119,2)=500000.D0
      SPCC(119,3)=0.D0
      SPCC(119,4)=T(45.D0,50.D0)
      SPCC(119,5)=T(47.D0,20.D0)
      SPCC(119,6)=T(45.D0,20.D0)
****           WV NORTH

      SPCC(120,1)=79.5D0
      SPCC(120,2)=600000.D0
      SPCC(120,3)=0.D0
      SPCC(120,4)=39.D0
      SPCC(120,5)=40.25D0
      SPCC(120,6)=38.5D0
****           WV SOUTH

      SPCC(121,1)=81.D0
      SPCC(121,2)=600000.D0
      SPCC(121,3)=0.D0
      SPCC(121,4)=T(37.D0,29.D0)
      SPCC(121,5)=T(38.D0,53.D0)
      SPCC(121,6)=37.D0
****           WI NORTH

      SPCC(122,1)=90.D0
      SPCC(122,2)=600000.D0
      SPCC(122,3)=0.D0
      SPCC(122,4)=T(45.D0,34.D0)
      SPCC(122,5)=T(46.D0,46.D0)
      SPCC(122,6)=T(45.D0,10.D0)
****           WI CENTRAL

      SPCC(123,1)=90.D0
      SPCC(123,2)=600000.D0
      SPCC(123,3)=0.D0
      SPCC(123,4)=T(44.D0,15.D0)
      SPCC(123,5)=45.5D0
      SPCC(123,6)=T(43.D0,50.D0)
****           WI SOUTH

      SPCC(124,1)=90.D0
      SPCC(124,2)=600000.D0
      SPCC(124,3)=0.D0
      SPCC(124,4)=T(42.D0,44.D0)
      SPCC(124,5)=T(44.D0,4.D0)
      SPCC(124,6)=42.D0
****           WY E


      SPCC(125,1)=T(105.D0,10.D0)
      SPCC(125,2)=200000.D0
      SPCC(125,3)=T(40.D0,30.D0)
      SPCC(125,4)=16000.D0
      SPCC(125,5)=0.D0
****           WY EC
      SPCC(126,1)=T(107.D0,20.D0)
      SPCC(126,2)=400000.D0
      SPCC(126,3)=T(40.D0,30.D0)
      SPCC(126,4)=16000.D0
      SPCC(126,5)=100000.D0
****           WY WC

      SPCC(127,1)=T(108.D0,45.D0)
      SPCC(127,2)=600000.D0
      SPCC(127,3)=T(40.D0,30.D0)
      SPCC(127,4)=16000.D0
      SPCC(127,5)=0.D0

****           WY W

      SPCC(128,1)=T(110.D0,05.D0)
      SPCC(128,2)=800000.D0
      SPCC(128,3)=T(40.D0,30.D0)
      SPCC(128,4)=16000.D0
      SPCC(128,5)=100000.D0

***           PUERTO RICO AND VIRGIN ISLANDS

      SPCC(129,1)=T(66.D0,26.D0)
      SPCC(129,2)=200000.D0
      SPCC(129,3)=200000.D0
      SPCC(129,4)=T(18.D0,02.D0)
      SPCC(129,5)=T(18.D0,26.D0)
      SPCC(129,6)=T(17.D0,50.D0)

****           GUAM

***   SPCC(133,1)=213.0D0
***   SPCC(133,2)=500000.0D0
***   SPCC(133,3)=0.0D0
***   SPCC(133,4)=2500.0D0
***   SPCC(133,5)=0.0D0
***
      SPCC(133,1)=T(215.D0,15.D0)
      SPCC(133,2)=100000.D0
      SPCC(133,3)=T(13.D0,30.D0)
      SPCC(133,4)=1.D0
      SPCC(133,5)=200000.D0

****           KY ONE
      SPCC(134,1)=85.75D0
      SPCC(134,2)=1500000.D0
      SPCC(134,3)=1000000.D0
      SPCC(134,4)=T(37.D0,05.D0)
      SPCC(134,5)=T(38.D0,40.D0)
      SPCC(134,6)=T(36.D0,20.D0)

****           GUAM New
      SPCC(135,1)=T(215.D0,15.D0)
      SPCC(135,2)=200000.D0
      SPCC(135,3)=T(13.D0,30.D0)
      SPCC(135,4)=1.D0
      SPCC(135,5)=100000.D0

*** UNIVERSAL TRANSVERSE MERCATOR HAS 4 CONSTANTS
*** LOAD CONSTANTS BY ZONES, 1 THRU 60
***          1 - CENTRAL MERIDIAN
***          2 - FALSE EASTING VALUE AT THE CM = 500,000.
***          3 - SOUTHERNMOST PARALLEL = 0.0
***          4 - SCALE FACTOR = 0.9996
*** SINCE THE LAST 3 CONSTANTS ARE ALWAYS THE SAME,
***       ONLY THE CENTRAL MERDIAN IS LOADED.

      DO 30 I=1,60
 30     UTMC(I)=6.D0*I-183.D0

      ZN(1)='AL E'
      ZN(2)='AL W'
      ZN(3)='AK 1'
      ZN(4)='AK 2'
      ZN(5)='AK 3'
      ZN(6)='AK 4'
      ZN(7)='AK 5'
      ZN(8)='AK 6'
      ZN(9)='AK 7'
      ZN(10)='AK 8'
      ZN(11)='AK 9'
      ZN(12)='AK10'
      ZN(13)='AZ E'
      ZN(14)='AZ C'
      ZN(15)='AZ W'
      ZN(16)='AR N'
      ZN(17)='AR S'
      ZN(18)='CA 1'
      ZN(19)='CA 2'
      ZN(20)='CA 3'
      ZN(21)='CA 4'
      ZN(22)='CA 5'
      ZN(23)='CA 6'
      ZN(24)='CO N'
      ZN(25)='CO C'
      ZN(26)='CO S'
      ZN(27)='CT  '
      ZN(28)='DE  '
      ZN(29)='FL E'
      ZN(30)='FL W'
      ZN(31)='FL N'
      ZN(32)='GA E'
      ZN(33)='GA W'
      ZN(34)='HI 1'
      ZN(35)='HI 2'
      ZN(36)='HI 3'
      ZN(37)='HI 4'
      ZN(38)='HI 5'
      ZN(39)='ID E'
      ZN(40)='ID C'
      ZN(41)='ID W'
      ZN(42)='IL E'
      ZN(43)='IL W'
      ZN(44)='IN E'
      ZN(45)='IN W'
      ZN(46)='IA N'
      ZN(47)='IA S'
      ZN(48)='KS N'
      ZN(49)='KS S'
      ZN(50)='KY N'
      ZN(51)='KY S'
      ZN(52)='LA N'
      ZN(53)='LA S'
      ZN(54)='LASH'
      ZN(55)='ME E'
      ZN(56)='ME W'
      ZN(57)='MD  '
      ZN(58)='MA M'
      ZN(59)='MA I'
      ZN(60)='MI N'
      ZN(61)='MI C'
      ZN(62)='MI S'
      ZN(63)='MI N'
      ZN(64)='MI C'
      ZN(65)='MI S'
      ZN(66)='MN N'
      ZN(67)='MN C'
      ZN(68)='MN S'
      ZN(69)='MS E'
      ZN(70)='MS W'
      ZN(71)='MO E'
      ZN(72)='MO C'
      ZN(73)='MO W'
      ZN(74)='MT  '
      ZN(75)='MT  '
      ZN(76)='MT  '
      ZN(77)='NE  '
      ZN(78)='NE  '
      ZN(79)='NV E'
      ZN(80)='NV C'
      ZN(81)='NV W'
      ZN(82)='NH  '
      ZN(83)='NJ  '
      ZN(84)='NM E'
      ZN(85)='NM C'
      ZN(86)='NM W'
      ZN(87)='NY E'
      ZN(88)='NY C'
      ZN(89)='NY W'
      ZN(90)='NY L'
      ZN(91)='NC  '
      ZN(92)='ND N'
      ZN(93)='ND S'
      ZN(94)='OH N'
      ZN(95)='OH S'
      ZN(96)='OK N'
      ZN(97)='OK S'
      ZN(98)='OR N'
      ZN(99)='OR S'
      ZN(100)='PA N'
      ZN(101)='PA S'
      ZN(102)='RI  '
      ZN(103)='SC  '
      ZN(104)='SD N'
      ZN(105)='SD S'
      ZN(106)='TN  '
      ZN(107)='TX N'
      ZN(108)='TXNC'
      ZN(109)='TX C'
      ZN(110)='TXSC'
      ZN(111)='TX S'
      ZN(112)='UT N'
      ZN(113)='UT C'
      ZN(114)='UT S'
      ZN(115)='VT  '
      ZN(116)='VA N'
      ZN(117)='VA S'
      ZN(118)='WA N'
      ZN(119)='WA S'
      ZN(120)='WV N'
      ZN(121)='WV S'
      ZN(122)='WI N'
      ZN(123)='WI C'
      ZN(124)='WI S'
      ZN(125)='WY E'
      ZN(126)='WYEC'
      ZN(127)='WYWC'
      ZN(128)='WY W'
      ZN(129)='PRVI'
      ZN(130)='VIZ1'
      ZN(131)='VISX'
      ZN(132)='AS  '
      ZN(133)='GU  '
      ZN(134)='KY1Z'
      ZN(135)='GU  '

      RETURN
      END
