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

def OrthogonalizeRows( m, row = 2):
    m[ row%3 ] = np.cross( m[ (row+1)%3 ] , m[ (row+2)%3 ] )
    return m

def Superimpose( mol1, mol2):
    #print( 'length:', len(mol1), len(mol2))
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
    coo1 = mol1 - cms1
    coo2 = mol2 - cms2
    m = mol1.transpose().dot( mol2)
    r = m.dot( m.transpose() )
    print( 'data matrix')
    print(r)
    eigenvalues, eigenvectors = np.linalg.eig( r)
    #print( 'eigenvalues:')
    #print( eigenvalues)
    eigenvectors = eigenvectors.transpose()
    #print( 'eigenvectors:')
    #print( eigenvectors )
    #print( 'det eigenvectors', np.linalg.det( eigenvectors))

    if eigenvalues[0] < eigenvalues[1]:
        eigenvectors[[0,1]] = eigenvectors[[1,0]]
        eigenvalues[0],eigenvalues[1] = eigenvalues[1],eigenvalues[0]
        print( 'swap01:', eigenvalues)
    if eigenvalues[1] < eigenvalues[2]:
        eigenvectors[[1,2]] = eigenvectors[[2,1]]
        eigenvalues[1],eigenvalues[2] = eigenvalues[2],eigenvalues[1]
        print( 'swap12:', eigenvalues)
    if eigenvalues[0] < eigenvalues[1]:
        eigenvectors[[0,1]] = eigenvectors[[1,0]]
        eigenvalues[0],eigenvalues[1] = eigenvalues[1],eigenvalues[0]
        print( 'swap01b:', eigenvalues)

    #eigenvectors[[0,2]] = eigenvectors[[2,0]]
    #eigenvalues[0],eigenvalues[2] = eigenvalues[2],eigenvalues[0]
    #print( 'eigenvalues:')
    #print( eigenvalues)
    #print( 'eigenvectors:')
    #print( eigenvectors )
    #print( 'det eigenvectors', np.linalg.det( eigenvectors))

    eigenvectors = OrthogonalizeRows( eigenvectors)
    #print( 'eigenvectors orthogonalized:\n')
    #print( eigenvectors )
    #print( 'det eigenvectors', np.linalg.det( eigenvectors))
    
    rot = eigenvectors.dot( m )
    #print( 'rot initial:\n', rot)
    
    for i in range( 0, 2):
        t = 1.0 / np.sqrt( eigenvalues[i])
        #print( 't:', t)
        for j in range( 0, 3):
            rot[i][j] *= t
    #print( 'rot rep:\n', rot)

    rot = OrthogonalizeRows( rot ) # critical step, might fail
    #rot = sym( rot ) # critical step, might fail
    rot = rot.transpose().dot( eigenvectors)
    #print( rot.shape )
    #print( 'rot:', rot)
    #print( 'det:', np.linalg.det(rot))
    #print( mol2.shape)
    #print( mol2[0] )
    return rot, cms1, cms2

#    m = np.dot( rot, mol1.transpose() ).transpose()
#    print( m[0])
#    print( m[1])
#    print( m[2])

#    mol2 = rot.dot( mol2.transpose()).transpose()
#    mol2 += cms1
#    print( 'superimposed:', mol2[0])
#    #print( mol2.shape)
#    #return mol2, rot


def RMSD( mol1, mol2):
    s = 0
    for m1,m2 in zip( mol1,mol2):
        m =  m1 - m2
        s += m.dot( m)
    return np.sqrt( s / len( mol1))

    
def CooInNewRef( pos, rot, cms1, cms2):
    pos -= cms2
    rot.dot( pos.transpose()).transpose()
    pos += cms1
    return pos
