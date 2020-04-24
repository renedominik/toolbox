#!/usr/bin/python3

import sys

if len(sys.argv) < 3:
    print( "USAGE:", sys.argv[0], "IN OUT (optional:NR_LIGANDS)")
    exit(1)


nr_ligs = 0
if len(sys.argv) > 3:
    nr_ligs = int( sys.argv[3])

header = []
count = -1
seqs = [ "" , "" ]
with open( sys.argv[1] ) as f:
    f.readline()
    for l in f:
        if len(l) < 15 or "*" in l: continue
        #print(l)
        c = l.split()
        if len(c) == 2:
            count += 1
            if len(header) < 2:
                header.append(c[0])
            elif c[0] not in header:
                print( "WARNING: header does not match already defined header:", header)
                print( l, end="")

            seqs[ count % 2] += c[1] 
#print( sys.argv)
#print( header, seqs)

# inverted order ???
with open( sys.argv[2], 'w' ) as w:
    w.write( "C; alignment converted from clustal format\n\n")
    w.write( ">P1;" + header[1] + "\nstructureX:" + header[1] + ":1 :R:" + str(len(seqs[1])-seqs[1].count('-')+nr_ligs) + " :R: : : : \n" + seqs[1] )
    for i in range(0, nr_ligs):
        w.write('.')
    w.write("*\n\n" ) 
    w.write( ">P1;" + header[0] + "\nsequence:" + header[0] + ":1 : :" + str(len(seqs[0])-seqs[0].count('-')+nr_ligs) + " : : : : : \n" + seqs[0] ) 
    for i in range(0, nr_ligs):
        w.write('.')
    w.write("*\n" ) 
