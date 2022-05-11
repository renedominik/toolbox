#!/bin/bash

#### GLADNESS
if [ $HOSTNAME == 'gladness' ]
then
    rsync -auP /home/hildilab/projects/peptide_gpcr /media/hildilab/Elements/projects
    
    find  /home/hildilab/data/ext/pdb \( -name \*.py -o -name \*.sh -o -name README\* \) -exec rsync -auP {} /media/hildilab/Elements/data/ext/pdb/ \;
fi
##### HAPPINESS
if [ $HOSTNAME == 'happiness' ]
then
    target='/media/hildilab/Elements/'
    echo "backup to $target"
    echo "backup server home"
    su -c 'rsync -auPW hildilab@proteinformatics.uni-leipzig.de:* /home/hildilab/projects/server/proteinformatics/home/ --log-file log.txt' hildilab
    echo
    echo "backup server www"
    su -c 'rsync -auPW hildilab@proteinformatics.uni-leipzig.de:/var/www :/etc/apache2 /home/hildilab/projects/server/proteinformatics/ --log-file log.txt' hildilab
    echo
    echo "backup home hildilab happiness"
    rsync -auPW  --exclude=blast --exclude=snap /home/hildilab $target --log-file log.txt
    echo
    echo "backup project peptide_gpcr to gladness"
    su -c 'rsync -auPW /home/hildilab/projects/peptide_gpcr 172.18.184.28:/disk2/backup/hildilab/projects/ --log-file log.txt' hildilab
    echo 
    echo "backup doc data dev projects to backup server on cluster (exclude dev/ext and data/ext and .xtc)"
    rsync -auPW doc data dev projects --exclude=data/ext/ --exclude=dev/ext --exclude '*.xtc' renedominik@172.18.212.3:/backup/renedominik  --log-file log.txt
    echo
    echo "backup xtc files to cluster home"
    rsync -auPW --include '*/' --include '*.xtc' --exclude '*' projects renedominik@172.18.212.3:.  --log-file log.txt
    echo 
    echo "backup home rene happiness"
    rsync -auPW /home/rene $target --log-file log.txt
    echo
fi
