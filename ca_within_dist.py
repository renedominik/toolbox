#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import numpy as np

if len(sys.argv) < 5:
    print "USAGE",sys.argv[0], " PDB  CHAIN RESID  OUT_FILE\n"
    exit(1)

pdb_file = sys.argv[1]
chain = sys.argv[2]
resid = sys.argv[3]
out_file = sys.argv[4]

ca = []
atoms = []


print "scores collected"
w = open( out_file, 'w')

with open( pdb_file ) as f:
    for l in f:
        if l[:4] != "ATOM"  or l[21] != chain or l[22:26].replace(' ','') != resid or l[12:16].replace(' ','') != "CA": continue  

        x = float( l[30:38] )
        y = float( l[38:46] )
        z = float( l[46:54] )
        ca = [x,y,z]
        print l,

        
with open( pdb_file ) as f:
    for l in f:
        if l[:4] != "ATOM"  or l[12:16].replace(' ','') != "CA": continue  

        x = float( l[30:38] )
        y = float( l[38:46] )
        z = float( l[46:54] )

        dist = np.linalg.norm( ca - np.array([x,y,z]) )
        if dist < 8:
            w.write( str(dist) + '\t' + l )
        
