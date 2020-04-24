#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

import pdb_functions as pdb


def SetResidueType( line, typ ):
    typ = typ.strip()
    if len(typ) != 3:
        print "ERROR: residue type has to be given in three letter code:", typ
        exit(1)
    return line[:17] + typ + line[20:]


length = len(sys.argv[2:])
if length < 3 or length % 3 != 0:
    print "USAGE", sys.argv[1], "FILE.pdb CHAIN1 RESID1 RESTYPE1 ..."
    exit(1)
    
replace = []
for i in range( 0, length/3):
    replace.append( sys.argv[3*i+2 : 3*i+5] )

#print replace

atoms = [ "C", "N", "O", "CA" ]

with open( sys.argv[1]) as f:
    for l in f:
        l = l.strip()
        if "ATOM" != l[:4]:
            print l
            continue
        found = False
        for r in replace:            
            if pdb.chain(l) == r[0] and pdb.residue_id(l) == int(r[1]):
                found = True
                break
        if found:
            if pdb.atom_name(l) in atoms:
                print SetResidueType( l, r[2] )
        else:
            print l
