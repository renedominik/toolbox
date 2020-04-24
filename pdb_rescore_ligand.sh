#!/bin/bash

#se PATH_TO_ROSETTA/home/hildilab/dev/ext/rosetta/2018.09/main
PATH_TO_ROSETTA=/home/hildilab/dev/ext/rosetta/2018.09/main
PATH_TO_DB=$PATH_TO_ROSETTA/database
PATH_TO_EXE=$PATH_TO_ROSETTA/source/bin/
CMD="$PATH_TO_EXE/score_jd2.static.linuxgccrelease -out:prefix ligands/  "


for f in `cat models_lt-200.txt`
do
    echo $f
    grep ^ATOM $f | grep " B "  > ligands/${f:7}
    $CMD -s ligands/${f:7} 
done


grep ^SCORE ligands/score.sc | grep -v total  | awk '{sum+=$2}END{print "mean ligand score of " NR " ligands: " sum/NR}'
