#!/bin/bash

path=~/dev/ext/rosetta/2018.09/main/source/bin

$path/fixbb.static.linuxgccrelease -in:file:s $1 -resfile /home/hildilab/projects/peptide_gpcr/resfile.txt -nstruct 1   

mv ${1:0:-4}_0001.pdb $2
