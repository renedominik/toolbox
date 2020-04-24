#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import numpy as np
import vector_functions as vf
import pdb_functions as pdb

if len(sys.argv) < 6:
    print "USAGE", sys.argv[0], " PDB  CHAIN  RESID  ATOM_NAME_1  ATOM_NAME_2"
    print "script finds two ca atoms in pdb that have the same direction as ATOM_1 and ATOM_2 in RESID/CHAIN"
    print "contains some settings of min/max values for z within which CA atoms are considered"
    exit(1)

pdb_file = sys.argv[1]
chain = sys.argv[2]
resid = int(sys.argv[3])
atom_name_1 = sys.argv[4]
atom_name_2 = sys.argv[5]

min_z = 20
max_z = 65
atomname = "CA"

print atomname, 'is searched within', min_z, max_z

x1 = []
x2 = []
atoms = []

print sys.argv

with open( pdb_file ) as f:
    for l in f:
        if l[:4] != "ATOM" or l[21] != chain: continue

        l_atom_name = pdb.atom_name( l )
        l_resid = pdb.resid(l)

        # calpha collection
        if l_atom_name == atomname:
            p = pdb.position(l)
            if p[2] >= min_z and p[2] <= max_z:
                atoms.append( [ chain , l_resid , p ] )
                
        if l_resid != resid: continue

        if l_atom_name == atom_name_1:
            print l
            x1 = pdb.position(l)
        elif l_atom_name == atom_name_2:
            print l
            x2 = pdb.position(l)

sidechain = np.array(x2) - np.array(x1)

print len( atoms), atomname , "collected"
print "dist of reference atoms:", np.linalg.norm(sidechain)

#print atoms

angle_dist_atominfo = {}

for i in range( 0, len(atoms)-1 ):
    for j in range( i+1 , len(atoms) ):
        atom1 = atoms[i]
        atom2 = atoms[j]
        vec = atom2[2] - atom1[2] 
        dist = np.linalg.norm( vec )
        angle = round( vf.angle(sidechain,vec) , 3 )
        #print i,j,dist, np.degrees( angle )
        if angle in angle_dist_atominfo:
            old_dist = angle_dist_atominfo[ angle ][0]
            if dist < old_dist:
                angle_dist_atominfo[ angle ] = [ dist , atom1[0], atom1[1] , atom2[0] , atom2[1] ] 
        else:
            angle_dist_atominfo[ angle ] = [ dist , atom1[0], atom1[1] , atom2[0] , atom2[1] ] 
            
        vec *= -1
        angle = round( vf.angle(sidechain,vec) , 3 )
        if angle in angle_dist_atominfo:
            old_dist = angle_dist_atominfo[ angle ][0]
            if dist < old_dist:
               angle_dist_atominfo[ angle ] = [ dist , atom1[0], atom1[1] , atom2[0] , atom2[1] ] 
        else:
            angle_dist_atominfo[ angle ] = [ dist , atom1[0], atom1[1] , atom2[0] , atom2[1] ] 

result =  sorted(angle_dist_atominfo.items())[0]

print np.degrees(result[0]), result[1:]

#    print round( np.degrees(k), 3), v
