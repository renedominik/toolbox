#!/usr/bin/python3

import pdb_functions as pdb
import numpy as np
import sys

if len(sys.argv) < 2:
    print( "USAGE:", sys.argv[0], "FILE.pdb")
    print( "it will return the x,y,z limits of the pdb using both ATOM and HETATM lines")
    exit(1)

mini = [ 999 , 999, 999 ]
maxi = [ -999, -999, -999 ]
with open( sys.argv[1]) as r:
    for l in r:
        if l[0:4] != "ATOM" and l[0:6] != "HETATM": continue
        pos = pdb.position(l)
        for i in range(0,3):
            if pos[i] < mini[i]:
                mini[i] = pos[i]
            if pos[i] > maxi[i]:
                maxi[i] = pos[i]

print( "limits of pdb:", mini, maxi)


                        
