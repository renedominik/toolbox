#!/usr/bin/python3

# copyright rene staritzbichler, 27.8.20

import math
import sys
import vector_functions as vec


if len(sys.argv) < 2 or len(sys.argv)%2 != 1:
    print( "USAGE:", sys.argv[0], "x1 y1 ... x2 y2 ...")
    exit(1)

length = int(len(sys.argv) / 2)

v1 = [float(x) for x in sys.argv[1:length+1]]
v2 = [float(x) for x in sys.argv[length+1:]]

a = vec.Angle( v1, v2)
print( "angle:", a, 180.0 / math.pi * a )

