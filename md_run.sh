#!/bin/bash

for i in {1..3}; do
    cd run$i
    echo starting run$i!
    ./sub.sh
    echo finished run$i
    
while [ ! -f run${n}.part0001.log ]
  do
   sleep 2
done
cd ../
done

echo all simulations done!
