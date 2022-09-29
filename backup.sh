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
    rm log.txt
    echo "backup to $target" 
    echo "****  backup to $target  ****  " > /home/hildilab/dev/scripts/status.log
    echo >> /home/hildilab/dev/scripts/status.log
    echo "backup server home" >> /home/hildilab/dev/scripts/status.log
    su -c 'rsync -auPW  --exclude=.config --exclude=.local  --exclude=\*~ --exclude .git  hildilab@proteinformatics.uni-leipzig.de:* /home/hildilab/projects/server/proteinformatics/home/ --log-file log.txt' hildilab
    
    echo >> /home/hildilab/dev/scripts/status.log
    echo "****  backup server www  ****" 
    echo "backup server www" >> /home/hildilab/dev/scripts/status.log
    su -c 'rsync -auPW hildilab@proteinformatics.uni-leipzig.de:/var/www :/etc/apache2 /home/hildilab/projects/server/proteinformatics/ --log-file log.txt' hildilab
    echo >> /home/hildilab/dev/scripts/status.log
    
    echo "****  backup spectrum home from happiness  ****" 
    echo "backup spectrum home from happiness" >> /home/hildilab/dev/scripts/status.log
    rsync -auPW    --exclude=.cache --exclude=.config --exclude=.local  --exclude=.mozilla --exclude=\*~ --exclude .git /home/spectrum $target --log-file log.txt

    echo >> /home/hildilab/dev/scripts/status.log
    echo "****  backup doc data dev projects to backup server on cluster (exclude dev/ext and data/ext and .xtc)  ****" 
    echo "backup doc data dev projects to backup server on cluster (exclude dev/ext and data/ext and .xtc)" >> /home/hildilab/dev/scripts/status.log
    su -c 'rsync -auPW doc data dev projects --exclude=data/ext/ --exclude=dev/ext --exclude \*.xtc  --exclude=.config --exclude=.local  --exclude=\*~ --exclude .git renedominik@172.18.212.3:/backup/renedominik  --log-file log.txt' hildilab
    
    echo >> /home/hildilab/dev/scripts/status.log
    echo "****  backup xtc files to cluster home  ****" 
    echo "backup xtc files to cluster home" >> /home/hildilab/dev/scripts/status.log
    #su -c 'rsync -auPW --include '*/' --include '*.xtc' --exclude '*' projects renedominik@172.18.212.3:.  --log-file log.txt' hildilab
    #su -c 'rsync -auPW --include '*/'  --exclude '*' --include '*.xtc' projects renedominik@172.18.212.3:.  --log-file log.txt' hildilab
    su -c 'rsync -auPW --include \*/  --include \*.xtc --exclude \*  projects renedominik@172.18.212.3:.' hildilab
    
    echo  >> /home/hildilab/dev/scripts/status.log
    echo "****  backup home rene happiness  ****" 
    echo "backup home rene happiness" >> /home/hildilab/dev/scripts/status.log
    rsync -auPW  --exclude=.config --exclude=.local  --exclude=\*~ --exclude .git /home/rene $target --log-file log.txt
    
    echo    >> /home/hildilab/dev/scripts/status.log
    echo "****  backup project peptide_gpcr to gladness  ****" 
    echo "backup project peptide_gpcr to gladness" >> /home/hildilab/dev/scripts/status.log
    su -c 'rsync -auPW /home/hildilab/projects/peptide_gpcr 172.18.184.28:/disk2/backup/hildilab/projects/ --log-file log.txt' hildilab
    
    echo  >> /home/hildilab/dev/scripts/status.log
    echo "****  backup home hildilab happiness  ****" 
    echo "backup home hildilab happiness" >> /home/hildilab/dev/scripts/status.log
    su -c 'rsync -auPW  --exclude=blast --exclude=snap --exclude=.cache --exclude=.config --exclude=.local --exclude=.mozilla  --exclude=\*~ --exclude .git  /home/hildilab $target --log-file log.txt' hildilab
    echo
fi
