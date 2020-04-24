#!/usr/bin/python3

import sys

atnr = 1
resnr = -99
prev_chain = '9'
prev_res_id = -999
prev_res_name = 'XYZ'
newchain = False

with open( sys.argv[1] ) as f:
    for l in f:
        if l[:4] == "ATOM" or l[:6] == "HETATM":
            s = '{:5d}'.format( atnr)
            l = l[:6] + s + l[11:]
            atnr+=1

            rname = l[17:20]
            chain = l[21]
            rid = int( l[22:26] )

            if chain != prev_chain:
                prev_chain = chain
                resnr = 0
                
            if prev_res_name != rname or prev_res_id != rid:
                resnr += 1
                prev_res_name = rname
                prev_res_id = rid

            l = l[:22] + '{:4d}'.format(resnr) + l[26:]
            
        print( l, end='')
