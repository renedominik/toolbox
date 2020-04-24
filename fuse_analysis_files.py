#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys



if len(sys.argv) < 5:
    print "USAGE:", sys.argv[0], " FILE_A  FILE_B  B_COL_ID_STRING  B_COL_VALUE  PREFIX_VALUE "
    print "e.g.:", sys.argv[0]," cluster_reweighted_sc-290_ca_rmsd.txt angle_act-inactive.txt 1 9 angle"
    exit(1)


col_str = int( sys.argv[3] )
col_val = int( sys.argv[4] )
name = sys.argv[5]

#print sys.argv

first_file = {}

with open( sys.argv[1]) as f:
    for l in f:
        c = l.split()
        id_string = c[0].strip('.').strip('/').strip('.pdb')
        first_file[id_string] = l.strip()
#print len( first_file)



with open( sys.argv[2]) as f:
    for l in f:
        c = l.split()
        
        id_string = c[col_str].strip(',').strip("'").strip('.').strip('/').strip('.pdb')
        if id_string.count('.') == 2: id_string += '.'
         
        value = c[col_val]
        #print id_string, value

        for key,line in first_file.items():
            if id_string in key:
                print line, name, value
        
 
