#!/usr/bin/python3


import numpy as np
import sys
import coordinate_transformation as ct
from collections import defaultdict




def correct( lines, relative):
    names = []
    positions = {}
    for l in lines:
        names.append( l[12:16].strip() )
        positions[ names[-1] ] = position(l)
        print( l.strip() ) # + ' # ')
    chain = lines[-1][21]
    resid = lines[-1][22:26]
    residue_name = lines[-1][17:20].strip()
    nr = -1
    missing = []
    keys = positions.keys()
    #print(keys)
    # find missing atoms:
    for atom_name, rel_coo in relative.items():
        if not atom_name in names:
            reference_atoms = ref_atoms[ atom_name ]
            if reference_atoms[0] not in keys or reference_atoms[1] not in keys or reference_atoms[2] not in keys:
                print( 'WARNING: cannot add', atom_name, ' to ', chain, resid, residue_name, ', one of these is missing:', reference_atoms)
                continue
            
            #print( atom_name, reference_atoms)
            rel_coo = relative[ atom_name]
            #print( rel_coo)
            abs_coo = ct.AbsolutePosition(
                rel_coo,
                positions[ reference_atoms[0] ],
                positions[ reference_atoms[1] ],
                positions[ reference_atoms[2] ])
                                           
            #print( abs_coo)
            print( "HETATM{:5d} {:>4s} ".format( nr, atom_name) + residue_name + " " + chain + "{:>4s}    {:8.3f}{:8.3f}{:8.3f}".format( resid, abs_coo[0], abs_coo[1], abs_coo[2] ) + "  1.00  0.0            H *")

            
def position( l ):
    return np.array( [ float(l[30:38]) , float(l[38:46]) , float(l[46:54]) ] )
            
def connectivity_map( lines ):
    diggi = defaultdict( list )
    for i in range( 0, len(lines) - 1):
        l = lines[i]
        pos1 = position(l)
        name1 = l[12:16].strip()
        for j in range( i+1, len(lines)):
            l = lines[j]
            name2 = l[12:16].strip()
            pos2 =  position(l)
            dist = np.linalg.norm( pos1 - pos2 )
            if dist < 1.65:
                diggi[name1].append( name2 )
                diggi[name2].append( name1 )
    return diggi

def position_map( lines ):
    diggi = {}
    for l in lines:
        diggi[l[12:16].strip()] = position(l)
    return diggi

def reference_heavy_atoms( name, connect):
    cons = connect[name]
    first = cons[0]
    if len(cons) > 1:
        print( 'WARNING: for <',name,'> it should contain single non-hydrogen', cons)
    next_cons = []
    for c in connect[ first ]:
        if c[0] != 'H':
            next_cons.append(c)
    if len( next_cons ) > 2:
        cons.remove( cons[-1] )
        cons.extend( next_cons)
        #print( 'fixed <',name,'> ', cons)
        return cons
    cons.extend( next_cons)
    #print( name, cons )
    if len( next_cons) == 2:
        return cons
    if len( next_cons ) == 0:
        print( 'WARNING: for <',name,'> empty: ', first, connect[first])


    now = next_cons[0]
    next2 = []
    for c in connect[ next_cons[0] ]:
        if c[0] != 'H' and c != first:
            next2.append(c)
    if len(next2) == 2:
        cons.remove( cons[-1] )
    elif len(next2) > 2:
        print( 'WARNING: next for <',name,'> it should contain not more than two non-hydrogen', next2)
    cons.extend( next2)
    #print( name, cons )
    return cons
   

if len(sys.argv) < 3:
    #print( 'USAGE', sys.argv[0], 'template.pdb model.pdb TYPE1 TYPE2 TYPE3 (CHAIN:default "A")' )
    print( 'USAGE', sys.argv[0], 'template.pdb model.pdb (CHAIN:default "A")' )
    print( 'reads template and checks model and adds missing hydrogens to identical residues')
    print( 'TYPEi defines the atom names used for defining the reference coordinate system')
    exit(1)

# GBF: 
#reference_atoms = [ 'C2A', 'CHD', 'C4B' ]       # atoms from ring structure, defining coordinate system
#reference_atoms = sys.argv[3:]
#print( reference_atoms)

chain = 'A'
if len( sys.argv) > 3:
    chain = sys.argv[3]
    
with open( sys.argv[1] ) as r:
    template = r.readlines()

pos = position_map( template)
connectivity = connectivity_map( template) 

# collect this from template.pdb
relative = {}  # key: atom name, value: relative coordinates 
ref_atoms = {}

for l in template:
    atom_name = l[12:16].strip()
    residue_name = l[17:20]
    if atom_name[0] == 'H':
        reference_atoms = reference_heavy_atoms( atom_name, connectivity ) # find 'backbone' atoms: C, N, O? 
        relative[ atom_name] = ct.RelativeCoordinates( pos[reference_atoms[0]], pos[reference_atoms[1]], pos[reference_atoms[2]], pos[atom_name])
        ref_atoms[atom_name] = reference_atoms
        #print( '*', atom_name, reference_atoms)


#print( "residue ", residue_name)

with open( sys.argv[2] ) as r:
    lines = r.readlines()

prev = -99999
residue = []
for i in range(0, len(lines)):
    l = lines[i]
    if l[:4] != 'ATOM' and l[:6] != 'HETATM':
        print( l.strip() ) #  + ' - ')
        continue
    if l[17:20] != residue_name:
        print( l.strip() ) #  + ' + ')
        continue
    resid = int( l[22:26] )
    if prev != resid:
        if prev != -99999:
            correct( residue , relative)
            residue = []
        prev = resid
        #print( 'reset')
    residue.append(l)

    
if len(residue) > 0:
    correct( residue , relative)



