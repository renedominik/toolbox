#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import numpy as np

# this script is supposed to write both rosetta score as well as the degree of insertion into the binding pocket for each docking pose (PDB)

if len(sys.argv) < 2:
    print "USAGE",sys.argv[0], " PDB \n"
    exit(1)
    
pdb = sys.argv[1]

first_id = 'R'
second_id = 'D'

first_chain = []
second_chain = []

with open( pdb ) as fx:
    for lx in fx:
        if  lx[12:16].replace( ' ','') == "CA" : 
            #lx[:4] == "ATOM" and
            lx = lx.strip()
            
            chain = lx[21]
            
            if chain == first_id:
                first_chain.append( lx )
            elif chain == second_id:
                second_chain.append( lx )
            else:
                print "WARNING: unexpected chain:", chain

for f in first_chain:
    x = float( f[30:38] )
    y = float( f[38:46] )
    z = float( f[46:54] )
    pos_f = np.array( [ x, y, z ] )

    for s in second_chain:
        x = float( s[30:38] )
        y = float( s[38:46] )
        z = float( s[46:54] )
        pos_s = np.array( [ x, y, z ] )

        dist = np.linalg.norm( pos_f - pos_s )

        if dist < 15:
            print dist, f, s

                



 
