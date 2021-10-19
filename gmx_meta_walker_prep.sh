#!/bin/bash

n=1
echo 0 > null
top=../simfiles/topol.top
index=../simfiles/index.ndx
for d in `awk '{ if( length($1) > 0 ) print $1}' $1`
do
    gmx trjconv -f $2.xtc -o walker$n.gro -s $2.tpr -dump $d < null
    gmx grompp -f ${2:0:-1}.mdp -c walker$n.gro -p $top -n $index -o walker$n.tpr
    ((n++))
done
