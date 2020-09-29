#!/usr/bin/python3

import sys

col1 = int(sys.argv[2])
x1 = float( sys.argv[3])
d1 = float( sys.argv[4])
col2 = int(sys.argv[5])
x2 = float( sys.argv[6])
d2 = float( sys.argv[7])

with open(sys.argv[1]) as r:
    for l in r:
        if l[0] == '#': continue
        c = [float(x) for x in l.split()]
        if c[col1] > x1 - d1 and c[col1] < x1 + d1 and c[col2] > x2 - d2 and c[col2] < x2 + d2 :
            print( l.strip()) 
