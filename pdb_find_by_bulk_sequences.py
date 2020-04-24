#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



from subprocess import Popen, PIPE
import os,sys


if len(sys.argv) < 4:
    print( "USAGE", sys.argv[0], "DIR FILE OUTDIR (opt:CHAIN)")
    exit(1)

sequences = []

with open( sys.argv[2]) as f:
    for l in f:
        sequences.append( l.split()[0] )
    
directory = sys.argv[1]
outdir = sys.argv[3]
chain = ""
if len(sys.argv) > 4:
    chain =  sys.argv[4]
    
    
if directory[-1] != '/':
    directory += '/'
if outdir[-1] != '/':
    outdir += '/'

    
for filename in os.listdir( directory ):
    if  filename.endswith(".pdb"):
        process = Popen(["pdb_sequences.py", directory + filename, chain], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        output = output.split()
        for o in output:
            seq = o.decode('UTF-8')
            if seq in sequences:
                process = Popen(["grep", "^pose", directory + filename], stdout=PIPE)
                (result, err) = process.communicate()
                exit_code = process.wait()
                score = result.split()[-1].decode('UTF-8') 

                with open( outdir + seq + ".txt", 'a') as f: 
                    f.write( filename + ' ' + score + '\n' )

                break
