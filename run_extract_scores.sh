#!/bin/bash

SUBDIR="refinement"
OUTFILE="seq_pdb_score.txt"
MODE="full"

#SUBDIR="designs_refined"
#OUTFILE="designs_refined_seq_scores_full.txt"
#MODE="stat"

#SUBDIR="designs"
#OUTFILE="designs_seq_scores_full.txt"
#MODE="full"

for d in "/home/hildilab/projects/peptide_gpcr/4_design/mu/6dde/grow_from_root/seq2/"   "/home/hildilab/projects/peptide_gpcr/4_design/kappa/6b73_open/grow_from_root/seq2" "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq2" "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/mu/6dde/grow_from_root/seq1" "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq1/"  "/home/hildilab/projects/peptide_gpcr/2_flexpepdock/kappa/6b73_open/grow_from_root/seq2/" 
do
    cd $d
    pwd

    if [ -d "$SUBDIR" ]
    then
	pdb_extract_seq_rosetta_score.py $SUBDIR $MODE $OUTFILE
    fi
    
    cd $OLDPWD
    pwd
done
 
