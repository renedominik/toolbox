#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import numpy as np

# this script is supposed to write both rosetta score as well as the degree of insertion into the binding pocket for each docking pose (PDB)


#####  SETTINGS, to be adjusted for each receptor / PDB ###########
center = np.array( [61.77050953793994, -25.39900084781689, -7.815874523103022] )
#radius = 15.13
radius = 13.5
###################################################################


if len(sys.argv) < 3:
    print "USAGE",sys.argv[0], " PDB_LIST_column1_directory  CHAIN  OUT_FILE (optional:ROSETTA_SCORE_TERMS)\n"
    exit(1)
    
# define arguments; file with paths to pdbs of models, peptide chain in pdb, out-file and the score term
pdb_list = sys.argv[1]
chain = sys.argv[2]
out_file = sys.argv[3]

score_terms = []

if len(sys.argv) > 4:
    score_terms = sys.argv[4:]

w = open( out_file, 'w')

w.write( "# PDB NR_CA_IN_POCKET  ZMIN ")
for st in score_terms:
    w.write( st + " ")
w.write('\n')

# go through list of pdbs and open pdb files with the name on the first column
with open( pdb_list ) as f:
    for l in f:
        count = 0
        zmin = 1e10
        score = ["0.0"] * len(score_terms)
        l = l.strip()
        li = l.split() 
        with open( li[0] ) as fx:
            for lx in fx:
            
                # select CA atoms from peptide chain and collect coordinates, define degree of insertion
                if lx[:4] == "ATOM":
                    if lx[21] == chain and lx[12:16].replace( ' ','') == "CA" : 
                        x = float( lx[30:38] )
                        y = float( lx[38:46] )
                        z = float( lx[46:54] )

                        if z < zmin:
                            zmin = z
                    
                        pos = np.array( [x,y,z] )
                        # check whether they are inside binding pocket
                        dist= np.linalg.norm( pos - center)
                        if dist <= radius:
                            count += 1

                # collect rosetta energy score            
                else:
                    for ii in range(0,len(score_terms)):
                        if score_terms[ii] in lx:
                            #print lx,
                            score[ii] = lx.split()[-1]
                    

        # print model, count of CA in pocket, degree of insertion, score
        w.write( l + '  ca_n ' + str( count ) + '  zmin ' + str(zmin) + ' ' )
        for s in score:
            w.write( s + ' ' )
        w.write( '\n' )


w.close()

                



 
