#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

count = 1

infile = sys.argv[1]
prefix = sys.argv[2]
ending = ".pdb"

name = '{:04d}'.format(count)
w = open( prefix + name + ending , 'w' )

with open( infile ) as r:
    for l in r:
        w.write(l)
        if "ENDMDL" in l:
            w.close()
            count += 1
            name = '{:04d}'.format(count)
            w = open( prefix + name + ending , 'w' )

w.close()
