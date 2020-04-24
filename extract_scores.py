#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print "USAGE", sys.argv[0], "SCORE_FILE SCORE_NAME"
    exit(1)

score_file = sys.argv[1]
score_name = sys.argv[2]

score_id = -1

scores = []

with open( score_file ) as f:
    l = f.readline()
    l = f.readline()

    cols = l.split() # chop at space, line into array 

    # iterate through all scores
    for i in range( 0, len(cols)):
        # find the matching score
        if score_name in cols[i]:
            print "found:", cols[i]
            score_id = i

    for line in f:
        
        if "SCORE:" not in line: continue #security check

        cols = line.split()

        score = float( cols[score_id] )

        scores.append( score )
        
# create histogram
n, bins, patches = plt.hist( scores, 20 )

plt.show()
