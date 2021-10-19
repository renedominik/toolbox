#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import pdb_atoms as pdb

if len( sys.argv) < 3:
    print( "USAGE FIRST.pdb", syst.argv[0], "SECOND.pdb  optional:CHAIN_1 (...)" )
    print( "calc RMSD, using CA atoms only" )
    print( "bye" )
    exit(1)

# to make this safe from HETATM section, use
#from Bio import Struct
#s = Struct.read('protein_A.pdb')
# p = s.as_protein()  # strip off hetatms
    
first_file = sys.argv[1]    
second_file = sys.argv[2]

chains = []
if len(sys.argv) > 3:
    chains = sys.argv[3:]

print( "RMSD:", pdb.RMSD( first_file, second_file, chains) )


#aligner.apply( first_structure.get_atoms() )
#print "RMSD:",aligner.rms

#io = Bio.PDB.PDBIO()
#io.set_structure( first_structure )
#io.save( out_file)          
#rotmatrix = aligner.rotran[0]
#transvector = si.rotran[1]
