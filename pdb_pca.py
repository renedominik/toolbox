#!/usr/bin/python3

### copyright: rene staritzbichler, 27.8.20

import pdb_functions as pdb
import numpy as np
from sklearn.decomposition import PCA
import sys

if len(sys.argv) < 2:
    print( "USAGE: ", sys.argv[0], "PDB (optional: CHAIN1 ..)")
    exit(1)

pos = []
chains = []
if len(sys.argv) > 2:
    chains = sys.argv[2:]


with open( sys.argv[1]) as f:
    for l in f:
        if l[:4] != "ATOM" or (len(chains)>0 and pdb.chain(l) not in chains):
            continue
        pos.append( pdb.position(l) ) 

pos = np.array( pos)
print( 'first pos:', pos[0])
print( pos.shape)

pca = PCA(n_components=3)
newpos = pca.fit(pos)

print( pca.components_)

print( pca.explained_variance_)

### test by hand implementation: ###
print( 'first pos:', pos[0])

cms = np.mean( pos, axis=0)
print( 'cms:', cms)

# standardization
d = 0.0
for p in pos:
    d += np.linalg.norm( p - cms )**2
d = np.sqrt( d / float( len(pos) - 1 ) )

print( 'rgyr:', d)

zpos = []
for p in pos:
    zpos.append( (p-cms) / d )
zpos = np.array(zpos)

print( 'first pos:', pos[0])

print( zpos.shape)

# covariance matrix
cvm = np.cov( pos.T ) #.transpose() )

print( cvm.shape)

# solve eigen gleichung
w,v = np.linalg.eig( cvm )

print( w,'\n', v.T )

