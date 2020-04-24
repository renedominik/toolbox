#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys
import pdb_functions as pdb

if len( sys.argv) < 3:
    print "USAGE:",sys.argv[0]," FIRST.txt  SECOND.txt"
    print "finds for each pdb in FIRST the closest pdb in SECOND"
    print "bye"
    exit(1)

dir_1 = ""
dir_2 = ""

id_1 = sys.argv[1].rfind('/')

if id_1 >= 0:
    dir_1 = sys.argv[1][:id_1+1]

id_2 = sys.argv[2].rfind( '/')
if id_2 >= 0:
    dir_2 = sys.argv[2][:id_2+1]
#print "dirs", dir_1, dir_2
                        
with open( sys.argv[1] ) as f:
    pdbs_1 = f.readlines()
print "read", len(pdbs_1)
    
with open( sys.argv[2] ) as f:
    pdbs_2 = f.readlines()
print "read", len(pdbs_2)

hits = []

for l1 in pdbs_1:
    rmsd = 100
    best = ""
    p1 = dir_1 + l1.split()[0]
    for l2 in pdbs_2:
        p2 = dir_2 + l2.split()[0]
        r = pdb.RMSD( p1, p2 )
        #print p1,p2,r
        if r < rmsd:
            rmsd = r
            best = l2.strip()
    hits.append( best.split()[0])
    print "CLUSTER:", p1
    print '\tRMSD: ', rmsd,  best
    sys.stdout.flush()
count = 0
print "Unassigned (new) clusters from second set:"
for l2 in pdbs_2:
    p2 = l2.split()[0]
    if p2 not in hits:
        print l2
        count += 1
print "# nr of unassigned", count 
