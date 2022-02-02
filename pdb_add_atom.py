#!/usr/bin/python3


import numpy as np
import sys

if len(sys.argv) < 6:
    print( 'USAGE', sys.argv[0], 'PDB CHAIN RESNAME ATOMNAME X Y Z' )
    print( 'write a single additional line to PDB, incrementing the atom ID')
    print( 'NOTE: ending of the line is currently set to hydrogen and bfactor of 0')
    exit(1)

pdb_file = sys.argv[1]
chain = sys.argv[2]
res_name = sys.argv[3]
atom_name = sys.argv[4]

x = float(sys.argv[5])
y = float(sys.argv[6])
z = float(sys.argv[7])


with open( pdb_file) as r:
    for l in r:
        print( l.strip() )
        if (l[:4] == "ATOM" or l[:6] == "HETATM") and l[] == chain and l[] == res_name :
            nr = int(l[6:11])
            res = l[17:30] 

print( "HETATM{:5d} {:>4s} ".format( nr+1, atom_name) + res + "{:8.3f}{:8.3f}{:8.3f}".format( x, y, z) + "  1.00  0.0            H")
