#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    print( "USAGE", sys.argv[0], "FILE1 COL0 COL1 (opt: FILE2 COL0 COL1...)")
    print( "COL0 set to '-1' will use range")
    exit(1)

for r in range( 0, int(len(sys.argv)/3) ):
    
    cols = [ int(x) for x in sys.argv[2+r*3:4+r*3] ]
    print( "ids:", cols)
    data = [[] for i in range(0, len(cols))]

    with open( sys.argv[1+r*3] ) as f:
        for l in f:
            c = l.split()
            if len(c) <= cols[-1]: continue
            for i in range(0,len(cols)):
                #  print( i, cols[i], c[cols[i]] )
                data[i].append( float(c[cols[i]]) )

    if cols[0] == -1:
        data[0] = range(0,len(data[1]))
    plt.plot( data[0], data[1] )

    
axes = plt.gca()

plt.grid()

#plt.legend()

# set to 'False' if you don't want to create .png
if True:
    fname = sys.argv[1][:-4] + '.png'
    print("safe as: " + fname)
    plt.savefig(fname)

# comment this out when you don't want extra window with plots to pop up (e.g. when iterating through many groups)
#plt.show()
