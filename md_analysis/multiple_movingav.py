#!/home/hildilab/anaconda3/bin/python3

##### Made by Adam Zech ######

import numpy as np
import sys
import matplotlib.pyplot as plt

print('I am doing my JOB')

if len(sys.argv) < 5:
    print('USAGE: InputFile AverageRadius \'xlabel\' \'ylabel\' NameOfOutPutfile', '\n\n', 'Don\'t forget to put the dimension into the label, or the program won\'t work properly!')
    quit()

def mov_av(name, data, n, c):
    av = np.array([])
    labels = ' '.join([str(i)for i in ((sys.argv[4].split())[:-2])])
    for i in range(n,len(data[:,1])-n):
        av = np.append(av, sum(data[:,1][i-n:i+(n+1)])/(2*n+1))
    plt.plot(data[:,0][n:-n]/1000000, av, color = c, linewidth = 0.8, alpha = 0.75, label = 'Moving Average of ' + labels +' '+ ' '.join(name))
    plt.plot(data[:,0]/1000000, data[:,1], color = c, linewidth = 0.8, alpha = 0.25)
    plt.grid()
    return 1

f = open(sys.argv[1], 'r')
for l in f:
    if l[0] != '#':
        data = np.loadtxt(l.split()[0], comments=['#','@'])
        mov_av(l.split()[2:], data, int(sys.argv[2]), l.split()[1])

plt.xlabel(sys.argv[3])
plt.ylabel(sys.argv[4])
plt.savefig(sys.argv[5], bbox_inches='tight', dpi=250)
plt.legend(fontsize=8)
plt.show()
