#!/home/hildilab/anaconda3/bin/python3

from scipy.stats import ks_2samp as ks
import numpy as np
import sys
import os

#################### Functions ###############

def calpha(a,b,c):
    return a*np.sqrt((b+c)/(c*b))


#################### Variables #################

j = 0
number1 = 0
number2 = 0
alpha = [0.1,0.05, 0.025, 0.01,0.005,0.001]
c = {0.1:1.22,0.05:1.36, 0.025:1.48, 0.01:1.63,0.005:1.73,0.001:1.95}
one = []
two = []
d = 0.1

################### load data #############

f = open(sys.argv[1], 'r')
g = open(sys.argv[2], 'r')
filename1 = [int(i) for i in list(sys.argv[1]) if i.isdigit()]
filename2 = [int(i) for i in list(sys.argv[2]) if i.isdigit()]

for idx, val in enumerate(filename1):
    number1 += val*10**(len(filename1)-1-idx)

for idx, val in enumerate(filename2):
    number2 += val*10**(len(filename2)-1-idx)

for l in f:
    if (l[0] != 'S') and (l[0] != 'M'):
        one.append(float(l[0:(len(l)-1)]))

for l in g:
    if (l[0] != 'S') and (l[0] != 'M'):
        two.append(float(l[0:(len(l)-1)]))


################# ks test  ####################
#while d not in alpha:
    #d = float(input('Please enter a value for alpha:={0.1,0.05, 0.025, 0.01,0.005,0.001}. Significance falls by taking the lower values: '))


################# printing ####################

if os.path.isfile(''.join(["./", sys.argv[3]])) == False:
    h = open(''.join(["./", sys.argv[3]]), "w+")
    if float(ks(one, two)[1]) < calpha(float(c[d]),len(one),len(two)):
        h.write('Since the p-value is smaller than the critical value we can reject the hypothisis!\n')
        h.write('1 ' + 'The Test is for: ' + str(number1) + '-'+ str(number2)+'\n')
    else:
        h.write('Since the p-value is larger than the critical value we cannot reject the hypothisis!\n')
        h.write('0 ' + 'The Test is for: ' + str(number1) + '-'+ str(number2)+'\n')
    h.write('You entered : '+ str(d) +'\n'+'The value of c(alpha) is then: '+ str(c[d])+'\n')
    h.write('The critical value is: '+ str(calpha(float(c[d]),len(one),len(two)))+'\n')
    h.write('The Result of the KS-Test is: ' + str(ks(one, two))+'\n\n\n')

else:
    h = open(''.join(["./", sys.argv[3]]), "a")
    if float(ks(one, two)[1]) < calpha(float(c[d]),len(one),len(two)):
        h.write('Since the p-value is smaller than the critical value we can reject the hypothisis!\n')
        h.write('1 ' + 'The Test is for: ' + str(number1) + '-'+ str(number2)+'\n')
    else:
        h.write('Since the p-value is larger than the critical value we cannot reject the hypothisis!\n')
        h.write('0 ' + 'The Test is for: ' + str(number1) + '-'+ str(number2)+'\n')
    h.write('You entered : '+ str(d) +'\n'+'The value of c(alpha) is then: '+ str(c[d])+'\n')
    h.write('The critical value is: '+ str(calpha(float(c[d]),len(one),len(two)))+'\n')
    h.write('The Result of the KS-Test is: ' + str(ks(one, two))+'\n\n\n')

h.close()
g.close()
f.close()
