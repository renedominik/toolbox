#!/bin/bash

SCOREFILE="rescored_flexpepdock_2.sc"
DIR="refinement_2/"

for d in "/home/hildilab/projects/peptide_gpcr/4_design/mu/6dde/grow_from_root/seq2/"   "/home/hildilab/projects/peptide_gpcr/4_design/kappa/6b73_open/grow_from_root/seq2" 
do
    cd $d
    pwd

    for f in $DIR*.pdb; do
	if ! grep -q ${f:0:-4} $SCOREFILE ; then
	    echo $f
	    FlexPepDocking.static.linuxgccrelease -in:file:s $f -flexPepDocking:flexpep_score_only -out:file:score_only  $SCOREFILE > /dev/null
	fi
    done &
    cd $OLDPWD
    pwd
done
 
