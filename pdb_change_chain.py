#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

# pruefe laenge der liste der argumente wenn ungleich print
if len( sys.argv ) != 3:
	print "USAGE:", sys.argv[0], "PDB CHAIN"
	exit(1)


chain = sys.argv[2]
# pruefe lenge des wortes chain
if len(chain) != 1:
	print "chain has one letter!, bye"
	exit(1)

#change side chain
with open( sys.argv[1] ) as f: 
	# gehe durch zeilen	
	for l in f:                
        	# filtern von zeilen, die mit "ATOM" anfangen
		if l[:4] == "ATOM":
			# schneide zw Pos und add
			l = l[:21] + chain + l[22:] 
	
		# print Block
		print l, 
