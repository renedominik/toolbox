#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import os,sys #, time


nr_processes = 8

nr_structs = 25

prefix = "refinement/mp1_ "


file_list = "top1k.txt" # sys.argv[1]

directory = "models/" # sys.argv[2]

files = []

relax = "rosetta_scripts.static.linuxgccrelease @relax_flags -out:prefix " + prefix + " -nstruct " + str(nr_structs)


if directory[-1] != '/':
    directory += '/'

with open( file_list) as f:
    for l in f:
        files.append( l.split()[0])

        
for i in range(0,nr_processes):
    child_pid = os.fork()
    if child_pid:
        print( 'in child', child_pid, os.getpid())
        
        for j in range( 0, len(files)):
            if j % nr_processes == i:
                
                cmd = relax + " -s " + directory + files[j] + "  >& log_" + str(i) + ".txt"
                print( cmd)
                os.system( cmd )
                    
        print( "exit")
        os._exit(os.EX_OK)
        print( 'hm... wasn''t supposed to get here')
    else:
        print( 'in parent', child_pid,os.getpid())

print( "done")
