#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import numpy as np
import sys
import vector_functions as vf
import pdb_functions as pdb

chain = 'A'
atom_ref1 = 187
atom_ref2 = 124

#nd2 = np.array( [ 52.554, -25.192 ,  5.839 ] )
#cb = np.array( [ 54.231, -24.900 ,  4.134 ] )
#ref = nd2 - cb

res = 91
atom_type1 = 'CB'
atom_type2 = 'ND2'

if len(sys.argv) == 8:
    file_name = sys.argv[1]
    chain = sys.argv[2]
    atom_ref1 = int( sys.argv[3] )
    atom_ref2 = int( sys.argv[4] )
    res = int( sys.argv[5] )
    atom_type1 = sys.argv[6]
    atom_type2 = sys.argv[7]
    
else:
    print "==>  NOTE: default settings used!!!  <=="

print sys.argv,
    
a1 = []
a2 = []
r1 = []
r2 = []

with open( file_name ) as f:
    for l in f:
        
        if l[:4] != "ATOM" or l[21] != chain: continue
        
        atom_name = pdb.atom_name( l )
        
        resid = pdb.resid(l)
        
        if atom_name == "CA":
            if resid == atom_ref1:
                #print l
                r1 = pdb.position(l)
            elif resid == atom_ref2:
                #print l
                r2 = pdb.position(l)
        else:
            if resid == res:
                if atom_name == atom_type1:
                    #print l
                    a1 = pdb.position(l)
                elif atom_name == atom_type2:
                    #print l
                    a2 = pdb.position(l)
                
ref = r2 - r1
sc = a2 - a1

#print "graphics 0 cone {" + str(a1[0]) + " " + str(a1[1]) + ' ' + str(a1[2]) + '} {' + str(a2[0]) + ' ' + str(a2[1]) + ' ' + str(a2[2]) + '} radius 0.2 resolution 21'
#print "graphics 0 cone {" + str(r1[0]) + " " + str(r1[1]) + ' ' + str(r1[2]) + '} {' + str(r2[0]) + ' ' + str(r2[1]) + ' ' + str(r2[2]) + '} radius 0.2 resolution 21'


print "angle:",np.degrees( vf.angle( ref, sc ) )
