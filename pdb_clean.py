#!/usr/bin/python3

import sys
from Bio.PDB import *

if len(sys.argv) != 3:
    print( "USAGE:",sys.argv[0],"IN.pdb OUT.pdb")
    exit(1)
    
parser = PDBParser()

structure = parser.get_structure('abc',sys.argv[1])

io = PDBIO()

io.set_structure(structure[0]) # select first model only
io.save( sys.argv[2] )
