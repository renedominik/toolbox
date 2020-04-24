#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

import pdb_functions as pdb


def SetResidueType( line, typ ):
    typ = typ.strip()
    if len(typ) != 3:
        print "ERROR: residue type has to be given in three letter code:", typ
        exit(1)
    return line[:17] + typ + line[20:]

    
chains = sys.argv[2:]

if len(sys.argv) < 3:
    print "USAGE", sys.argv[0], "FILE.pdb CHAIN1 ..."
    exit(1)

atoms = [ "C", "N", "O", "CA" ]

with open( sys.argv[1]) as f:
    for l in f:

        l = l.strip()

        # whattodo with hatatoms?
        if l[:4] != "ATOM":
            print l
            continue
        
        found = False

        if pdb.chain(l) not in chains or pdb.atom_name(l) in atoms:
            print l
            
