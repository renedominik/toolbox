#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import pdb_atoms as pdb

import sys

chains = []

if len(sys.argv) > 3:
    chains = sys.argv[3:]

pos = pdb.MatchingPositions( sys.argv[1], sys.argv[2], chains)

#print pos

print pdb.MatchingPositionsRMSD( sys.argv[1], sys.argv[2], pos )
