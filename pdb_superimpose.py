#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import Bio.PDB
import sys

if len( sys.argv) != 8 and len( sys.argv ) != 6:
    print "USAGE:",sys.argv[0]," ALIGN.pdb  FIRST_RESIDUE_ID  LAST_RESIDUE_ID TEMPLATE.pdb  FIRST_RESIDUE_ID  LAST_RESIDUE_ID  OUT.pdb"
    print "OR:   ",sys.argv[0]," ALIGN.pdb  CHAIN  TEMPLATE.pdb  CHAIN  OUT.pdb"
    print "align first PDB to the coordinates of the second, using CA atoms only"
    print "bye"
    exit(1)

if len( sys.argv ) == 8:
    first_file = sys.argv[1]    
    id_first_start = int(sys.argv[2])
    id_first_last = int(sys.argv[3])

    second_file = sys.argv[4]
    id_second_start = int(sys.argv[5])
    id_second_last = int(sys.argv[6])

    out_file = sys.argv[7]

    first_atom_ids = range( id_first_start , id_first_last+1 )
    second_atom_ids = range( id_second_start , id_second_last+1 )

elif len( sys.argv ) == 6:
    first_file = sys.argv[1]
    first_chain = sys.argv[2]
    second_file = sys.argv[3]
    second_chain = sys.argv[4]
    out_file = sys.argv[5]
    
pdb_parser = Bio.PDB.PDBParser( QUIET=True )

first_structure = pdb_parser.get_structure( "first", first_file )[0]
second_structure = pdb_parser.get_structure( "second", second_file )[0]

first_atoms = []
second_atoms = []

if len( sys.argv ) == 8:
    for chain in first_structure:
        for residue in chain:
            if residue.get_id()[1] in first_atom_ids:
                first_atoms.append( residue['CA'] )

    for chain in second_structure:
        for residue in chain:
            if residue.get_id()[1] in second_atom_ids:
                second_atoms.append( residue['CA'] )

elif len( sys.argv ) == 6:
    #print "superimpose chains"
    #t = 0
    for chain in first_structure:
        #c = 0
        #for a in chain.get_atoms():
        #    c += 1
        #print( chain.get_id() , c )
        #t += c
        if chain.get_id() == first_chain:
            for residue in chain:
                first_atoms.append( residue['CA'] )
    #print "total:", t
    for	chain in second_structure:
	if chain.get_id() == second_chain:
            for	residue	in chain:
                second_atoms.append( residue['CA'] )

                
if len(second_atoms) != len(first_atoms):
    print "WARNING: number of atoms do not match!", len(first_atoms),len(second_atoms)
            
aligner = Bio.PDB.Superimposer()
aligner.set_atoms( second_atoms, first_atoms ) # place latter on former
print "RMSD", first_file + ":", aligner.rms

for chain in first_structure:
    aligner.apply( chain.get_atoms() ) # apply rotation and translation 

#c = 0
#for a in first_structure.get_atoms():
#    c += 1
#print c , "atoms"
               

io = Bio.PDB.PDBIO()
io.set_structure( first_structure )
io.save( out_file)

           
#rotmatrix = aligner.rotran[0]
#transvector = si.rotran[1]
