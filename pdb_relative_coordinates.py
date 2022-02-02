#!/usr/bin/python3


import numpy as np
import sys
import Bio.PDB


def RelativeCoordinates( file_name, type1, type2, type3, type4):
    pdb_parser = Bio.PDB.PDBParser( QUIET=True )
    structure = pdb_parser.get_structure( "first", sys.argv[1] )

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    name = atom.get_name()
                    if name == type1:
                        pos1 = atom.coord
                        #print( 'found 1', type1, pos1)
                    elif name == type2:
                        pos2 = atom.coord
                        #print( 'found 2', type2, pos2)
                    elif name == type3:
                        pos3 = atom.coord
                        #print( 'found 3', type3, pos3)
                    elif name == type4:
                        pos4 = atom.coord
                        #print( 'found 4', type4, pos4)
                        #print( type4, end=' ')

    v1 = pos2 - pos1
    v2 = pos2 - pos3
    v3 = np.cross( v1, v2)

    m = np.array( [ v1, v2, v3 ] ).transpose()

    pos = pos4 - pos2

    x = np.linalg.solve( m, pos)
    #print( x[0], x[1], x[2] )

    return x


    #print( 'correct?' , np.allclose( np.dot(m,x), pos))



if __name__ == "__main__":

    if len(sys.argv) < 6:
        print( 'USAGE', sys.argv[0], 'PDB ATOMNAME1 ATOMNAME2 ATOMNAME3 ATOMNAME4' )
        print( 'determine relative coordinates of atom4 in respect to the first three')
        exit(1)

    pdb_file = sys.argv[1]
    type1 = sys.argv[2]
    type2 = sys.argv[3]
    type3 = sys.argv[4]
    type4 = sys.argv[5]

    x = RelativeCoordinates( pdb_file, type1, type2, type3, type4)
    print( x[0], x[1], x[2] )
