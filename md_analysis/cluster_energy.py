#!/usr/bin/python3

####### Adam Produktions #######

import sys
import os
from fnmatch import fnmatch
import numpy as np

if len(sys.argv) != 5:
    print("USAGE: clus_ener.py #AllEnergiesInOneFileWithoutAnythingElse #FileWithTimeStamps #fileNameWhereMeansShallBeSaved #CoulmnNumberPythonArrayStyle")
    quit()

filename = ''.join(["./", sys.argv[3]])   
pattern = []
t = 1
c = 0
sums = 0
energies = []
stand = np.array([])

#spezify which coulmn of the energy.xvg file you want to use aus the fourth input. For example if it is the (normal counting) fourth coulmn, write down 3 (normalnumber - 1) 
coulmn = int(sys.argv[4])


f = open(sys.argv[2], 'r') #cluster index file oeffnen
g = open(sys.argv[1], 'r') #open all of the energys

for time in f: # going threw the given times 
    fraction = time.split(' ') # splitting up the times
    #print(fraction)
    if not '[' in fraction:
        for i in fraction:
            sahne = i.replace('\n','') #getting those killer linebraks away
            pattern.append(''.join([sahne,'00.000000'])) #loosening up, cause the zeros are missing and making a list of all the times

#print(pattern)
#print(len(pattern))

for line in g:
    particles = line.split()
    if particles[0] in pattern: #if the time is in pattern (which is the times from the cluster)
        print(particles[coulmn])#printing the energies
        sums += float(particles[coulmn])
        energies.append(particles[coulmn])
        #print(t)
        #t += 1

#print(t)
#print(len(pattern))
print('Mean:', sums/len(pattern))


for i in energies:
    energies[c] = (abs(float(i)-(sums/len(pattern))))**2
    c += 1

stand = np.sqrt(np.sum(np.array(energies))/(len(pattern))) #berechnung dr standardabweichung

print('Standarddeviation:', stand)

if os.path.isfile(filename) == False:
    h = open(filename,"w+")
    h.write('\n'+sys.argv[2]+' '+str(sums/len(pattern))+' '+str(stand))
else:
    h = open(filename,"a") 
    h.write('\n'+sys.argv[2]+' '+str(sums/len(pattern))+' '+str(stand))

h.close()

g.close()
f.close()

