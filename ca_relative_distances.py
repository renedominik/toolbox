#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import numpy as np

# this script is supposed to write both rosetta score as well as the degree of insertion into the binding pockt for each docking pose (PDB)


#####  SETTINGS, to be adjusted for each receptor / PDB ###########
center = np.array( [2.78 , -24.17 , 58.39] )
radius = 14.83
positions = []

#positions.append( [ 6.697 , -21.841 , 58.433 ] )  # CB of Asp 84 in 4djh renumbered
#positions.append( [ 7.691 , -17.035 , 57.181 ] )  # CB of Tyr 85
#positions.append( [ 3.072 , -18.114 , 54.412 ] )  # CB of Met 88
#positions.append( [-4.293 , -21.392 , 58.074 ] )  # CB of ILE 235
#positions.append( [-2.146 , -27.157 , 60.174 ] )  # CB of ILE 261

positions.append( [   6.928 , -21.782 ,  56.921 ] )  # CA of Asp 84 in 4djh renumbered
positions.append( [   6.957 , -18.042 ,  56.301 ] )  # CA of Tyr 85
positions.append( [   3.238 , -18.493 ,  52.944 ] )  # CA of Met 88
positions.append( [  -5.555 , -20.774 ,  58.694 ] )  # CA of ILE 235
positions.append( [  -3.004 , -26.666 ,  58.977 ] )  # CA of ILE 261


###################################################################


if len(sys.argv) < 5:
    print "USAGE",sys.argv[0], "ROSETTA_SCORE_FILE  PDB_LIST  CHAIN  OUT_FILE\n"
    exit(1)

score_file = sys.argv[1]
pdb_list = sys.argv[2]
chain = sys.argv[3]
out_file = sys.argv[4]

score = {}  # dictionary


# fill score dictionary from score.sc file
with open(score_file) as f:
    for l in f:
        cols = l.split()  # array mit allen strings

        if cols[0] != "SCORE:" or cols[1] == "total_score" : continue

        score[ cols[-1] ] = float( cols[1] )
        # score["model_001.pdb"] = -237.146

print "scores collected"
w = open( out_file, 'w')


# go through list of pdbs
with open( pdb_list ) as f:
    for l in f:

        key =  os.path.splitext( l.strip() )[0]
        if key not in score: continue

        count = 0
        zmin = 1e10
        min_dists = [1e10] * len(positions)
        
        with open( l.strip() ) as fx:
            for lx in fx:
                # select CA atoms from chain
                if lx[:4] != "ATOM" or lx[21] != chain or lx[17:20] != "TYR" or lx[12:16].replace( ' ','') != "CA" : continue  # filter CA atoms in chain
                x = float( lx[30:38] )
                y = float( lx[38:46] )
                z = float( lx[46:54] )

                if z < zmin:
                    zmin = z
                    
                pos = np.array( [x,y,z] )
                # check whether they are inside binding pocket
                dist= np.linalg.norm( pos - center)
                if dist <= radius:
                    count += 1

                for i in range( 0, len(positions)):
                    dist = np.linalg.norm( pos - positions[i] )
                    if dist < min_dists[i]:
                        min_dists[i] = dist

        w.write( key + '\t' + str( count ) + '\t' + str( score[key] ) + '\t' + str(zmin) + '\t' )
        for m in min_dists:
            w.write( str(m) + '\t' )
        w.write( str(np.mean(min_dists)) + '\n' )

w.close()

                



 
