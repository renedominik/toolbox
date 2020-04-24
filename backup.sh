#!/bin/bash

### REMARK ###
### Execute as root ###

su -c 'rsync -auP hildilab@proteinformatics.uni-leipzig.de:* /home/hildilab/projects/server/proteinformatics/home/' hildilab
su -c 'rsync -auP hildilab@proteinformatics.uni-leipzig.de:/var/www :/etc/apache2/sites-available/000-default.conf /home/hildilab/projects/server/proteinformatics/' hildilab
rsync -auP /home/rene /media/hildilab/e98a64e4-4463-4ee9-9819-a7c00b12fc4d/ 
rsync -auP  --exclude=blast --exclude=snap /home/hildilab /media/hildilab/e98a64e4-4463-4ee9-9819-a7c00b12fc4d/
su -c 'rsync -auP /home/hildilab/projects/peptide_gpcr 172.18.184.28:/disk2/backup/hildilab/projects/' hildilab
