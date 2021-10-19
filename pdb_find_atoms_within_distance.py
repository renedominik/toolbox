#!/usr/bin/python3

# copyright rene staritzbichler 11.9.2020

import sys, numpy as np
import pdb_functions as pdb, vector_functions as v

print( "NOTE: script is subject to continuos adjustment, check script before using it!!")

pdb_file = sys.argv[1]
mode = sys.argv[2]    # 'atom' or chain, e.g. 'A'
atom_id = int(sys.argv[3])
distance = float( sys.argv[4] )
atom_types = []
if len(sys.argv) > 5:
    atom_types = sys.argv[5:]

    
    
ref_pos = []
with open( pdb_file ) as r:
    for l in r:
        if ("ATOM" in l or "HETATM" in l) and ( ("at" in mode and atom_id == pdb.atom_id(l)) or (pdb.chain(l) == mode and atom_id == pdb.residue_id(l))) and "TIP3" not in l:
            ref_pos.append( pdb.position(l))
            print(l.strip())

print('\n',len(ref_pos), ' reference atoms found\n')

previous = -666

with open(pdb_file) as r:
    for l in r:
        if l[:4] == "ATOM"  and ( len(atom_types) == 0 or pdb.atom_name(l) in atom_types):

            if( previous != pdb.residue_id(l)):
                #print( pdb.single_letter( pdb.residue_name(l) ) , end='')
                previous = pdb.residue_id(l)
                
            pos = pdb.position(l)
            for ref in ref_pos:
                if v.Distance( pos, ref) <= distance:
                    #if pos[2] < ref[2]: # and pdb.residue_id(l) > 10:
                        #print( pdb.atom_id(l), end=',')
                        #print( l.strip())
                    print( pdb.atom_id(l), pdb.residue_id(l), pdb.residue_name(l), pdb.single_letter( pdb.residue_name(l)), pdb.chain(l),v.Distance( pos, ref) )
                    #print('.', end='')
print('')
