#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             24.01.2022           ##
#######################################

import sys
import numpy as np
import pdb_functions as pdb

first = []
with open( sys.argv[1] ) as f:
    for l in f:
        if 'ATOM' == l[:4] or 'HETATM' == l[:6]: 
            first.append(l)
second = []
with open( sys.argv[2] ) as f:
    for l in f:
        if 'ATOM' == l[:4] or 'HETATM' == l[:6]: 
            second.append(l)



print( len(first), len(second) )

m = []
for i1 in range( len(first)):
    n = []
    for i2 in range( len(second)):
        n.append( np.linalg.norm( pdb.position(first[i1]) - pdb.position(second[i2]) ))
    m.append(n)

m = np.array( m)

print( m)

print( m.shape )

minima = np.argmin( m, axis=1)
#print( minima)

#exit(1)

for i1 in range( len(first)):
    index = minima[i1]
    value = m[i1][index]
    print( i1, index, value)
    print( first[i1],second[index])
    
    

        
