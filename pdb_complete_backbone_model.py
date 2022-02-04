#!/usr/bin/python3

import numpy as np
import sys
import coordinate_transformation as ct
from collections import defaultdict

import Bio.PDB



# not used
def Orthogonalize( pos):
    x = pos[0] - pos[1]
    dx = np.linalg.norm(x)    
    x /= np.linalg.norm(x)
    pos[0] = pos[1] + x
    y = pos[2] - pos[1]
    dy = np.linalg.norm(y)    
    print( '# ortho: dist:', dx, dy, 'angle:', 180.0 / np.pi * np.arccos( np.dot( x, y)))
    z = np.cross( x, y)
    y = np.cross( z, x )
    y /= np.linalg.norm(y)
    pos[2] = pos[1] + y
    return pos


def Insert( all_pos, residue, template_ref, template_pos, template_names, reference_atoms): 
    if len(residue) == len(template_names[0]):
        for l in residue:
            print( l.strip(), '##' )
        #print( 'complete, nothing to do')
        return
    
    positions = {}
    for l in residue:
        positions[ l[12:16].strip() ] = Position(l)
    chain = residue[0][21]
    resid = residue[0][22:26]
    residue_name = residue[0][17:20].strip()
    nr = -1

    ref_pos = []
    ref_pos.append( positions[ reference_atoms[0] ] )
    ref_pos.append( positions[ reference_atoms[1] ] )
    ref_pos.append( positions[ reference_atoms[2] ] )

    clash = []
    rotate = []
    for template_ref_pos, template_all_pos in zip( template_ref, template_pos):
        tmp, rot, cms1, cms2 = ct.Superimpose( ref_pos, template_ref_pos)
        new_pos = ct.CooInNewRef( template_all_pos, rot, cms1, cms2)
        clash.append( Clashes( all_pos, new_pos, 3 ) )
        rotate.append( [rot,cms1,cms2,new_pos] )

    print( '# clashes:', clash)
    min_id = min(enumerate(clash),key=lambda x: x[1])[0]
    #print( 'template', min_id, ' with', clash[min_id], 'clashes')

    for new_pos, atom_name in zip( rotate[min_id][3], template_names[min_id]):
        print( "HETATM{:5d} {:>4s} ".format( nr, atom_name) + residue_name + " " + chain + "{:>4s}    {:8.3f}{:8.3f}{:8.3f}".format( resid, new_pos[0], new_pos[1], new_pos[2] ) + "  1.00  0.0            H **")


            
def Position( l ):
    return np.array( [ float(l[30:38]) , float(l[38:46]) , float(l[46:54]) ] )
            
def PositionMap( lines ):
    diggi = {}
    for l in lines:
        diggi[l[12:16].strip() + ':' + l[21] + ':' + l[22:26].strip() ] = Position(l)
    return diggi

   
def Clashes( all_posx, pos, threshold ):
    count = 0
    for p in all_posx:
        d = np.linalg.norm( p - pos )
        #print( d, threshold, l[:54] , pos )
        if d < threshold:
            count += 1
    return count



######################################################################################
###############################   MAIN   #############################################
######################################################################################


if len(sys.argv) < 3:
    print( 'USAGE', sys.argv[0], 'template.pdb model.pdb RESNAME' )  # TYPE1 TYPE2 TYPE3' )
    #print( 'USAGE', sys.argv[0], 'template.pdb model.pdb (CHAIN:default "A")' )
    print( 'reads template and checks model and adds missing atoms, comparing different conformations' )
    print( 'TYPEi defines the atom names used for defining the reference coordinate system')
    exit(1)


    
resname = sys.argv[3]

#if resname == "GBF":
#    reference_atoms = [ 'C1A', 'C2A', 'C3A' ]
#    backbone = ['CAA','CBA','CGA','O1A','O2A','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','HAA1','HAA2','HBA1','HBA2','H11','H12','H2','H41','H42','H43','H51','H52','H61','H62','H71','H91','H92','H93','H101','H102','H111','H112','H121','H141','H142','H143','H151','H152','H161']

# GBF:
if resname == "GBF":
    reference_atoms = [ 'C2A', 'CHD', 'C4B' ]       # atoms from ring structure, defining coordinate system
#reference_atoms = sys.argv[3:]

print( 'reference atoms:', reference_atoms)

pdb_parser = Bio.PDB.PDBParser( QUIET=True )
first_structure = pdb_parser.get_structure( "first", sys.argv[1] )[0]
second_structure = pdb_parser.get_structure( "second", sys.argv[2] )[0]


with open( sys.argv[1] ) as r:
    template_lines = r.readlines()
    
pos_map = PositionMap( template_lines) # key: atom name + ':' + l[21] + ':' + l[22:26].strip()

template_ref = []
template_pos = []
template_names = []
residue_pos = []
atom_names = []

prev = -99999
for l in template_lines:
    atom_name = l[12:16].strip()
    residue_name = l[17:20]
    resid = int(l[22:26])
    if residue_name == resname:
        if resid != prev:
            ending = ':' + l[21] + ':' + l[22:26].strip()
            ref_pos = []
            ref_pos.append( pos_map[reference_atoms[0] + ending ])
            ref_pos.append( pos_map[reference_atoms[1] + ending ])
            ref_pos.append( pos_map[reference_atoms[2] + ending ])
            template_ref.append( ref_pos )
            prev = resid            
            if len(residue_pos) > 0:
                template_pos.append( residue_pos)
                template_names.append( atom_names)
                residue_pos = []
                atom_names = []
        residue_pos.append( Position(l) )
        atom_names.append( atom_name )
                            
if len(residue_pos) > 0:
    template_pos.append( residue_pos)
    template_names.append( atom_names)


print( "residue ", residue_name)
print( len(template_names), 'templates')

with open( sys.argv[2] ) as r:
    lines = r.readlines()

all_pos = []
for l in lines:
    if l[:4] != 'ATOM' and l[:6] != 'HETATM':
        continue
    all_pos.append( Position(l))
print( '# pos:', len(all_pos))

prev = -99999
residue = []
for i in range(0, len(lines)):
    l = lines[i]
    if l[:4] != 'ATOM' and l[:6] != 'HETATM':
        print( l.strip()   + ' - ')
        continue
    if l[17:20] != residue_name:
        print( l.strip()   + ' + ')
        continue
    resid = int( l[22:26] )
    if prev != resid:
        if len(residue) > 0:
            Insert( all_pos, residue , template_ref, template_pos, template_names, reference_atoms)
            residue = []
        prev = resid
        #print( 'reset')
    residue.append(l)

    
if len(residue) > 0:
    Insert( all_pos, residue , template_ref, template_pos, template_names, reference_atoms)




