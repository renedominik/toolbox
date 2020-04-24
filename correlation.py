#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import numpy as np
#import scipy as sp
import sys

if len( sys.argv) < 4:
    print "USAGE:"
    print sys.argv[0], " FILE COL1 COL2"
    print "OR:"
    print sys.argv[0], "FILE1 COL1 FILE2 COL2"
    exit(1)

x = []
y = []

if len( sys.argv) == 4:
    c1 = int( sys.argv[2])
    c2 = int( sys.argv[3])
#    print c1, c2

    with open( sys.argv[1]) as f:
        for l in f:
            if l[0] == "#" or len( l) == 0: continue
            c = l.split()
            if len( c) < c2 + 1: continue
#            print c[c1],"\t", c[c2]
#            print len(c)
            x.append( float( c[c1]))
            y.append( float( c[c2]))

elif len( sys.argv) == 5:
    c1 = int( sys.argv[2])
    c2 = int( sys.argv[4])

    with open( sys.argv[1]) as f:
        for l in f:
            if l[0] == "#" or len( l) == 0: continue
            c = l.split()
            x.append( float( c[c1]))
        
    with open( sys.argv[3]) as f:
        for l in f:
            if l[0] == "#" or len( l) == 0: continue
            c = l.split()
            y.append( float( c[c2]))

print
print "correlation:", np.corrcoef( x, y)[0][1]
print "cross-correlation:", np.correlate(x,y)
#print "scipy: ", sp.pearsonr( x,y)
print
