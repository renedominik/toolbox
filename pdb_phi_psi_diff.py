#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import Bio.PDB
import sys
import numpy as np

if len( sys.argv ) < 9:
    print "USAGE:", sys.argv[0], "  PDB1 (MODEL1) CHAIN1 FIRST_RES1 LAST_RES1 PDB2 (MODEL2) CHAIN2 FIRST_RES2 LAST_RES2"
    print "NOTE: if providing only one model identifier, it will be assumed to belong to PDB2 !!"
    exit(1)


def PhiPsi( pdb , model_id, chain_id, first_id, last_id ):
    
    for model in Bio.PDB.PDBParser().get_structure( "pdb" , sys.argv[1] ) :
        #print model.id
        if len( model_id ) > 0 and model.id != int(model_id): continue
        #print "right model"
        for chain in model :
            #print chain.id
            if chain.id != chain_id: continue
            #print "chain found"
            poly = Bio.PDB.Polypeptide.Polypeptide(chain)
            #print "Model %s Chain %s" % (str(model.id), str(chain.id)),
            return [item for sublist in poly.get_phi_psi_list()[first_id:last_id] for item in sublist]
            #print poly.get_phi_psi_list()[4:8]

            
offset = 0
pdb1 = sys.argv[1]
model1 = ""
if len(sys.argv) == 11:
    model1 = sys.argv[2]
    offset += 1
chain1 = sys.argv[2+offset]
first_res1 = int(sys.argv[3+offset])
last_res1 = int( sys.argv[4+offset])

pdb2 = sys.argv[5+offset]
model2 = ""
    
if len(sys.argv) > 9:
    model2 = sys.argv[6+offset]
    offset += 1
        
chain2 = sys.argv[6+offset]
first_res2 = int(sys.argv[7+offset])
last_res2 = int(sys.argv[8+offset])

print pdb1, model1, chain1, first_res1, last_res1, pdb2, model2, chain2 , first_res2, last_res2

list1 = PhiPsi( pdb1, model1, chain1, first_res1, last_res1 )
#print list1
list2 = PhiPsi( pdb2, model2, chain2, first_res2, last_res2 )
#print list2

diff = [0] * (len(list1)-2)
for i in range(1, len(list1)-1):
    d = np.degrees( abs( list1[i] - list2[i] ) )
    if d > 180:
        d = 360.0 - d
    diff[i-1] = d
    
print diff
print sum(diff) / float(len(diff))

print
