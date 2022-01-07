#!/usr/bin/python3

from Bio import PDB
from Bio import AlignIO
import sys

pdb_file = sys.argv[1]
chain = sys.argv[2]
ali_file = sys.argv[3]
ali_id = int( sys.argv[4] )

alignment = AlignIO.read( ali_file, 'clustal')

nr = len( alignment)



if ali_id >= nr:
    print( "ERROR: sequence id too small:", ali_id, nr )
    exit(1)

    
vals = []
for i in range( 0, len( alignment[ ali_id ] )):
    aa = alignment[ ali_id][i]
    if aa == '-':
        print( '-',end=' ' )
        continue
    count = 0
    for j in range( 0, nr):
        if j == ali_id: continue
        if alignment[j][i] == aa:
            count += 1

    vals.append( float(count)/float(nr-1) )

eidi = -1
previd = -99999
with open( pdb_file) as r:
    for l in r:
        l = l.strip()
        if "ATOM" != l[0:4] or l[21] != chain:
            print( l)
        else:
            if previd != l[22: 
            print( l[:61] + " ".format() + l[72:] )
