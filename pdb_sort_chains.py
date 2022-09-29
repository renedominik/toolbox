#!/usr/bin/python3
import sys

# usage skipped for speed reasons

# 2 arguements: PDB_FILE STRING_TO_KEEP
keep = sys.argv[2]

# read file to check order
chains = []
with open( sys.argv[1] ) as r:
    for l in r:
        if 'ATOM' == l[:4] or 'HETATM' == l[:6]:
            chains.append( l[21] )
sortiert =  list(set(chains))
sortiert.sort()

# check if not alphabetical
if sortiert[0] != chains[0] or sortiert[-1] != chains[-1]:
    print( sys.argv[1] )

# do nothing if alphabetical
#if sortiert[0] == chains[0] and sortiert[-1] == chains[-1]:
#    exit(1)

# otherwise sort
from collections import defaultdict
import os
chains = defaultdict(list)
lines = []
with open( sys.argv[1] ) as r:
    for l in r:
        if 'ATOM' == l[:4] or 'HETATM' == l[:6]:
            chains[l[21]].append(l)
        elif keep in l:
            lines.append(l)

sortiert = list(chains.keys())
sortiert.sort()

with open( 'tmp.pdb', 'w') as w:
    for a in sortiert:
        #print(a)
        for l in chains[a]:
            print( l, end='', file=w)
        print( 'TER', file=w)
    for l in lines:
        print(l, end='', file=w)
os.rename( 'tmp.pdb', sys.argv[1] )
