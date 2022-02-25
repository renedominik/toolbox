#!/usr/bin/python3

##############################
# author: Rene Staritzbichler
# 10.01.21
##############################

from Bio import PDB
from Bio import AlignIO
from Bio import SeqUtils
import sys


if len( sys.argv) < 5:
    print( 'script writes sequence conservation into temperature factor of output PDB')
    print( "USAGE:", sys.argv[0], 'PDB CHAIN ALIGNMENT.clw ROW')
    print( "\tALIGNMENT is Clustal formatted multiple sequence alignment")
    print( "\tROW specifies the sequence in the alignment that belongs to PDB")
    print( '\tROW starts with 0')
    print( '\tCHAIN is needed because alignments are single chain only')
    print( '\tcall multiple times if you want to color more than one chain')
    print()
    help(SeqUtils.IUPACData)
    exit(1)


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
seq = []
for i in range( 0, len( alignment[ ali_id ] )):
    aa = alignment[ ali_id][i]
    if aa == '-':
        print( '-',end=' ' )
        continue
    seq.append( aa )
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
            new_Id = int(l[22:26])
            if previd != new_Id:
                previd = new_Id
                eidi += 1
            aa = SeqUtils.IUPACData.protein_letters_3to1[ l[ 17:20 ].title()]
            if aa != seq[eidi]:
                print( "ERROR: sequence in alignment and pdb do not match:", eidi, seq[eidi],aa)
                exit(1)
            print( l[:60] + "{:6.2f}".format( vals[eidi] ) + l[66:] )
