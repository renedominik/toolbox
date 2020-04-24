#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

#import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

offset = 2
step = 2

name = sys.argv[1]
prefix = sys.argv[2]
nr = int(sys.argv[3])

x = []
with open( name ) as f:
    for l in f:
        if prefix not in l: continue
        #print(l)
        c = l.split()
        x = [float(v) for v in c[offset::step]]
        break
#print(x)
n,bins,patches = plt.hist(x,nr)
plt.show()
