#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import Bio.PDB
import Bio.AlignIO
import sys
import numpy as np

if len( sys.argv) < 3:
    print( "USAGE:",sys.argv[0]," IN.pdb  OUT.pdb")
    print( "min dist of ATOM CA to HETATM will be written into b-factor of pdb")
    exit(1)

atoms = []
hetatms = []

in_file = sys.argv[1]
out_file = sys.argv[2]

pdb_parser = Bio.PDB.PDBParser( QUIET=True )

structure = pdb_parser.get_structure( "first", in_file )[0]

for chain in structure:
    #print( 'first:', chain.get_id())
    for residue in chain:
        print( residue.id)
        if "H_" == residue.id[0][:2]:
            for atom in residue:
                hetatms.append( atom)
        for atom in residue:
            atom.set_bfactor( 0.0)
print( 'we found', len(hetatms), 'hetero atoms in the pdb file')

for chain in structure:
    for residue in chain:
        if "H_" == residue.id[0][:2] or 'W' == residue.id[0]:
            continue
        print( residue.id)
        for atom in residue:
            position = atom.coord
            min_dist = 999999999
            for h in hetatms:
                distance = np.linalg.norm( position - h.coord )
                if distance < min_dist:
                    min_dist = distance
            atom.set_bfactor( min_dist)

                     
io = Bio.PDB.PDBIO()
io.set_structure( structure )
io.save( out_file)

