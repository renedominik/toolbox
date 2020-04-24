#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

# pruefe laenge der liste der argumente wenn ungleich print
if len( sys.argv ) < 4:
	print "USAGE:", sys.argv[0], "PDB ORIGINAL_CHAIN_1 ALTER_TO_CHAIN_1 (...) "
	exit(1)


chains = {}
for i in range( 0, len(sys.argv[2:])/2):
    chains[ sys.argv[2*i+2] ] = sys.argv[2*i+3]

#print( chains)

        
#change side chain
with open( sys.argv[1] ) as f: 
    # gehe durch zeilen	
    for l in f:                
        # filtern von zeilen, die mit "ATOM" anfangen
        if l[:4] != "ATOM":
                print l,
                continue
        c = l[21]
        if c not in chains:
                print l,
        # schneide zw Pos und add
        else:
                l = l[:21] + chains[c] + l[22:] 
	    
	        # print Block
	        print l, 
