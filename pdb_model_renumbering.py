#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

count = 0
with open(sys.argv[1]) as f:
    for l in f:
        if l[:5] == "MODEL":
            print "MODEL  ", count
            count += 1
        else:
            print l,
        
        
