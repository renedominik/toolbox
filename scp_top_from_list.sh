#!/bin/bash

echo ""
echo "highly specific script, CHECK SETTINGS !!!"
echo ""

for f in `sort -nk4 top5000_total_Isc_rew.txt | head -n 50`
do
    if [[ $f == *".pdb" ]]
    then
	scp $f hildilab@proteinformatics.uni-leipzig.de:/disk/data/mdsrv/peptide_gpcr/2_flexpepdock/mu/dynB/top_models/.
    fi
done
    
