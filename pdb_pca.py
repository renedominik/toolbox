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
        if l[:4] != "ATOM" or (len(chains)>0 and chain(l) not in chains):
            continue
        pos.append( pdb.position(l) ) 

pos = np.array( pos)
print( pos.shape)

pca = PCA(n_components=3)
newpos = pca.fit(pos)

print( pca.components_)
