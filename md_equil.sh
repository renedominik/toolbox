#!bin/bash

#this script can be used for a fully automated equilibration; after charmm-gui prep / directory should contain charmm-gui-output | sims >  eq1 | simfiles | eq0 > sub1.sh


#set path
path=../simsfiles
ind=${path}/index.ndx
top=${path}/topol.top
charmmfiles=../../charmm-gui-pose3-dowser/gromacs
simssetup=../../../../../../../sims/sims-setup/

cd eq0

#copy necessary files
cp $charmmfiles/step5_charmm2gmx.pdb ./
cp $charmmfiles/step6.0_minimization.mdp ./
cp $charmmfiles/topol.top ../simsfiles/
cp $charmmfiles/index.ndx ../simsfiles/
cp -r $charmmfiles/toppar/ ../simsfiles/
cp -r $charmmfiles/restraints/ ../simsfiles/

#make tpr file
gmx grompp -f step6.0_minimization.mdp -o min.tpr -c step5_charmm2gmx.pdb -p $top -r step5_charmm2gmx.pdb

while [ ! -f min.tpr ]
do
 sleep 20
done


#minimization # add -ntmpi 6 for run on 6 cores and remove -dlb yes if problematic
gmx mdrun -deffnm min -dlb yes -v >& logmin
while [ ! -f min.gro ]
do
 sleep 20
done


#prepare index file ; define groups

mv $path/index.ndx $path/charmgui-index.ndx

echo -e "0 | 1 \n name 3 PROTMEMBLIG \n name 2 SOL \n q \n " | gmx make_ndx -f min.gro -o $path/index.ndx -n $path/charmgui-index.ndx

while [ ! -f $path/index.ndx ]
do
 sleep 20
done


#prepare sub.sh files for 7 equilibration steps #add cp sub and cp equil files
for i in {2..7}; do cp sub1.sh sub$i.sh; sed -i "s/eq1/eq${i}/g" sub$i.sh; done

#Equilibration eq0
for n in `seq 1 7`; do
 if [ "$n" -eq 1 ]; then 
  eqGro=min.gro
 else
  n0=$((n-1))
  eqGro=eq${n0}.gro
 fi
 eqMdp=equiL${n}.mdp 
 sub=sub${n}.sh
 tpr=eq${n}.tpr

 gmx grompp -f $eqMdp -o $tpr -c $eqGro -n $ind -p $top -r $eqGro
 bash sub${n}.sh
 #msub -E sub${n}.sh
 #Wait for the start
 while [ ! -f eq${n}.log ]
 do
  sleep 2
 done
 #Wait for the end
 while [ ! -f eq${n}.gro ]
 do
  sleep 20
 done

done
 

#Equilibration1 (random seed) #add cp sub7_${i}.sh
cd ../eq1

for i in {1..3}; do cp $simssetup/eq1/equiL7_${i}.mdp ./ ; done

eqGro=../eq0/eq7.gro 
for n in {1..3}; do 
 gmx grompp -f equiL7_${n}.mdp -o eq7_${n}.tpr -c $eqGro -n $ind -p $top -r $eqGro
bash sub7_${n}.sh
 
 #Wait for the start
 while [ ! -f eq7_${n}.log ]
 do
  sleep 2
 done
done

 while [[ ! -f eq7_1.gro  || ! -f eq7_2.gro || ! -f eq7_3.gro  ]]
 do
  sleep 20
 done
done
