#!/bin/bash

#se PATH_TO_ROSETTA/home/hildilab/dev/ext/rosetta/2018.09/main
PATH_TO_ROSETTA=/home/hildilab/dev/ext/rosetta/2018.09/main
PATH_TO_DB=$PATH_TO_ROSETTA/database
PATH_TO_EXE=$PATH_TO_ROSETTA/source/bin/
CMD="$PATH_TO_EXE/score_jd2.static.linuxgccrelease -out:prefix ligands_top100/  "


for f in `cat models_top100.txt`
do
    echo $f
    grep ^ATOM $f | grep " B "  > ligands_top100/${f:7}
    $CMD -s ligands_top100/${f:7} 
done


grep ^SCORE ligands_top100/score.sc | grep -v total  | awk '{sum+=$2}END{print "mean ligand score of " NR " ligands: " sum/NR}'
