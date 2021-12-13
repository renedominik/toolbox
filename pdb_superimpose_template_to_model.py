#!/usr/bin/python3


import Bio.PDB
import Bio.AlignIO
import sys, copy

#first_atoms = [] # template residue/cofactor
#second_atoms = [] # full protein

second_residues = []  # this stores any residue type to be replaced (one residue is a single entry in this list of lists)

pdb_parser = Bio.PDB.PDBParser( QUIET=True )
first_structure = pdb_parser.get_structure( "first", sys.argv[1] )
second_structure = pdb_parser.get_structure( "second", sys.argv[2] )

aligner = Bio.PDB.Superimposer()
io = Bio.PDB.PDBIO()

#################   ADJUST HERE  ################################
# selection of atoms used for aligning molecules
alis = [ 'NA', 'NB', 'NC', 'ND' , 'CHA', 'CHB', 'CHC', 'CHD' ] 
#################################################################

###  extract full molecule, its resname and its atoms found in 'alis' from first structure
resname = ""
first_residue = []
template = []
count = 0
for model in first_structure.get_list():
    for chain in model.get_list():
        for residue in chain.get_list():
            resname = residue.get_resname()
            first_residue = residue  # all atoms of residue
            for atom in residue.get_list():
                if atom.get_name() in alis:
                    template.append( atom)  # only those atoms defined in 'alis' are included
                if atom.get_name()[0] == 'C':
                    count += 1
print( "length template: ", len(first_residue), len( template), len(alis))
print( 'nr carbons in template:', count)


resid = 0
count = 0
for model in second_structure.get_list():
    for chain in model.get_list():
        for residue in chain.get_list():
            # consider only residues with identical type than template
            if residue.get_resname() != resname: continue
            # create sublist of atoms in the same order than template
            first = []
            for atom1 in template:
                count = 0
                for atom2 in residue:
                    if atom2.get_name() == atom1.get_name():
                        first.append( atom2)
                    if atom2.get_name()[0] == 'C':
                        count += 1

            if count == 50:
                io.set_structure( residue )
                io.save( 'gbf_' + str(resid) + '.pdb')
            # some checks
            print( "lengths: ", len(residue), len(first), 'carbon count:', count)
            if len( alis) != len( first):
                print( "ERROR: lengths do not match: ", len(alis), len(first))
                exit(1)
            # check that atomnames are in same order
            for a1, a2 in zip( template, first):
                if a1.get_name() != a2.get_name():
                    print( "ERROR:", a1.get_name() ,  a2.get_name())
                    exit(1)

            # align the subsets
            aligner.set_atoms( first, template ) # place latter on former
            # apply same rotation to the entire template molecule
            cp = copy.deepcopy( first_residue)  # e.g. GBF with long tail
            aligner.apply( cp ) # move full molecule into model
            res = residue.get_full_id()
            io.set_structure( cp )
            io.save( sys.argv[3] + '_' + res[2] + str(res[3][1]) + '.pdb')  # write to pdb that has chain and residue id in its name
            resid += 1

           


