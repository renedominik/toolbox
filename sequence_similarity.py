#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import sys
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO
from Bio.Align import substitution_matrices

BLOSUM = substitution_matrices.load('BLOSUM62')

def CountIdentical( s1, s2):
    if len(s1) != len(s2):
        print( "ERROR: length of strings does not match: ", len(s1),len(s2))
    count = 0
    for a,b in zip(s1,s2):
        if a == b and a != '-':
            count+=1
    return count


first = sys.argv[1]
if len(sys.argv) < 3:
    second = first
else:
    second = sys.argv[2]


# read first seq:
for s1 in SeqIO.parse( open( first ),'fasta'):
    for s2 in SeqIO.parse( open( second ),'fasta'):
        print( s1.id, s2.id)
        ali = pairwise2.align.globalds( s1.seq, s2.seq, BLOSUM, -10, -1)
        formatted = format_alignment( *ali[0])
        rows = formatted.split('\n')
        count = float( CountIdentical( rows[0], rows[2] ))
        n1 = len(s1.seq)
        n2 = len(s2.seq)
        print( s1.id, n1, s2.id, n2, count, 2.0 * count / float( n1+n2), count / min( n1, n2))
        print( rows[0])
        print( rows[2])
        print()
