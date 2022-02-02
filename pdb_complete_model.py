#!/usr/bin/python3


import numpy as np
import sys
import pdb_relative_coordinates as rel
import pdb_abs_from_rel_pos as ab
from container import defaultdict

def correct( lines, relative , names, residue_name):
    for l in lines:
        print( l.strip() )
    chain = lines[-1][21]
    resid = lines[-1][22:26]
    nr = -1
    missing = []
    # find missing atoms:
    for atom_name, rel_coo in relative.items():
        if not atom_name in names:
            abs_coo = ab.AbsoluteCoordinates( sys.argv[2], reference_atoms[0], reference_atoms[1], reference_atoms[2], rel_coo[0], rel_coo[1], rel_coo[2] )
            print( "HETATM{:5d} {:>4s} ".format( nr, atom_name) + residue_name + " " + chain + "   {:>4s}    {:8.3f}{:8.3f}{:8.3f}".format( resid, abs_coo[0], abs_coo[1], abs_coo[2] ) + "  1.00  0.0            H")

            
            
def connectivity_map( lines ):
    diggi = defaultdict( list )
    for i in range( 0, len(lines) - 1):
        l = lines[i]
        pos1 = np.array( [ float(l[30:38]) , float(l[38:46]) , float(l[46:54]) ] )
        name1 = l[12:16]
        diggi[name1].append( [name1,pos1] )
        for j in range( i+1, len(lines)):
            l = lines[j]
            name2 = l[12:16]
            pos2 =  np.array( [ float(l[30:38]) , float(l[38:46]) , float(l[46:54]) ] )
            dist = np.linalg.norm( pos1 - pos2 )
            if dist < 1.55:
                diggi[name1].append( [name2,pos2] )

                

if len(sys.argv) < 6:
    print( 'USAGE', sys.argv[0], 'template.pdb model.pdb TYPE1 TYPE2 TYPE3 (CHAIN:default "A")' )
    print( 'reads template and checks model and adds missing hydrogens to identical residues')
    print( 'TYPEi defines the atom names used for defining the reference coordinate system')
    exit(1)

# GBF: 
#reference_atoms = [ 'C2A', 'CHD', 'C4B' ]       # atoms from ring structure, defining coordinate system

reference_atoms = sys.argv[3:]
#print( reference_atoms)

chain = 'A'
if len( sys.argv) > 6:
    chain = sys.argv[6]
    
# collect this from template.pdb
relative = {}  # key: atom name, value: relative coordinates 

template = []

with open( sys.argv[1] ) as r:
    for l in r:
        if l[:4] != 'ATOM' and l[:6] != 'HETATM': continue
        template.append( l.strip() )
        atom_name = l[12:16]
        residue_name = l[17:20]
        if atom_name[0] == 'H':
            relative[ atom_name ] = rel.RelativeCoordinates(sys.argv[1], reference_atoms[0], reference_atoms[1], reference_atoms[2], atom_name)


#print( "residue ", residue_name)

with open( sys.argv[2] ) as r:
    lines = r.readlines()

prev = -99999
residue = []
names = []
for i in range(0, len(lines)):
    l = lines[i]
    if l[:4] != 'ATOM' and l[:6] != 'HETATM':
        print( l.strip() )
    if l[17:20] != residue_name:
        print( l.strip() )
    resid = int( l[22:26] )
    if prev != -99999 and prev != resid:
        correct( residue , relative, names, residue_name)
        prev = resid
        residue = []
        names = []
    residue.append(l)
    names.append( l[12:16] )
    
if len(residue) > 0:
    correct( residue , relative, names, residue_name)



