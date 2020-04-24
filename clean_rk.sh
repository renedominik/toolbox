#!/bin/bash

cmd="find /home/hildilab/projects/peptide_gpcr -type f \( -name \*~ -o -name '#'\* \) -exec rm {} \;"
#cmd="find /home/hildilab/projects/peptide_gpcr -type f -name \*~ -o -name '#'\*"

echo $cmd

eval $cmd
for i in 1 2 3 4 5; do
    echo now $i
    ssh 172.18.212.$i "$cmd"
done
