#!/usr/bin/python3

### copyright: rene staritzbichler, 27.8.20

import numpy as np
from sklearn.decomposition import PCA
import sys, copy

if len(sys.argv) < 2:
    print( "USAGE: ", sys.argv[0], "FILE NR_COMPONENTS (optional: COL1 ..)")
    exit(1)

nr_components = int(sys.argv[2])
data = []
cols = []
if len(sys.argv) > 3:
    cols = [int(x) for x in sys.argv[3:]]


if len(cols) > 0:
    with open( sys.argv[1]) as f:
        for l in f:
            data.append( [float(x[1]) for x in enumerate( l.split() ) if x[0] in cols] )
else:
    with open( sys.argv[1]) as f:
        for l in f:
            data.append( [float(x) for x in l.split()] )

            
data = np.array( data)
#print( '#', data.shape)

pca = PCA(n_components=nr_components)
#pca.fit(data)
transformed = pca.fit_transform( data )

print( '# eigenvectors: \n', pca.components_)

print( '# eigenvalues:', pca.explained_variance_)

#print( "# data:\n", data[0])
print( '# transformed from sklearn PCA:\n',transformed[0])

cms = np.mean( data, axis=0)
#print( '# cms:', cms)
print( '# check: \n', ((data-cms).dot( pca.components_.T))[0] )

##### test by hand implementations: #####

#### FIRST APPROACH ####
### solve eigen gleichung
# covariance matrix
cvm = np.cov( data.T ) 
eigen_values, eigen_vectors = np.linalg.eig( cvm )
## sort eigenvalues, eigenvectors
idx = np.argsort(eigen_values, axis=0)[::-1]
sorted_eigen_vectors = eigen_vectors[:, idx]
print( '# eigenvalues: ', eigen_values,'\n# eigenvectors:\n', sorted_eigen_vectors.T )
## a slightly different way of sorting:
# Make a list of (eigenvalue, eigenvector) tuples
eigen_pairs = [(np.abs(eigen_values[i]), eigen_vectors[:, i]) for i in range(len(eigen_values))]
eigen_pairs.sort(key=lambda k: k[0], reverse=True)
w = np.hstack((eigen_pairs[0][1][:, np.newaxis], eigen_pairs[1][1][:, np.newaxis], eigen_pairs[2][1][:, np.newaxis]))
#print('Matrix W:\n', w.T)
transf = np.dot( (data-cms), sorted_eigen_vectors)
print( "# transformed data: \n", transf[0] )
print('# max diff:', np.abs(transf-transformed).max()) # not soo small ...

##### SECOND APPROACH #####
### single value decomposition
u, s, vh = np.linalg.svd( (data-cms) , full_matrices=False)
## straight forward way of applying it
# transformed version based on WIKI: t = X@vh.T = u@np.diag(s)
t_svd1=  (data-cms)@vh.T
t_svd2= u@np.diag(s)
print( "# transformed based on SVD: \n", t_svd1[0] )
print( "# transformed based on SVD: \n", t_svd2[0] )
print('# max diff:', np.abs(t_svd1-transformed).max()) # not soo small ...
print('# max diff:', np.abs(t_svd2-transformed).max()) # not soo small ...
## sklearn like way
max_abs_cols = np.argmax(np.abs(u), axis=0)
signs = np.sign(u[max_abs_cols, range(u.shape[1])])
u *= signs
vh *= signs.reshape(-1,1)
t_svd1=  (data-cms)@vh.T
t_svd2= u@np.diag(s)
print( "# transformed based on sklearn SVD: \n", t_svd1[0] )
print( "# transformed based on sklearn SVD: \n", t_svd2[0] )
print('# max diff:', np.abs(t_svd1-transformed).max()) # pretty small value :)
print('# max diff:', np.abs(t_svd2-transformed).max()) # pretty small value :)



#print( 'orthogonality check: inverse matrix (must be equal transposed):\n', np.linalg.inv(sorted_eigen_vectors))

