#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import numpy as np

# this script switches score_type_1 with score_type_2

type_1 = "reweighted_sc"
type_2 = "pose"


if len(sys.argv) < 3:
    print "USAGE",sys.argv[0], " PDB_LIST  OUTDIR"
    exit(1)
    
pdb_list = sys.argv[1]
out_dir = sys.argv[2]

if out_dir[-1] != '/':
    out_dir += '/'

with open( pdb_list ) as f:
    for thisfile in f:

        thisfile = thisfile.strip()
        
        with open( thisfile) as pdb:
            # read entire pdb file into list:
            data = pdb.readlines()

        for i in range( 0, len(data) ):
            if type_1 in data[i]:
                id1 = i
                c = data[i].split()
                value1 = c[-1]
            if type_2 in data[i]:
                c = data[i].split()
                id2 = i
                value2 = c[-1]

        c = thisfile.split('/')
        length = len(c[0])
        name =  out_dir + thisfile[length:]
        print name
        w = open( name , 'w' )

        cols = data[id1].split()
        
        string = ""
        for i in range(0, len(cols)-1):
            string += cols[i] + '\t'
        string += value2 + '\n'
        data[id1] = string

        cols = data[id2].split()
        
        string = ""
        for i in range(0, len(cols)-1):
            string += cols[i] + '\t'
        string += value1 + '\n'
	data[id2] = string

        for d in data:
            w.write( d )
            
        w.close()

                



 
