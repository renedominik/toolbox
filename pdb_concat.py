#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

count = 1
with open( sys.argv[-1] , 'w' ) as w:
    for a in sys.argv[1:-1]:
        w.write( "MODEL\t\t" + str(count) + '\n' )
        with open( a ) as r:
            for l in r:
                if l[:3] != "END":
                    w.write(l)
#        w.write( "TER\n" )
        w.write( "ENDMDL\n" )
        count += 1
        
