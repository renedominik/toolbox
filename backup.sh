#!/bin/bash

rsync -auP /home/hildilab/projects/peptide_gpcr /media/hildilab/Elements/projects

find  /home/hildilab/data/ext/pdb \( -name \*.py -o -name \*.sh -o -name README\* \) -exec rsync -auP {} /media/hildilab/Elements/data/ext/pdb/ \;

