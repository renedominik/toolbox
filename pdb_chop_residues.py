#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             28.04.2020           ##
#######################################



import sys

if len(sys.argv) < 2:
    print( "USAGE", sys.argv[0], "PDB A: 1 4 9 - 12 B: 23 - 55 CARVED.pdb CHOPPED.pdb" )
    exit(1)

infile = sys.argv[1]
outfile1 = sys.argv[-2]
outfile2 = sys.argv[-1]

chain = "x"
residues = []

current = 2
while current < len(sys.argv) - 2:
    if ":" in sys.argv[current]:
        chain = sys.argv[current][0]
    elif sys.argv[current] != '-':
        residues.append( [chain, int(sys.argv[current]) ] )
    else:
        current += 1
        print( residues[-1], sys.argv[current] )
        for i in range( residues[-1][1]+1 , int(sys.argv[current])+1 ):
            residues.append( [chain , i ] )
    current += 1

print( "residues:" , residues )

with open( outfile1, 'w') as w1:
    with open( outfile2, 'w') as w2:
        with open( infile ) as r:
            for l in r:
                if l[0:4] != "ATOM": 
                    w1.write(l)
                    continue
                if [l[21],int(l[22:26])] not in residues:
                    w1.write(l)
                else:
                    w2.write(l)
