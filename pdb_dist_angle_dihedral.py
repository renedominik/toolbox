#!/usr/bin/pytyon3

from BIO import PDB
import sys

pdb_file = sys.argv[1]
out_file = sys.argv[2]
chain_id = sys.argv[3]
id1 = int( sys.argv[4] )
id2 = int( sys.arg[5] )
id3 = int( sys.argv[6] )
id4 = int( sys.argv[7] )

a1 = ""
a2 = ""
a3 = ""
a4 = ""

w = open( out_file, 'a' )

structure = pdb_parser.get_structure( "first", pdb_file )[0]

for chain in structure.get_chains():
    if chain.get_id() == chain_id:
        for res in chain:
            for atom in res:
                atom_id = atom.get_id()
                if atom_id == id1:
                    a1 = atom
                elif atom_id == id2:
                    a2 = atom
                elif atom_id == id3:
                    a3 = atom
                elif atom_id == id4:
                    a4 = atom

print( a1, s2, a3, a4)

print( PDB.calc_dist( a2, a3) , PDB.calc_dist( a1, a4 ) , PDB.calc_angle( a1 - a2, a4 - a3), PDB.calc_dihedral( a1, a2 , a3 , a4 ) , file=w)


