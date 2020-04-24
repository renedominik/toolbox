#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
from operator import itemgetter

if len(sys.argv) < 3:
    print "USAGE", sys.argv[0], " ANALYSIS_FILE  COL "

def Write( m ):
    for i in range(0,len(m)-1):
        print m[i] + '\t',
    print m[-1] 
    
col = int( sys.argv[2] )

ids = []

data = [] 
with open( sys.argv[1]) as f:
    for l in f:
        data.append( l.split() )

data.sort( key = itemgetter( col ), reverse = True)

for l in data:
    if len(l) < 2:
        continue
        
#    c = l.split()
    this_id = l[0].split('.')[-3]
    
    if this_id not in ids:
        Write( l )
        ids.append( this_id )

            
