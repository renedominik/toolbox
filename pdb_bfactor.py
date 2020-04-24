#!/usr/bin/python3

##################################
## @Copyright Rene Staritzbichler
## 22.4.20
##################################

import sys

if len(sys.argv) < 3:
    print( "EXAMPLE:", sys.argv[0], "IN.pdb residues: A: 1 - 57 68 B: 5 - 122 atoms: C CA N value: 0 else: 1 OUT.pdb")
    exit(1)

infile = sys.argv[1]
outfile = sys.argv[-1]
typ = sys.argv[2]

beg = -1
end = -1

if typ == "residues:":
    beg = 22
    end = 26
elif typ == "atoms:":
    beg = 6
    end = 11
else:
    print( "type rubbish" )
    exit(2)

    
ids = []
current = 3
prev = -1
chain = 'x'
while sys.argv[current] != "atoms:":
    if ':' in sys.argv[current]:
        chain = sys.argv[current][0]
    elif sys.argv[current] != '-':
        ids.append( [chain, int(sys.argv[current])] )
        prev = ids[-1]
    else:
        current += 1
        for i in range( ids[-1] , int( sys.argv[current] ) ):
            ids.append( [chain, i]  )
    current += 1
current += 1
atoms = []
while sys.argv[current] != "value:":
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
            if [chain,nr] in ids and l[12:16].strip() in atoms:
                w.write( l[:60] + ("%6.2f" % value ) + l[66:] )
            else:
                w.write( l[:60] + ("%6.2f" % other ) + l[66:] )


                
