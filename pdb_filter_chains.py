#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import sys


# pruefe laenge der liste der argumente wenn ungleich print
if len( sys.argv ) < 3:
	print "USAGE:", sys.argv[0], "PDB CHAIN1 .."
	exit(1)


chains = sys.argv[2:]

#change side chain
with open( sys.argv[1] ) as f: 
	# gehe durch zeilen	
	for l in f:                
        	# filtern von zeilen, die mit "ATOM" anfangen
		if l[:4] == "ATOM" and l[21] in chains:
		        print l, 
