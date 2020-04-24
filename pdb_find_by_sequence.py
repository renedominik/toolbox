#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



from subprocess import Popen, PIPE
import os,sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if len(sys.argv) < 3:
    print( "USAGE", sys.argv[0], "DIR SEQ (opt:CHAIN) (opt:LOWER UPPER-SCORE)")
    exit(1)
    
    
directory = sys.argv[1]
sequence = sys.argv[2]
chain = ""
lower = -1e8
upper = 1e8

is_first = True
for arg in sys.argv[3:]:
    if is_number( arg ):
        if is_first:
            lower = float( arg )
            is_first = False
        else:
            upper = float( arg )
    else:
        chain = arg

    
if directory[-1] != '/':
    directory += '/'
for filename in os.listdir( directory ):
    #if filename.endswith(".pdb"):
    if  filename.endswith(".pdb"):
        process = Popen(["pdb_sequences.py", directory + filename, chain], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        #print(output)
        output = output.split()
        for o in output:
            seq = o.decode('UTF-8')
            if sequence in seq:
                process = Popen(["grep", "^pose", directory + filename], stdout=PIPE)
                (result, err) = process.communicate()
                exit_code = process.wait()
                score = float( result.split()[-1] )
                if score >= lower and score <= upper:
                    print( filename )
                    print( seq )
                    print( score , '\n' )
                
