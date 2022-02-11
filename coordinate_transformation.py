#!/usr/bin/python3


import numpy as np


def AbsolutePosition( rel, pos1, pos2, pos3):
    v1 = pos2 - pos1
    v2 = pos2 - pos3
    v3 = np.cross( v1, v2)
    m = np.array( [ v1, v2, v3 ] ).transpose()
    pos = np.dot(m,rel) + pos2
    return pos


def RelativeCoordinates( ref1, ref2, ref3, pos):
    v1 = ref2 - ref1
    v2 = ref2 - ref3
    v3 = np.cross( v1, v2)
    m = np.array( [ v1, v2, v3 ] ).transpose()
    pos -= ref2
    x = np.linalg.solve( m, pos)
    return x

def CMS( pos ):
    s = np.array([0,0,0])
    for p in pos:
        s = s + p
        #print( '*',s)
    return s / len(pos)

# diagonalize matrix
def sym(w):
    from scipy.linalg import sqrtm, inv
    return w.dot(inv(sqrtm(w.T.dot(w))))

def Superimpose( mol1, mol2):
    #print( mol1[0] )
    #print( mol2[0] )
    cms1 = CMS( mol1)
    cms2 = CMS( mol2)
    #print( 'cms')
    #print(cms1)
    #print(cms2)
    mol1 -= cms1
    mol2 -= cms2
    #print( 'centered:')
    #print( mol1[0] )
    #print( mol2[0] )
    #print( 'check:', CMS( mol1))
    #coo1 = mol1 - cms1
    #coo2 = mol2 - cms2
    m = mol1.transpose().dot( mol2)
    r = m.dot( m.transpose() )
    eigenvalues, eigenvectors = np.linalg.eig( r)
    #print( 'eigenvalues:')
    #print( eigenvalues)
    eigenvectors = eigenvectors.transpose()

    if eigenvalues[0] < eigenvalues[1]:
        eigenvectors[[0,1]] = eigenvectors[[1,0]]
        eigenvalues[0],eigenvalues[1] = eigenvalues[1],eigenvalues[0]
        #print( 'swap01:', eigenvalues)
    if eigenvalues[1] < eigenvalues[2]:
        eigenvectors[[1,2]] = eigenvectors[[2,1]]
        eigenvalues[1],eigenvalues[2] = eigenvalues[2],eigenvalues[1]
        #print( 'swap12:', eigenvalues)
    if eigenvalues[0] < eigenvalues[1]:
        eigenvectors[[0,1]] = eigenvectors[[1,0]]
        eigenvalues[0],eigenvalues[1] = eigenvalues[1],eigenvalues[0]
        #print( 'swap01b:', eigenvalues)

    eigenvectors = sym( eigenvectors)
    rot = eigenvectors.dot( m )

    for i in range( 0, 2):
        t = 1.0 / np.sqrt( eigenvalues[i])
        for j in range( 0, 3):
            rot[i][j] *= t

    rot = sym( rot )
    rot = rot.transpose().dot( eigenvectors)
    #print( rot.shape )
    #print( mol2.shape)
    #print( mol2[0] )

    mol2 = rot.dot( mol2.transpose()).transpose()
    mol2 += cms1
    #print( 'superimposed')
    #print( mol2[0] )
    #print( mol2.shape)
    return mol2
    
