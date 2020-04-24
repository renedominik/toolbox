#!/bin/bash

path=/home/hildilab/dev/ext/rosetta/2018.09/main/
b=${1##*/}
base=${b%.*}
$path/source/bin/BuildPeptide.static.linuxgccrelease -database $path/database -in:file:fasta $1 -out:file:o $base.pdb

