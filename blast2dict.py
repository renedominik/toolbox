#!/usr/bin/python3

import sys

query = ""
partner = ""

w = open( sys.argv[2], 'w' )

print( "identity={", file=w)

with open(sys.argv[1]) as r:
    for l in r:
        if l[:6] == "Query=":
            query = l.split()[1]
        if l[0] == '>':
            partner = l.split()[0][1:]
        if "Identities" in l:
            value = float( l.split()[7][1:-3] ) / 100 
            print( '"' + query + ',' + partner + '" : ' + str(value) + ',' , file=w)

print( "}", file=w)
w.close()
