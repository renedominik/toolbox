#!/usr/bin/python3
import sys

# read file to check order
chains = []
with open( sys.argv[1] ) as r:
    for l in r:
        if 'ATOM' == l[:4] or 'HETATM' == l[:6]:
            chains.append( l[21] )
sortiert =  list(set(chains))
sortiert.sort()

# check if not alphabetical
#if sortiert[0] != chains[0] or sortiert[-1] != chains[-1]:
#    print( sys.argv[1] )

# do nothing if alphabetical
if sortiert[0] == chains[0] and sortiert[-1] == chains[-1]:
    exit(1)

# otherwise sort
from collections import defaultdict
import os
chains = defaultdict(list)
with open( sys.argv[1] ) as r:
    for l in r:
        if 'ATOM' == l[:4] or 'HETATM' == l[:6]:
            chains[l[21]].append(l)

sortiert = list(chains.keys())
sortiert.sort()

with open( 'tmp.pdb', 'w') as w:
    for a in sortiert:
        #print(a)
        for l in chains[a]:
            print( l, end='', file=w)
        print( 'TER', file=w)
os.rename( 'tmp.pdb', sys.argv[1] )
