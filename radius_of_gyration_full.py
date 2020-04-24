#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import numpy as np
import sys

if len(sys.argv) < 2:
    print( "USAGE",sys.argv[0],"PDB optional:CHAINS")
    print( "only ATOM section is considered for calculation of radius of gyration")
    exit(1)

chains = []

if len(sys.argv) > 2:
    chains = sys.argv[2:] 


    
positions = []
    
with open(sys.argv[1]) as r:
    for l in r:
        if l[:4] == "ATOM" and ( len( chains) == 0 or l[21] in chains ):
            positions.append( np.array( [ float(l[30:38]) , float(l[38:46]) , float(l[46:54]) ] ) )

cms = np.array( [ 0.0 , 0.0 , 0.0 ] )

for pos in positions:
    cms += pos


cms /= len(positions)

distances = []

for pos in positions:
    distances.append( ( ( pos - cms )**2 ).sum() )


radius = np.sqrt( np.mean( np.array( distances) ) ) 

#print( radius )
print( "radius-of-gyration:", radius )


print( "cms:", cms )

print( "graphics 0 sphere {" + str(cms[0]) + " " + str(cms[1]) + " " + str(cms[2]) + "} radius " + str( radius ) + " resolution 30" )
