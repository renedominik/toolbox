#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

if len(sys.argv) < 3:
    print "USAGE:", sys.arg[0], " FILE_WITH_DIST_TO_NATIVE  FILE_WITH_BINDING_POCKET_STATS"
    exit(1)

first = {}

with open( sys.argv[1]) as f:
    for l in f:
        c = l.split()
        first[ c[0] ] = c[1]




with open( sys.argv[2]) as f:
    for l in f:
        if l[0] == "#": continue
        
        c = l.split()
        if c[0] in first:
            print c[0][:4] + " & & " + c[1] + " & " + c[2] + " & " + first[c[0]] + " & " + c[3] + " & " + c[4] + " \\\\"
        else:
            print c[0][:4] + " & & " + c[1] + " & " + c[2] + " &  & " + c[3] + " & " + c[4] + " \\\\"
