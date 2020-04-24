#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys

#
##
### prepare rosetta input files for a subsequence  #
##
#

fasta_file = sys.argv[1]
psipred_file = sys.argv[2]
frag3_file = sys.argv[3]
frag9_file = sys.argv[4]
prefix = sys.argv[5]
sub1 = int( sys.argv[6])  # starts with 1 !!!!
sub2 = -1                 # same  
if len(sys.argv) > 7:
    sub2 = int( sys.argv[7])

# chop fasta
with open( prefix + ".fasta" , 'w' ) as w:
    seq = ''
    with open( fasta_file ) as f:
        for l in f:
            if l[0] == '>':
                w.write(l)
            else:
                seq += l.strip()
    if sub2 < 0:
        sub2 = len(seq)
    w.write( seq[sub1-1:sub2] + '\n' )   # adjust to string logic starting from 0


if sub2 < 0:
    print( "ERROR: sequence length not found")
    exit(1)
    
# chop psipred
count = 1
with open( prefix + ".psipred_ss2" , 'w' ) as w:
    with open( psipred_file) as f:
        w.write( f.readline())
        w.write( f.readline())
        for l in f:
            c = l.split()
            ID = int(c[0])
            if ID >= sub1:

                if sub2 > 0 and ID > sub2: continue

                line = f'{count:4d}' + l[4:]
                w.write(line)
                count += 1
                
#chop fragment files
for name in ( frag3_file , frag9_file ):
    count = 1
    add = str(sub1)
    if len(sys.argv)  > 7:
        add += '_' + str( sub2)
    with open( name + "_sub" + add , 'w' ) as w:
        with open( name ) as f:
            write = False
            for l in f:
                if "position" in l:
                    ID = int( l[19:22] )
                    #print( ID )
                    if ID >= sub1 and ID <= sub2:
                            write = True
                            l = l[:19] + f'{count:3d}' + l[22:]
                            count += 1
                    else:
                        write = False
                        
                if write:
                    w.write( l)
