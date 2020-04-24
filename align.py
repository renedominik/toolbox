#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62

# read first seq:
for sr in SeqIO.parse( open( sys.argv[1] ),'fasta'):
    s1 = sr.seq

# read second seq:
for sr in SeqIO.parse( open( sys.argv[2] ),'fasta'):
    s2 = sr.seq

# global alignment
ali = pairwise2.align.globalds( s1, s2,blosum62, -10, -1) 

# format first alignment
formatted = format_alignment( *ali[0])

# break into lines:
rows = formatted.split('\n')

#output actual sequences:
print rows[0]
print rows[2]

    
