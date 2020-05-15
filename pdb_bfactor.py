#!/usr/bin/python3

##################################
## @Copyright Rene Staritzbichler
## 22.4.20
##################################

import sys

if len(sys.argv) < 3:
    print( "EXAMPLE:", sys.argv[0], "IN.pdb residues: A: 1 - 57 68 B: 5 - 122  atoms: C CA N  value: 1.0  else: 0.0  OUT.pdb")
    print( "EXAMPLE:", sys.argv[0], "IN.pdb residues: A: all  B: all  atoms: all  value: 1.0  else: 0.0  OUT.pdb")
    exit(1)

infile = sys.argv[1]
if ".pdb" not in infile:
    print( "you have to provide an input .pdb file")
    exit(3)
outfile = sys.argv[-1]
if ".pdb" not in outfile:
    outfile = "bfactor.pdb"
    print( "OUT.pdb not correctly provided, changed to 'bfactor.pdb'")
typ = sys.argv[2]

beg = -1
end = -1

if "res" in typ:
    beg = 22
    end = 26
else:
    print( "type rubbish" )
    exit(2)

    
ids = []
current = 3
prev = -1
chain = 'x'
while "at" not in sys.argv[current]:
    if ':' in sys.argv[current]:
        chain = sys.argv[current][0]
    elif sys.argv[current] != '-':
        if sys.argv[current] == 'all':
            ids.append( [chain, sys.argv[current] ] )
        else:
            ids.append( [chain, int(sys.argv[current])] )
            prev = ids[-1]
    else:
        current += 1
        print( ids[-1], sys.argv[current] )
        for i in range( ids[-1][1]+1 , int( sys.argv[current] ) + 1 ):
            ids.append( [chain, i]  )
    current += 1
current += 1
atoms = [] 
while "val" not in sys.argv[current]:
    atoms.append( sys.argv[current] )
    current += 1
    
current += 1
value = float( sys.argv[current] )
current += 2
other = float( sys.argv[current] )

print( "ids:", ids)
print( "atoms:", atoms )
print( value, other )

with open( outfile, 'w') as w:
    with open( infile ) as r:
        for l in r:
            if "ATOM" not in l:
                w.write(l)
                continue
            chain = l[21]
            nr = int( l[beg:end] )
            if ( [chain,nr] in ids or [chain,'all'] in ids ) and ( atoms[0] == 'all' or l[12:16].strip() in atoms):
                w.write( l[:60] + ("%6.2f" % value ) + l[66:] )
            else:
                w.write( l[:60] + ("%6.2f" % other ) + l[66:] )


                
