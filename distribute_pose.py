#!/usr/bin/python

import numpy as np
import math, sys
import pdb_functions as pdb
import pdb_atoms as at
import math_functions as m
import numpy.random as r

if len(sys.argv) != 9:
    print( "USAGE:", sys.argv[0], "PDB NR-COPIES X-MIN Y-MIN Z-MIN X-MAX Y-MAX Z-MAX" )
    exit(1)


pose = sys.argv[1]
nr = int( sys.argv[2] )
mins = [float(x) for x in sys.argv[3:6]]
maxs = [float(x) for x in sys.argv[6:]]

print( pose, nr, mins, maxs)

pid = pose.rfind( ".")
head = pose[:pid]
tail = pose[pid+1:]

pdb_lines = []
with open( pose ) as f:
    pdb_lines = f.readlines()

cms = at.CMS( pose )

for i in range( 0, nr ):
    pos = [ r.uniform( low, high) for low,high in zip( mins, maxs) ]
    axis = [ r.uniform( -1.0, 1.0 ) for j in range( 0, 3 ) ]
    angle = r.uniform( 0, 2.0 * np.pi )
    matrix = m.rotation_matrix( axis, angle)
    filename = head + '_' + str(i) + '.' + tail
    print( filename )
    with open( filename, 'w') as w:
        for l in pdb_lines:
            if l[:4] == "ATOM":
                x =  np.dot( matrix , pdb.position(l) - cms )
                l = pdb.write_position( l , x + pos )
            w.write( l )
            
            
