#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import matplotlib.pyplot as plt
import numpy as np, sys

#from matplotlib import colors
#from matplotlib.ticker import PercentFormatter

if len(sys.argv) < 5:
    print "USAGE", sys.argv[0],"FILE col/row ID NR_BINS FILTER"
    print "FILTER: e.g. '>-30.2' or '<20'  ('brackets are needed!')"
    exit(1)

x = []

nr = int( sys.argv[4] )

eid = int( sys.argv[3] )

to_filter = False
filt = ""
val = 0

if len(sys.argv) > 5:
    to_filter = True
    filt = sys.argv[5][0]
    val = float( sys.argv[5][1:] )
    print "filter set to",filt, val
        

if sys.argv[2] == "row":
    count = 1
    with open( sys.argv[1] ) as f:
        for l in f:
            if l[0] != "#" and count == eid:
                cols = l.split()
                for c in cols:
                    #if c.isdigit():
                     #   x.append( int(c) )
                    if c.replace('.','',1).replace('-','',1).isdigit():
                        x.append( float(c) )
            count+=1
elif sys.argv[2] == "col":
    print "enter col"
    with open( sys.argv[1] ) as f:
        print "opened", sys.argv[1],"col", eid, "bins:", nr
        for l in f:
            if l[0] == "#": continue
            cols = l.split()
            if len(cols) < eid + 1:
                print "WARNING: nr cols: ", len(cols), "id:", eid
                continue
            c = l.split()[eid]
            #if c.isdigit():
             #   x.append( int(c) )
            if c.replace('.','',1).replace('-','',1).isdigit():
                if not to_filter:
                    x.append( float(c) )
                else:
                    v = float(c)
                    if (filt == ">" and v > val) or (filt=="<" and v < val):
                        x.append(v)
                    
#print x
print "min:", min(x), "max:", max(x), "nr datapoints:",len(x)

# the histogram of the data
n, bins, patches = plt.hist(x, nr, facecolor='g') #, alpha=0.75)


plt.xlabel('values')
plt.ylabel('counts')
plt.title('Histogram')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)

plt.savefig( sys.argv[1][:-4] + "_" + sys.argv[2] + sys.argv[3] + ".png" , bbox_inches='tight')
#plt.show()
plt.close()
