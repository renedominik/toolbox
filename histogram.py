#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import matplotlib.pyplot as plt
import numpy as np, sys, os

#from matplotlib import colors
#from matplotlib.ticker import PercentFormatter

if len(sys.argv) < 5:
    print "USAGE", sys.argv[0],"FILE col/row ID NR_BINS FILTER"
    print "FILTER: e.g. '>-30.2' or '<20'  ('brackets are needed!')"
    print "you can enter multiple blocks of arguments (same order)"
    exit(1)

nr_blocks = int( (len(sys.argv) - 1) / 5)

outname = "hist"

minx = -350
maxx = 0.5
deltax = 5.0
miny = 0
maxy = 400

label_list = "kappa, dyn A", "kappa, dyn B", "mu, dyn B", "mu, dyn A"

print( nr_blocks, 'blocks')

allx = []

for iii in range( 0, nr_blocks ):
    
    x = []
    
    nr = int( sys.argv[iii*5+4] )
    
    eid = int( sys.argv[iii*5+3] )
    
    to_filter = False
    filt = ""
    val = 0
    
    if len(sys.argv) > 5:
        to_filter = True
        filt = sys.argv[iii*5+5][0]
        val = float( sys.argv[iii*5+5][1:] )
        print "filter set to",filt, val
            
    
    if sys.argv[iii*5+2] == "row":
        count = 1
        with open( sys.argv[iii*5+1] ) as f:
            for l in f:
                if l[0] != "#" and count == eid:
                    cols = l.split()
                    for c in cols:
                        #if c.isdigit():
                         #   x.append( int(c) )
                        if c.replace('.','',1).replace('-','',1).isdigit():
                            x.append( float(c) )
                count+=1
    elif sys.argv[iii*5+2] == "col":
        print "enter col"
        with open( sys.argv[iii*5+1] ) as f:
            print "opened", sys.argv[iii*5+1],"col", eid, "bins:", nr
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
    allx.append(x)
    xstr = sys.argv[iii*5+1].replace( '../','').replace( '/','_')
    xid = xstr.find( '.')
    if xid > 0:
        xstr = xstr[:xid]
    outname +=  "_" + xstr + "_" + sys.argv[iii*5+2] + sys.argv[iii*5+3]

    #n, bins, patches = plt.hist(x, nr, facecolor='g') #, alpha=0.75)
    n, bins, patches = plt.hist(x, bins=np.arange(minx,maxx +0.005,deltax), alpha = 0.5, label = label_list[iii]) #, facecolor=color_list[iii], alpha=0.5)
    

plt.legend(loc='best')
plt.xlabel('values')
plt.ylabel('counts')
plt.title('Docking scores')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.xlim((minx, maxx))
#plt.ylim((miny, maxy))
plt.yscale('log')

plt.grid(True)

print( 'filename: ' , outname + '.png' )
plt.savefig( outname + ".png" , bbox_inches='tight')
#plt.show()
plt.close()
