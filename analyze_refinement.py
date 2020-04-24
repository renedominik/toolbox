#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



from collections import defaultdict
import numpy as np

directories = [
         #"/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq1/" ,
         #"/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq1/" ,
         #"/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq2/" ,
         #"/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq2/",
         "/home/hildilab/projects/peptide_gpcr/4_design/mu/6dde/grow_from_root/seq1/" ,
         "/home/hildilab/projects/peptide_gpcr/4_design/kappa/6b73_open/grow_from_root/seq1/"
]


types = ["I_sc" , "reweighted_sc" ]
ids = []  #  I_sc, reweighted_sc

full = defaultdict( list )

w = open( "seq1_scores.txt", 'w')


for d in directories:
         
         pdb2seq = {}
         rescored_I = defaultdict( list )
         rescored_rew = defaultdict( list )

         print(d)
         
         with open( d + "seq_pdb_score.txt" ) as f:
	          for l in f:
                           c = l.split()
                           seq = c[0][:-1]
                           scores = [ float(x) for x in c[2::2] ]
                           if "mu" in d:
                                    line = "MU:    " 
                           elif "kappa" in d:
                                    line = "KAPPA: " 
                           line += seq + '  refn\t'
                           line += "min: %8.2f\t" % min(scores) 
                           line += "mean: %8.2f\t" % np.mean(scores) 
                           line += "max: %8.2f\t" % max(scores) 
                           line += "std: %8.2f\t" % np.std(scores) 
                           line += "nr: %8i\n" % len(scores) 
                           full[seq].append(line)

                           for i in range( 0 , int( (len(c)-1) / 2 ) ):
                                    #print(  c[2*i+1][1:-2] , seq)
                                    pdb2seq[ c[2*i+1][1:-2] ] = seq
         
         with open( d + "rescored_flexpepdock.sc" ) as f:
                  print( d + "rescored_flexpepdock.sc opened" )
                  for l in f:
                           if "SCORE:" not in l:continue
                           
                           c = l.split()
                           if "total" in l:
                                    for t in types:
                                             ids.append( c.index( t) )
                           else:
                                    pdb = c[-1][:-5]
                                    if pdb not in pdb2seq.keys(): continue
                                    seq = pdb2seq[pdb]  # ignore flexpep rescore id [:-5]
                                    rescored_I[ seq ].append( float(c[ids[0]]) )
                                    rescored_rew[ seq ].append( float(c[ids[1]]) )



         for k in rescored_I.keys():
                  print(k)
                  if "mu" in d:
                           line = "MU:    " 
                  elif "kappa" in d:
                           line = "KAPPA: " 
                  scores = rescored_I[k]
                  line += k + '  I_sc\t'
                  line += "min: %8.2f\t" % min(scores) 
                  line += "mean: %8.2f\t" % np.mean(scores) 
                  line += "max: %8.2f\t" % max(scores) 
                  line += "std: %8.2f\t" % np.std(scores) 
                  line += "nr: %8i\n" % len(scores) 
                  full[k].append(line)
                  
                  if "mu" in d:
                           line = "MU:    " 
                  elif "kappa" in d:
                           line = "KAPPA: " 
                  scores = rescored_rew[k]
                  line += k + '  rewg\t'
                  line += "min: %8.2f\t" % min(scores) 
                  line += "mean: %8.2f\t" % np.mean(scores) 
                  line += "max: %8.2f\t" % max(scores) 
                  line += "std: %8.2f\t" % np.std(scores) 
                  line += "nr: %8i\n" % len(scores) 
                  full[k].append(line)
for k,v in full.iteritems():
         w.write( k + '\n')
         for s in v:
                  w.write( s )
         w.write( '\n')
                  
w.close()

