#!/usr/bin/python3

import numpy as np
import math, sys
import pdb_functions as pdb
import math_functions as m

if len(sys.argv) < 5:
    print( "USAGE:", sys.argv[0], "PDB X Y Z ANGLE optional:CHAIN1...")
    exit(1)

axis = [float(x) for x in sys.argv[2:5]]
angle = float( sys.argv[5] )

chains = []
if len(sys.argv) > 6:
    chains = sys.argv[6:]


with open( sys.argv[1]) as f:
    for l in f:
        l = l.strip()
        if l[:4] == "ATOM" and (len(chains)==0 or pdb.chain(l) in chains):
            pos =  np.dot( m.rotation_matrix(axis, angle) , pdb.position(l) )
            l = pdb.write_position(l,pos)
            print(l)
        else:
            print(l)
            


#np.dot(rotation_matrix(axis, theta), v)
        
