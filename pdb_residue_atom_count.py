#!/usr/bin/python3

import sys
import pdb_functions as pf

resname = ""
if len( sys.argv) > 2:
    resname = sys.argv[2]
count = 0
prev_resid = -999
first_line = ""
with open( sys.argv[1]) as r:
    for l in r:
        if l[:4] == "ATOM" or l[:6] == "HETATM":
            name = pf.residue_name(l)
            if len(resname) > 0 and name != resname:
                continue
            
            resid = pf.resid( l)

            if resid != prev_resid:
                if prev_resid >= 0:
                    print( first_line[:30], "COUNT: ", count)
                count = 0
                prev_resid = resid
            if count == 0:
                first_line = l
            count += 1
print( first_line[:30], "COUNT: ", count)
