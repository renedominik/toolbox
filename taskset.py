#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import sys, os
from subprocess import check_output

def get_pid(name):
    return  [int(x) for x in check_output(["pidof",name]).split() ]

#################    SETTINGS  ##############################

nr_processes = 36

first_processor = 27

exe = "rosetta_scripts.static.linuxgccrelease"

#################    SETTINGS  END  #########################

if len(sys.argv) > 1:
    exe = sys.argv[1]

pids = get_pid( exe ) 

for i in range( 0 ,  min(nr_processes,len(pids)) ):
    print(i)
    os.system( "taskset -pc " + str(i+nr_processes) + " " + str(pids[i]) )

exit(1)
if len(pids) > nr_processes:
    for i in range( nr_processes , len(pids) ):
        print("erase:",i, pids[i])
        os.system("kill " + str(pids[i]))
