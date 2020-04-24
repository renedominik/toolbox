#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

seq = sys.argv[1]

print( "TM region prediction for xxxxx predicted using OCTOPUS")
print( len( sys.argv[2:] ) , len(seq) )
print( "antiparallel" )
print( "n2c" )

for s in sys.argv[2:]:
    #print(s, len(s) )
    first = seq.find(s) + 1
    second = first + len(s)
    #print( first, second, len(s))
    print( "{0:4} {1:4} {2:4} {3:4}".format(first, second, first, second))
