#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

if len(sys.argv) < 2:
    print "USAGE", sys.argv[0], "SCORE_FILE SCORE_NAME"
    exit(1)

score_file = sys.argv[1]
score_name = sys.argv[2]


with open( score_file ) as f:
    f.readline()
    c = f.readline().split()
    index = c.index(score_name)
    forsort = index+1
    print (score_name,'column_nr', index)
    print (score_name, 'column_nr_for_sort', forsort)

