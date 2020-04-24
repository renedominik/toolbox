#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import numpy as np

atoms = []   # array/list
zmin = 1e10
zmax = -1e10
chain = sys.argv[2]

with open( sys.argv[1]) as f:
    for l in f:
        if l[:4] != "ATOM" or l[21] != chain : continue  # continue geht zur naechsten zeile

        x = float( l[30:38] )
        y = float( l[38:46] )
        z = float( l[46:54] )

        if z <= zmin :
            zmin = z
        if z >= zmax :
            zmax = z
        atoms.append( [x,y,z] )

z_limit = zmin + .5 * ( zmax - zmin )
        
filtered = []

for a in atoms:               # loop over atoms, each atom is called 'a'
    if a[2] > z_limit:        # check z coordinate of atom a
        filtered.append( a )  # append whole atom coordinate array
    

print (len( atoms) , len( filtered))

filtered = np.array(filtered)

center = np.mean(filtered,axis=0)

distances = []

for atom in filtered:
    distance = np.linalg.norm( atom - center )
    distances.append( distance ) 
    
radius = np.mean( distances )

print ("graphics 0 sphere {",center[0],center[1],center[2],"} radius", radius, "resolution 30")
