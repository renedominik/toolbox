#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             22.03.2022           ##
#######################################



import Bio.PDB
#import Bio.AlignIO
import sys
from Bio.SVDSuperimposer import SVDSuperimposer
from collections import OrderedDict

def Consistency( l1, l2):
    for a1,a2 in zip(l1,l2):
        #print( a1.get_name(),a2.get_name())
        if a1.get_name()[0] != a2.get_name()[0]:
            return False
    return True

def Erase( diggi, key1, key2 ):
    newbi = {}
    for k,v in diggi.items():
        s = k.split(':')
        if s[0] != key1 and s[1] != key2:
            newbi[k] = v
    return newbi

ref = 'O', 'N'

first_ref_atoms = []
first_all_atoms = []
second_residues = []
second_ref_atoms = []

first_file = sys.argv[1]
second_file = sys.argv[2]
resname = sys.argv[3]


pdb_parser = Bio.PDB.PDBParser( QUIET=True )

first_structure = pdb_parser.get_structure( "first", first_file )[0]
second_structure = pdb_parser.get_structure( "second", second_file )[0]


for chain in first_structure:
    for residue in chain:
        for atom in residue:
            first_all_atoms.append( atom )
            if atom.get_name()[0] in ref:
                first_ref_atoms.append( atom)
print( len(first_ref_atoms), 'non H atoms found in first structure')
                    
for chain in second_structure:
    for residue in chain:
        if residue.get_resname() == resname:
            second_residues.append( residue)
            refs = []
            for atom in residue:
                if atom.get_name()[0] in ref:
                    refs.append(atom)
            second_ref_atoms.append( refs)

print( len( second_residues), 'residues found in second structure of type', resname, 'length:', len(second_ref_atoms[0]))


aligner = Bio.PDB.Superimposer()  
#supi = SVDSuperimposer

import itertools, copy, numpy as np

best_score = 9999999
best_rmsd = 999999
best_perm = -1

count = 0
for second_ref,second_all in zip(second_ref_atoms,second_residues):
    #print( 'permute')
    for permutation in itertools.permutations(second_ref):
        ### second_all is NOT permutated !!! ###
        if not Consistency( permutation, first_ref_atoms): continue

        aligner.set_atoms( first_ref_atoms, permutation ) # place latter on former
        #supi.set( first_ref_atoms, permutation)
        #supi.run()
        #print( 'RMSD seed atoms:', supi.get_rms())
        #if supi.get_rms() > 1.0: continue
        
        if aligner.rms > 1.5: continue
        print( "RMSD seed atoms",  aligner.rms)

        second_cp = copy.deepcopy( second_all) 
        #print(  list(second_cp.get_atoms())[0].coord )
        aligner.apply(second_cp)
        
        #rot, tran = sup.get_rotran()
        #second_cp = dot(second_cp, rot) + tran

        m = []
        trans = {}
        for a1 in first_all_atoms:
            n = []
            for a2 in second_cp:
                x =  np.linalg.norm( a1.coord - a2.coord )
                n.append(x)
                trans[a1.get_name() + ':' + a2.get_name() ] =  x
            m.append(n)
        
        m = np.array( m)

        #print( m.shape )

        minima = np.argmin( m, axis=1)
        #print( minima)

        rmsd = 0
        maxi = -99
        at1 = []
        at2 = []
        for i1 in range( len(minima)):
            i2 = minima[i1]
            value = m[i1][i2]
            if value < 0.1:
                at1.append( first_all_atoms[i1])
                at2.append(  list(second_cp.get_atoms())[i2] )
            rmsd += value * value
            maxi = max( maxi, value)
            
        rmsd = np.sqrt( rmsd / float(len(minima)))
        print( 'rmsd:', aligner.rms, rmsd, 'max:', maxi)
        if aligner.rms < best_score:
            best_score = aligner.rms
            best_trans = trans
            best_mol = second_cp
            best_rmsd = rmsd

            
print( 'best match rmsd: ' , best_rmsd , ' best max:', best_score )
best_trans = dict(sorted(best_trans.items(), key= lambda x:x[1]))
count = 0
while len(best_trans) > 0:
    k,v = list( best_trans.items() )[0]
    s = k.split(':')
    print( s[1], s[0], v )
    if s[0][0] != s[1][0]:
        print( "WARNING: atom types do not match!!!")
    best_trans = Erase( best_trans, s[0], s[1] )
    count += 1

print( count, 'matches found')

io = Bio.PDB.PDBIO()
io.set_structure( best_mol )
io.save( "best.pdb" )
