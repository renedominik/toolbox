#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import pdb_functions as pdb
import sys
import numpy as np

if len(sys.argv) < 3:
    print "USAGE", sys.argv[0], "PDB1 PDB2"
    exit(1)

mols1 = pdb.ReadPDBLines( sys.argv[1] )
mols2 = pdb.ReadPDBLines( sys.argv[2] )

for atom1 in mols1:
    
