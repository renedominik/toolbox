#!/usr/bin/python3


import sys
import pdb_functions as pf
import numpy as np

if len(sys.argv) < 3:
    print( "USAGE", sys.argv[0], 'PDB1 PDB2')
    print( "returns lines that are spatially as close as possible")
    exit(1)

pdb = []
template = []

with open( sys.argv[1]) as r:
    for l in r:
        if l[:4] != "ATOM" and l[:6] != "HETATM": continue
        pdb.append(l)
with open( sys.argv[2]) as r:
    template  = r.readlines()

pdb_pos = []
for l in pdb:
    pdb_pos.append( pf.position(l))

template_pos = []
for l in template:
    template_pos.append( pf.position(l))
print( len(pdb), len(template))

    
if len(template) != len(template_pos) or len(pdb) != len(pdb_pos):
    print( "ERROR:",  len(template) , len(template_pos) , len(pdb) ,len(pdb_pos))
    exit(1)

for i in range( 0, len(template)):
    closest = -1
    min_dist = 99999999;
    for j in range( 0, len(pdb)):
        dist = np.linalg.norm( template_pos[i] - pdb_pos[j] )
        #print( i, j, dist )
        if dist < min_dist:
            #print('closer')
            closest = j
            min_dist = dist
    if closest == -1:
        print( "NOTHING FOUND!")
        exit(1)
    print( template[i][:30], 'DIST:', min_dist, pdb[closest][:30] )

    
