#!/usr/bin/python3

import sys, os

header  = "\n\n#######################################\n"
header += "###  COPYRIGHT: RENE STARITZBICHLER  ##\n"
header += "###             02.02.2020           ##\n"
header += "#######################################\n\n\n"

tmp = "tmpxtmp.tmp"

for arg in sys.argv[1:]:
   if arg in sys.argv[0]: continue
   with open( tmp, 'w' ) as w:
      with open( arg ) as r:
         for l in r:
            w.write(l)
            if "/usr/bin/python" in l:
               w.write(header)


   os.rename( tmp, arg )
  
