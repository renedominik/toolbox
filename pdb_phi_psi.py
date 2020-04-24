#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import Bio.PDB
import sys

for model in Bio.PDB.PDBParser().get_structure( "pdb" , sys.argv[1] ) :
    for chain in model :
        poly = Bio.PDB.Polypeptide.Polypeptide(chain)
        print "Model %s Chain %s" % (str(model.id), str(chain.id)),
        print poly.get_phi_psi_list()
        #print poly.get_phi_psi_list()[4:8]
        # flat list: print [item for sublist in poly.get_phi_psi_list() for item in sublist]
