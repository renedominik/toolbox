#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import numpy as np
import sys
import pdb_functions as pdb

if len( sys.argv) < 3:
    print( "USAGE:",sys.argv[0]," FIRST.pdb XSHIFT YSHIFT ZSHIFT optional:CHAIN_1 (...)")
    print( "move all or specified chains by x,y,z")
    print( "bye")
    exit(1)

# to make this safe from HETATM section, use
#from Bio import Struct
#s = Struct.read('protein_A.pdb')
# p = s.as_protein()  # strip off hetatms
    
first_file = sys.argv[1]    

shift = np.array( [ float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) ] )

chains = []
if len(sys.argv) > 5:
    chains = sys.argv[5:]

with open( first_file) as f:
    for l in f:
        if len(l) > 50 and (l[0:4] == "ATOM" or l[0:6] == "HETATM") and (len(chains)==0 or pdb.chain(l) in chains):
            pos = shift + pdb.position(l)
            l = pdb.write_position(l,pos)
            print( l, end='')
        else:
            print( l, end='')
