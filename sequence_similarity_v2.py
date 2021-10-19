#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import sys, os
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
#from Bio import SeqIO
from Bio.Align import substitution_matrices
from joblib import Parallel, delayed

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

data = []
# read first seq:
with open( first ) as f:
    for l in f:
        cols = l.split()
        data.append( cols )


nr_jobs = 10

def run( i ):
    count = 0
    for i1 in range( 0, len(data) -1 ):
        for i2 in range( i1+1, len(data)):
            count += 1
            if count % nr_jobs != i:
                continue
            s1=data[i1][1]
            s2=data[i2][1]
            h1 = data[i1][0]
            h2 = data[i2][0]
            if h1 == h2 or s1 == s2: continue
            #print( s1, s2 )
            ali = pairwise2.align.globalds( s1, s2, BLOSUM, -10, -1)
            formatted = format_alignment( *ali[0])
            rows = formatted.split('\n')
            count = float( CountIdentical( rows[0], rows[2] ))
            n1 = len(s1)
            n2 = len(s2)
            print( h1, n1, h2, n2, count, 2.0 * count / float( n1+n2), count / min( n1, n2))
            #print( rows[0])
            #print( rows[2])
            #print()



pids = []
for i in range(1,nr_jobs+1):
    n = os.fork()
    if n==0:
        run( i)
    else:
        pids.append(n)

for p in pids:
    os.waitpid(p,0)
