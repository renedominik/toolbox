#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import Bio.PDB
import Bio.AlignIO
import sys

first_atoms = []
second_atoms = []

first_file = "5v8k_orig.pdb"
second_file = "5v8k_opm.pdb"
third_file = "5v8k_dimer.pdb"
out_file = "5v8k_dimer_membrane.pdb"

###  read pdbs 
pdb_parser = Bio.PDB.PDBParser( QUIET=True )
first_structure = pdb_parser.get_structure( "first", first_file )[0]
second_structure = pdb_parser.get_structure( "second", second_file )[0]
third_structure = pdb_parser.get_structure( "third", third_file )[0]

# use only CA atoms for alignment
for chain in first_structure:
    for residue in chain:
        if 'CA' in residue:
            first_atoms.append( residue['CA'] )

for chain in second_structure:
    for residue in chain:
        if 'CA' in residue:
            second_atoms.append( residue['CA'] )

### aligning structures            
aligner = Bio.PDB.Superimposer()
aligner.set_atoms( second_atoms, first_atoms ) # place latter on former
print( "RMSD", first_file + ":", aligner.rms)

# apply to third structure
for chain in third_structure:
    aligner.apply( chain.get_atoms() ) # apply rotation and translation 

# write output
io = Bio.PDB.PDBIO()
io.set_structure( third_structure )
io.save( out_file)

           
#rotmatrix = aligner.rotran[0]
#transvector = si.rotran[1]
