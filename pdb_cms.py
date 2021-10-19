#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import pdb_atoms as pdb

if len( sys.argv) < 2:
    print( "USAGE:",sys.argv[0]," X.pdb optional:CHAIN_1 (...)" )
    print( "calc CMS and min max limits, once for CA only, once for all atoms (incl HETATM)" )
    print( "bye" )
    exit(1)

pdb_file = sys.argv[1]
chains = []
if len(sys.argv) > 2:
    chains = sys.argv[2:]
   
print( "CMS CA: ", pdb.CMS( pdb_file, chains, ["CA"]) )
print( "CMS all: ", pdb.CMS( pdb_file, chains) )

mini,maxi = pdb.MinMax( pdb_file, chains, ["CA"]) 

print( "min CA: %.2f  %.2f  %.2f" % (mini[0],mini[1],mini[2]) )
print( "max CA: %.2f  %.2f  %.2f" % (maxi[0],maxi[1],maxi[2]) )

mini,maxi = pdb.MinMax( pdb_file, chains) 

print( "min all: %.2f  %.2f  %.2f" % (mini[0],mini[1],mini[2]) )
print( "max all: %.2f  %.2f  %.2f" % (maxi[0],maxi[1],maxi[2]) )
