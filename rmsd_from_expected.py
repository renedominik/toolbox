#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import numpy as np


if len(sys.argv) < 3:
    print "USAGE",sys.argv[0], "PDB_LIST EXPECTED_DISTANCE_FILE (optional:SCORE_TERMS)"
    print "EXPECTED_DISTANCE_FILE contains expected distances from template"
    print "passed", len(sys.argv)-1, "arguments"
    exit(1)

pdb_list = sys.argv[1]
distance_file = sys.argv[2]

score_terms = sys.argv[3:]

distances = {} # constraints, expected values

first_chain = "A"
second_chain = "B"

first_chain_ids = []
second_chain_ids = []

with open( distance_file) as f:
    for l in f:
        c = l.split()
        distances[ c[1]+':'+c[4] ] = float( c[2] )  # links residue ids with expected distances
        first_chain_ids.append( c[1] )
        second_chain_ids.append( c[4] )

        


# read list
with open( pdb_list ) as fx:
    for lx in fx:
        first_chain_position = {}
        second_chain_position = {}
        scores = []
        lx = lx.strip()
        li = lx.split()
        # read individual pdb
        with open( li[0] ) as f:
            for l in f:
        
                c = l.split()
                if l[:4] == "ATOM" and l[12:16].replace(' ', '') == "CA":
                    resid = l[22:26].replace(' ','') 
                    chain = l[21]

                    x = float( l[30:38] )
                    y = float( l[38:46] )
                    z = float( l[46:54] )
                    pos = np.array([x,y,z])

                    if chain == first_chain and resid in first_chain_ids:
                        first_chain_position[ resid ] = pos
                    elif chain == second_chain and resid in second_chain_ids:
                        second_chain_position[ resid ] = pos
                elif len(c) > 0 and c[0] in score_terms:
                    scores.append([ score_terms[ score_terms.index(c[0]) ] ,  c[1]] )
                
        average = 0.0
        for idstring , expected_distance in distances.iteritems():
            ids = idstring.split(':')
            pos1 = first_chain_position[ ids[0] ]
            pos2 = second_chain_position[ ids[1] ]
            dist = np.linalg.norm( pos1 - pos2 )
            average += ( dist - expected_distance ) ** 2

        print lx + '\t' + 'rmsd ' + str( np.sqrt( average / len(distances) ) ) + '\t',

        for s in scores:
            print s[0] + '\t' + s[1] + '\t' , 


        print
