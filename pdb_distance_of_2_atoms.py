#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             12.08.2020           ##
#######################################

import sys
import pdb_functions as pdb
import numpy as np

if len(sys.argv) < 5:
    print( "USAGE:", sys.argv[0], "RESID1 CHAIN1 RESID2 CHAIN1 PDB_1 ...")

r1 = int( sys.argv[1] )
c1 = sys.argv[2]
r2 = int( sys.argv[3] )
c2 = sys.argv[4]
name = "CA"

for i in range( 5, len(sys.argv)):
    with open( sys.argv[i] ) as f:
        pos1 = []
        pos2 = [] 
        found1 = False
        found2 = False
        for l in f:
            if ("ATOM" in l or "HETATM" in l) and  pdb.chain(l) == c1 and pdb.resid(l) == r1 and pdb.atom_name(l) == name:
                pos1 = pdb.position(l)
                found1 = True
            elif  ("ATOM" in l or "HETATM" in l) and pdb.chain(l) == c2 and pdb.resid(l) == r2 and pdb.atom_name(l) == name:
                pos2 = pdb.position(l)
                found2 = True
            if found1 and found2:
                print( sys.argv[i], np.linalg.norm( pos1 - pos2 ) , end = ' ')
                found1 = False
                found2 = False
            if l[:4] == "pose":
                print( l.split()[-1] )
