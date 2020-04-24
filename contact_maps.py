#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import Bio.PDB
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm, LogNorm

## DUPLICATE !! ## 
def ShortestDistance( r1 , r2 ):
    maximum = 21
    minimum = 1e12
    types = ['C','CA','O','N', 'HA', 'H' ]
    for a1 in r1:
        if a1.get_name() in types: continue
        for a2 in r2:
            if a2.get_name() in types: continue
            d = a2 - a1
            if d < minimum:
                minimum = d
            elif d > maximum:
                return 
    return minimum


def Contact( dist, first, second):
    if dist == None or dist >= second:
        return 0.0
    elif dist <= first:
        return 1.0
    else:
        return 0.5 * ( 1.0 + np.cos( np.pi * (dist-first) / (second-first) ) )


# works for 2 chain PDBs only!!!
def ContactMap( files, chain, first, second): 
    pdb_parser = Bio.PDB.PDBParser( QUIET=True )
    data = []
    ii = 0
    for f in files:
        structure = pdb_parser.get_structure( f, f )[0]
        receptor = []
        ligand = []
        for c in structure:
            if c.get_id() == chain:
                ligand = c
            else:
                receptor = c 
        if ii == 0:
            print len(ligand), len(receptor)
            data = np.zeros( [ len(ligand), len(receptor) ] )
            res_receptor = []
            for r in receptor:
                res_receptor.append( r.get_resname() )
            res_ligand = []
            for l in ligand:
                res_ligand.append( l.get_resname() )
        if ii % 250 == 0:
            print ii,
            sys.stdout.flush()
        ii += 1
        i = 0
        for l in ligand:
            j = 0
            for r in receptor:
                #d =  ShortestDistance( l , r )
                #x = Contact(d, first, second )
                #if x > 0:
                #    print i,j,d,x,l.get_resname(), r.get_resname()
                #data[i][j] += x
                data[i][j] += Contact( ShortestDistance( l , r ) , first, second )                
                j += 1
            i += 1
    print
    return data / float(len(files)), res_ligand, res_receptor


dirs = [  # "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq1/models/",
          # "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq4/models/",
          # "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq7_1-13/models/",
          # "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq1/models/",
          # "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq4/models/",
          # "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq7_1-13/models/",
           "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq2/models/",
          #  "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq2/models/",
]

#dirs = ["tmp/"]


first = 3
last = 9

if len(sys.argv) > 2:
    first = int( sys.argv[1] )
    last = int( sys.argv[2] )

print "contact parameters:", first, last

for directory in dirs:
    files = []
    print directory
    if os.path.isfile( directory + "../top10k.txt" ):
        print "read top scoring from file",  directory + "../top10k.txt"
        with open(  directory + "../top10k.txt" ) as f:
            for l in f:
                files.append( directory + "../" + l.strip() )
    else:
        for f in os.listdir( directory):
            if ".pdb" in f:
                files.append( directory + f )
    print len(files) , "files"
    contact_map, res_ligand, res_receptor = ContactMap( files, 'B', first, last )
    (a,b) = np.shape( contact_map )
    print a, b
    with open( directory + "contact_map_" + str(first) + "_" + str(last) + ".txt", 'w') as out:
        out.write( 'x\t')
        for r in res_receptor:
            out.write( r + '\t')
        out.write( '\n' )
            
        for j in range( 0, a ):
            out.write( res_ligand[j] + '\t' )
            #print res_receptor[j], len( contact_map[j] ), 
            for k in range( 0, b ):
                out.write( str( contact_map[j][k] ) + '\t' )
            out.write( '\n')

                        
    cmap = plt.cm.get_cmap("hot") # "seismic")
    plt.figure()
    plt.pcolormesh( contact_map, cmap=cmap) #, interpolation='nearest')
    #plt.imshow( contact_map, cmap="seismic", interpolation='nearest')
    plt.savefig( directory + "contactmap_" + str(first) + "_" + str(last) + ".png")
    plt.savefig( directory + "contactmap_" + str(first) + "_" + str(last) + ".pdf")
