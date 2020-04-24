#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



from subprocess import Popen, PIPE
import os,sys,statistics
from collections import defaultdict

if len(sys.argv) < 2:
    print( "USAGE:", sys.argv[0], "DIR (optional:MODE:'full':default:'stat') (optional:OUTFILE.txt) (optional:PREFIX)")
    exit(1)

    
w = sys.stdout
mode = "stat"
prefix = ""
chain = "B"
ending = ".pdb"

for arg in sys.argv[2:]:
    if arg == "full":
        mode = arg
    elif arg == 'stat':
        mode = arg    
    elif ".txt" in arg:
        w = open( arg, 'w')
    else:
        prefix = arg
        
directory = sys.argv[1]
if  directory[-1] != '/':
    directory += '/'

    
seq_scores = defaultdict( list )

for filename in os.listdir( directory ):
    if filename.startswith( prefix ) and filename.endswith( ending ):
        process = Popen(["pdb_sequences.py", directory + filename, chain], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        output = output.split()
        header = output[0].decode('UTF-8')
        seq = output[-1].decode('UTF-8')
        #print(seq)

        process = Popen(["grep", "^pose", directory + filename], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        score = float( output.split()[-1] )
        #print(score)
        seq_scores[seq].append([header,score])


        
if mode == "stat":
    for seq,head_score in seq_scores.items():
        scores = [ x[1] for x in head_score]

        if len(scores) > 1:
            print( seq, len(head_score), "mean", "%.2f" % (sum(scores)/len(scores)), "min:", min(scores), "max:", max(scores), "stdev", "%.2f" % (statistics.stdev(scores)), file=w)
        else:
            print( seq, len(head_score), "score", scores[0], file=w)
            
elif mode == "full":
    for seq,head_score in seq_scores.items():
        w.write( seq + ':\t' )
        for x in head_score:
            w.write( x[0] + '\t' + str(x[1]) + '\t' )
        w.write( '\n' )
