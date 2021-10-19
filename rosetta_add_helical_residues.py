#!/usr/bin/python
from pyrosetta import *
import sys


if len(sys.argv) < 2:
    print( "USAGE:", sys.argv[0], "INPDB RESID SEQUENCE OUTPDB")
    print( "provide sequence in 1 letter code" )
    exit()


init()

name = sys.argv[1]
out = sys.argv[-1]
residues = sys.argv[]


pose = Pose()
for aa in residues:

chm = pyrosetta.rosetta.core.chemical.ChemicalManager.get_instance()
resiset = chm.residue_type_set( 'fa_standard' )
res_type = resiset.get_representative_type_name1(aa) #e.g. A
residue = pyrosetta.rosetta.core.conformation.ResidueFactory.create_residue(res_type)
pose.append_polymer_residue_after_seqpos(residue, previous + 1, True)
