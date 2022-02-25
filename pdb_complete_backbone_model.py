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


def Insert( all_pos, residue, template_ref, template_pos, template_atoms, reference_atoms, second_structure): 
    if len(residue) == len(template_atoms[0]):
        for l in residue:
            print( l.strip()) #, '##' )
        #print( 'complete, nothing to do')
        #sys.stdout.flush()
        return all_pos
    #print( "insert")
    sys.stdout.flush()
    positions = {}
    for l in residue:
        positions[ l[12:16].strip() ] = Position(l)
    res_chain = residue[0][21]
    resid = int( residue[0][22:26])
    residue_name = residue[0][17:20].strip()
    nr = -1

    ref_atoms = []
    for chain in second_structure:
        if chain.get_id()  == res_chain:
            for residue in chain:
                #print(  residue.get_id()[1], resid )
                #if residue.get_id()[1] == resid: 
                #    print( 'found?:', resid, residue.get_resname() , residue_name)
                if residue.get_resname() == residue_name and residue.get_id()[1] == resid:
                    #print( 'found!')
                    ref_atoms.append( residue[ reference_atoms[0] ] )
                    ref_atoms.append( residue[ reference_atoms[1] ] )
                    ref_atoms.append( residue[ reference_atoms[2] ] )
                    break
    #print( '# nr atoms in insert: ' , len(ref_atoms))
    #sys.stdout.flush()

    clash = []
    aligner = Bio.PDB.Superimposer()
    for i in range(0, len(template_atoms)):
        aligner.set_atoms( ref_atoms, template_ref[i] ) # place latter on former
        #print( "RMSD", aligner.rms, len(template_atoms[i]), i )
        sys.stdout.flush()

        aligner.apply( template_atoms[i] )
        count = 0
        for atom in template_atoms[i]:
            count += Clashes( all_pos, atom.coord , 2.5 )
        clash.append( count )

    #print( '# clashes:', clash)
    #sys.stdout.flush()

    min_id = min(enumerate(clash),key=lambda x: x[1])[0]
    aligner.set_atoms( ref_atoms, template_ref[min_id] )
    aligner.apply( template_atoms[min_id] )
    for atom in template_atoms[min_id]:
        new_pos = atom.coord
        all_pos.append(new_pos)
        atom_name = atom.name
        print( "HETATM{:5d} {:>4s} ".format( nr, atom_name) + residue_name + " " + res_chain + "{:>4d}    {:8.3f}{:8.3f}{:8.3f}".format( resid, new_pos[0], new_pos[1], new_pos[2] ) + "{:6.2f}  0.0                ".format( clash[min_id]))
    return all_pos


            
def Position( l ):
    return np.array( [ float(l[30:38]) , float(l[38:46]) , float(l[46:54]) ] )
            
def PositionMap( lines ):
    diggi = {}
    for l in lines:
        diggi[l[12:16].strip() + ':' + l[21] + ':' + l[22:26].strip() ] = Position(l)
    return diggi


def Clashes( all_pos, pos, threshold ):
    all_pos -= pos
    d = np.linalg.norm( all_pos, axis=1)
    return sum( x < threshold for x in d) # returns number of atom contacts below threshold

   
def Clashesxxx( all_posx, pos, threshold ):
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

print( 'REMARK cofactor:', resname)
print( 'REMARK reference atoms:', reference_atoms)

pdb_parser = Bio.PDB.PDBParser( QUIET=True )
first_structure = pdb_parser.get_structure( "first", sys.argv[1] )[0]
second_structure = pdb_parser.get_structure( "second", sys.argv[2] )[0]


template_ref = []
template_pos = []
template_names = []
template_atoms = []

prev = -99999
for chain in first_structure:
    for residue in chain:

        residue_name = residue.get_resname()

        ref_atoms = []
        ref_atoms.append( residue[reference_atoms[0]] )
        ref_atoms.append( residue[reference_atoms[1]] )
        ref_atoms.append( residue[reference_atoms[2]] )
        template_ref.append( ref_atoms )

        residue_pos = []
        atom_names = []
        atoms = []
        for atom in residue:
            residue_pos.append( atom.coord )
            atom_names.append( atom.name )
            atoms.append( atom)
        template_pos.append( residue_pos)
        template_names.append( atom_names)
        template_atoms.append( atoms )

if resname != residue_name:
    print( 'ERROR residue names do not match: ', resname, residue_name)
    exit(1)
    
#print( "# residue ", residue_name)
#print( len(template_names), 'templates')

with open( sys.argv[2] ) as r:
    lines = r.readlines()

all_pos = []
for l in lines:
    if l[:4] != 'ATOM' and l[:6] != 'HETATM':
        continue
    all_pos.append( Position(l))
#print( '# pos:', len(all_pos))

prev = -99999
residue = []
for i in range(0, len(lines)):
    l = lines[i]
    if l[:4] != 'ATOM' and l[:6] != 'HETATM':
        print( l.strip()) #   + ' - ')
        continue
    if l[17:20] != residue_name:
        print( l.strip() ) #  + ' + ')
        continue
    resid = int( l[22:26] )
    if prev != resid:
        if len(residue) > 0:
            #print( 'before insert all pos: ', len(all_pos))
            all_pos = Insert( all_pos, residue , template_ref, template_pos, template_atoms, reference_atoms, second_structure)
            #print( 'after insert all pos: ', len(all_pos))
            sys.stdout.flush()
            residue = []
        prev = resid
        #print( 'reset')
    residue.append(l)

    
if len(residue) > 0:
    Insert( all_pos, residue , template_ref, template_pos, template_atoms, reference_atoms, second_structure)



