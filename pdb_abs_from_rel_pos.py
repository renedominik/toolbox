#!/usr/bin/python3


import numpy as np
import sys
import Bio.PDB


if len(sys.argv) < 6:
    print( 'USAGE', sys.argv[0], 'PDB ATOMNAME1 ATOMNAME2 ATOMNAME3 REL_X REL_Y REL_Z' )
    print( 'determine absolute coordinates from position of three atoms and the relative coordinates')
    exit(1)

pdb_file = sys.argv[1]
type1 = sys.argv[2]
type2 = sys.argv[3]
type3 = sys.argv[4]
rel_x = float(sys.argv[5])
rel_y = float(sys.argv[6])
rel_z = float(sys.argv[7])


pdb_parser = Bio.PDB.PDBParser( QUIET=True )
structure = pdb_parser.get_structure( "first", sys.argv[1] )

for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                name = atom.get_name()
                if name == type1:
                    pos1 = atom.coord
                    print( 'found 1', type1, pos1)
                elif name == type2:
                    pos2 = atom.coord
                    print( 'found 2', type2, pos2)
                elif name == type3:
                    pos3 = atom.coord
                    print( 'found 3', type3, pos3)

v1 = pos2 - pos1
v2 = pos2 - pos3
v3 = np.cross( v1, v2)

x = np.array( [rel_x,rel_y,rel_z])
m = np.array( [ v1, v2, v3 ] ).transpose()

pos = np.dot(m,x) + pos2

print( pos )
