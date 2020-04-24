#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

if len(sys.argv) < 2:
    print("USAGE",sys.argv[0],"PDB")
    exit(1)

prefix = sys.argv[1][:-4] + "_" 
w = open( "/dev/null", 'w')
with open( sys.argv[1] ) as f:
    for l in f:
        if l[:5] == "MODEL":
            w.close()
            name = '{}{:06d}{}'.format( prefix, int(l.split()[-1]), ".pdb" )
            print( name )
            w = open( name , 'w')
        elif l[:4] == "ATOM":
            w.write(l)

w.close()
