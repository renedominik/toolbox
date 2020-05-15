#!/usr/bin/python3

##################################
##
## copyright: Rene Staritzbichler
##
## absolutely no warranties
##################################

import sys

filename = sys.argv[1]
outname = sys.argv[2]

with open( outname , 'w') as w:
    with open( filename) as r:
        for l in r:
          if "tc_grps" in l:
              w.write( "tc_grps             = PROTMEMBLIG SOL       ; Couple lipids and SOL seperatly\n" )
          elif "tau_t" in l:
              w.write( "tau_t               = 0.5 0.5            ; Time constant for temperature coupling\n")
          elif "ref_t" in l:
              w.write ( "ref_t               = 310 310            ; Desired temperature (K)\n" )
          else:
              w.write( l )
