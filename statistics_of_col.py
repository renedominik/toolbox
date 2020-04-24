#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import numpy as np, sys

col = int(sys.argv[2])

v = []

with open(sys.argv[1]) as f:
    for l in f:
        if l[0] == '#' or l[0] == '@': continue
        c = l.split()
        v.append(float(c[col]))

a = np.array(v)
print np.mean(a), np.std(a)
