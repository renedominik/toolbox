#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm, LogNorm

name = sys.argv[1]
typ = sys.argv[2] # col / row

first = int( sys.argv[3] )
last = int( sys.argv[4] )
draw = True
header = True

if len( sys.argv) < 5:
    print "USAGE:", sys.argv[0], " FILE row/col FIRST LAST (opt:header:false)"
    print "NOTE: FIRST/LAST start from 1"
elif len( sys.argv) > 5:
    print "set header to false"
    header = False
    first -= 1
    last -= 1

x = []
y = []
data = []
    
if typ == "col":
    count = 0
    with open( name ) as f:
        for l in f:
            c = l.split()
            if header == True:
                #print c[0],
                if draw:
                    if count == 0:
                        x = []
                        for j in range(first,last+1):
                            string = ""
                            if j % 5 == 0:
                                string += str(j) + ":   "
                            string += c[j]
                            x.append( string )
                        #print x
                        count += 1
                        continue
                    else:
                        y.append( c[0])
            d = []
            for i in range( first, last+1):
                #print c[i],
                d.append( float( c[i] ) )
        
            #print
            #print len(d)
            data.append( d)
            count += 1
    

elif typ == "row":
    with open( sys.argv[1] ) as f:
        count = 0
        for l in f:
            if ( header == True and count == 0 )  or ( count >= first and count <= last ):
                print l,
            count += 1

if draw:            
    cmap = plt.cm.get_cmap("hot") # "seismic")
    #fig, ax = plt.subplots()
    plt.figure()
    plt.pcolormesh( data, cmap=cmap) #, interpolation='nearest')
    #plt.imshow( contact_map, cmap="seismic", interpolation='nearest')
    #ax.set_xticklabels(x)
    x_offset = [ 0.5 + i for i in range(0, len(x))]
    y_offset = [ 0.5 + i for i in range(0, len(y))]
    plt.xticks( x_offset,x, rotation='vertical',fontsize=8)
    plt.yticks( y_offset,y)
    #plt.subplots_adjust(wspace=0.5)
    plt.show()
    #plt.savefig(  "sub_" + str(first) + "_" + str(last) + ".png")
    #plt.savefig(  name[:-4] + "_" + typ + "_" + str(first) + "_" + str(last) + ".pdf")
