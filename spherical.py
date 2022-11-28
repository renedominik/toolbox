#!/usr/bin/python3

import math, sys

angle = float( sys.argv[1])
delta = float(sys.argv[2])
radius = float(sys.argv[3])

xmin = 0
ymin = 0
if len(sys.argv) > 4:
    xmin = float( sys.argv[4])
if len(sys.argv) > 5:
    ymin = float( sys.argv[5])
    

while angle < 360:
    x = radius * math.cos( math.radians( angle))
    y = radius * math.sin( math.radians( angle))
    print( "{:.3f} {:.3f} {:.3f}".format(xmin + x,ymin + y, math.sqrt(x**2 + y**2)))
    angle += delta


