--TEST--
Different float syntaxes
--FILE--
<?php
0.0;
0.;
.0;
0e0;
0E0;
0e+0;
0e-0;
30.20e10;
300.200e100;
1e10000;
9999999999999999999;
0xFFFFFFFFFFFFFFFF;
07777777777777777777777;
0777777777777777777777787;
0b1111111111111111111111111111111111111111111111111111111111111111;
--EXPECT--
<?php
0.0;
0.;
.0;
0e0;
0E0;
0e+0;
0e-0;
30.20e10;
300.200e100;
1e10000;
9999999999999999999;
0xFFFFFFFFFFFFFFFF;
07777777777777777777777;
0777777777777777777777787;
0b1111111111111111111111111111111111111111111111111111111111111111;