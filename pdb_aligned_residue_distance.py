#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import Bio.PDB
import Bio.AlignIO
import sys
import numpy as np

if len( sys.argv) < 7:
    print ( "USAGE:",sys.argv[0]," A.pdb  CHAIN_IN_A  B.pdb  CHAIN_IN_B  ALIGNMENT.clw  OUT.pdb")
    exit(1)

first_atoms = []
second_atoms = []

first_file = ""
second_file = ""

mode = sys.argv[1]

first_ids = []
second_ids = []

first_file = sys.argv[1]
first_chain_id = sys.argv[2]
second_file = sys.argv[3]
second_chain_id = sys.argv[4]
alignment_file = sys.argv[5]
out_file = sys.argv[6]

pdb_parser = Bio.PDB.PDBParser( QUIET=True )

first_structure = pdb_parser.get_structure( "first", first_file )[0]
second_structure = pdb_parser.get_structure( "second", second_file )[0]

alignment = Bio.AlignIO.read( open( alignment_file ), 'clustal')

first_chain = []
second_chain = []

for chain in first_structure:
    #print( 'first:', chain.get_id())
    for residue in chain:
        for atom in residue:
            atom.set_bfactor( 0.0)
    if chain.get_id() == first_chain_id:
        #print( 'found')
        first_chain = list(chain)

for chain in second_structure:
    #print( 'second:', chain.get_id())
    if chain.get_id() == second_chain_id:
        #print('found')
        second_chain = list(chain)
print( 'lengths of chains:', len(first_chain), len(second_chain))
        
first_count = 0  # position in first pdb, chain
second_count = 0 # position in second pdb/chain
for i in range( 0, len( alignment[0].seq )):
    if alignment[0].seq[i] != '-' and alignment[1].seq[i] != '-':
        #print( i, alignment[0].seq[i], alignment[1].seq[i])
        #print( i, first_count, first_chain[first_count], second_count, second_chain[second_count] )
        #print( i, first_chain[first_count]['CA'].coord , second_chain[second_count]['CA'].coord )
        distance = np.linalg.norm( first_chain[first_count]['CA'].coord - second_chain[second_count]['CA'].coord )
        for atom in first_chain[first_count]:
            atom.set_bfactor(distance)
            #first_chain[first_count].set_bfactor( distance)
    if alignment[0].seq[i] != '-':
        first_count += 1
    if alignment[1].seq[i] != '-':
        second_count += 1

                     
io = Bio.PDB.PDBIO()
io.set_structure( first_structure )
io.save( out_file)
