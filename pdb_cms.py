#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import pdb_atoms as pdb

if len( sys.argv) < 2:
    print( "USAGE:",sys.argv[0]," X.pdb optional:CHAIN_1 (...)" )
    print( "calc CMS, using CA atoms only" )
    print( "bye" )
    exit(1)

pdb_file = sys.argv[1]
chains = []
if len(sys.argv) > 2:
    chains = sys.argv[2:]
   
print( "CMS: ", pdb.CMS( pdb_file, chains) )

mini,maxi = pdb.MinMax( pdb_file, chains) 

print( "min:", mini )
print( "max:", maxi )
