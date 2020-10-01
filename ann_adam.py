#!/usr/bin/python3

import sys, numpy as np,copy

def Logistic(  x ):
    return 1.0 / ( 1.0 + np.exp( -x ) )

# pass sigmoid/logistic, not linear comb
def Logistic_Derivative( logi ):
    return logi * ( 1 - logi )

def TanH( x):
    return np.tanh(x)

# pass tanh
def TanH_Derivative( tanh ):
    return 1 - np.power( tanh, 2)

# one hot encoding for binary output 
def OneHotEncoding(Y):
    n_col = np.amax(Y) + 1
    binarized = np.zeros((len(Y), n_col))
    for i in range(len(Y)):
        binarized [i, Y[i]] = 1
    return binarized

def SoftMax( x ):
    exp_scores = np.exp(x)
    return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

# pass softmax
def SoftMax_Derivative( softi ):
    #S = softmax(x)
    S_vector = softi.reshape(softi.shape[0],1)
    S_matrix = np.tile(S_vector,softi.shape[0])
    np.diag(S) - (S_matrix * np.transpose(S_matrix))


def ReadData( filename ):
    x = []
    y = []
    with open( filename) as f:
        for l in f:
            c = [float(s) for s in l.split()]
            x.append( np.array(c[:-1] ) )
            #print( np.array(c[:-1] ,ndmin=2 ).shape)
            y.append( c[-1] )
    return np.array(x),np.array(y,ndmin=2).T

def InitializeWeights( length0, length1 ):
    #print( 'InitializeWeights', length0, length1 )
    return  np.random.randn( length0,length1 ) * np.sqrt( 1.0 / float(length0) )

def Mean( arrofarr):
    cp = np.array( copy.deepcopy(arrofarr[0]), dtype = object)
    for i in range(1,len(arrofarr)):
        cp = np.add( cp,  np.array( arrofarr[i], dtype = object) )
    cp = np.divide( cp, len(arrofarr) )
    return cp
                

################################################################
############      SETTINGS -  ADJUST ONLY HERE       ###########

learning = 0.01  
epsilon = 1e-8
beta1 = 0.9
beta2 = 0.999

X,ref = ReadData( sys.argv[1] )

hidden = [10,20,10,1]  # hidden plus output!!

iterations = 5000

test = 0.75

func = TanH
last_layer_func = func
deriv = TanH_Derivative

if hidden[-1] > 1:
    last_layer_func = SoftMax

np.random.seed(108)

print( '# learning rate: ', learning, 'beta1', beta1, 'beta2', beta2, 'hidden and output', hidden, 'iterations', iterations, 'test data ratio', test )
################################################################

if hidden[-1] > 1:
    y = OneHotEncoding( ref)
else:
    y = ref

x1 = []
r1 = []
x2 = []
r2 = []
for i in range( 0, len(X)):
    if np.random.random() <= test:
        x2.append( X[i] )
        r2.append( y[i] )
    else:
        x1.append( X[i] )
        r1.append( y[i] )

X_test = np.array( x2 )
y_test = np.array( r2 )
X_train = np.array( x1 )
y_train = np.array( r1 )


z = [None] * len(hidden) 
a = [None] * len(hidden) 
w = [None] * len(hidden) 
b = [None] * len(hidden)
d = [None] * len(hidden)
vw = [None] * len(hidden)
vb = [None] * len(hidden)
sw = [None] * len(hidden)
sb = [None] * len(hidden)

# initialize weights and other objects
w[0] = InitializeWeights( X_train[0].shape[0] , hidden[0] )  
b[0] = np.zeros( (1, hidden[0])) 
vw[0] = np.zeros( w[0].shape )
vb[0] = np.zeros( b[0].shape )
sw[0] = np.zeros( w[0].shape )
sb[0] = np.zeros( b[0].shape )

for i in range( 1, len(hidden)):
    w[i] = InitializeWeights( hidden[i-1], hidden[i] ) 
    b[i] = np.zeros( (1, hidden[i]))  #, ndmin=2)
    vw[i] = np.zeros( w[i].shape )
    vb[i] = np.zeros( b[i].shape )
    sw[i] = np.zeros( w[i].shape )
    sb[i] = np.zeros( b[i].shape )

    
# main loop
for i in range(0, iterations):
    t = i+1
    ### forward propagation ###
    # first layer
    z[0] = np.dot( X_train, w[0] ) + b[0]
    a[0] = func( z[0] )
    for h in range(1,len(hidden)-1):
        z[h] = np.dot( a[h-1] , w[h] ) + b[h]
        a[h] = func( z[h] )
    # last layer
    z[-1] = np.dot( a[-2] , w[-1] ) + b[-1]
    a[-1] = last_layer_func( z[-1] )
    
    ### backpropagation ###
    # last layer
    d[-1] = y_train - a[-1]
    error = np.mean( np.abs( d[-1] ) )

    dW = a[-2].T.dot( d[-1] )
    vw[-1] = beta1 * vw[-1] + (1-beta1) * dW
    vw_corr = vw[-1] / float( 1.0 - beta1**t )
    sw[-1] = beta2 * sw[-1] + (1-beta2) * (dW**2)
    sw_corr = sw[-1] / float( 1.0 - beta2**t )
    w[-1] += learning * vw_corr / ( np.sqrt( sw_corr)+epsilon)

    db = np.sum( d[-1], axis = 0, keepdims = True )
    vb[-1] = beta1 * vb[-1] + (1-beta1) * db
    vb_corr = vb[-1] / float( 1.0 - beta1**t )
    sb[-1] = beta2 * sb[-1] + (1-beta2) * (db**2)
    sb_corr = sb[-1] / float( 1.0 - beta2**t )
    b[-1] += learning * vb_corr / ( np.sqrt( sb_corr ) + epsilon )

    # middle layers
    for h in range( len(hidden) - 2, -1, -1 ):
        d[h] = d[h+1].dot( w[h+1].T ) * deriv( a[h] )
        dW = a[h-1].T.dot( d[h] ) 
        vw[h] = beta1 * vw[h] + (1-beta1) * dW
        vw_corr = vw[h] / float( 1 - beta1**t )
        sw[h] = beta2 * sw[h] + (1-beta2) * (dW**2)
        sw_corr = sw[h] / float( 1 - beta2**t )
        w[h] += learning * vw_corr / ( np.sqrt( sw_corr)+epsilon)

        db = np.sum( d[h], axis=0, keepdims=True )
        vb[h] = beta1 * vb[h] + (1-beta1) * db
        vb_corr = vb[h] / float( 1 - beta1**t )
        sb[h] = beta2 * sb[h] + (1-beta2) * (db**2)
        sb_corr = sb[h] / float( 1 - beta2**t )
        b[h] += learning * vb_corr / ( np.sqrt( sb_corr ) + epsilon )

        
    # first layer
    d[0] = d[1].dot( w[1].T ) * deriv( a[0] )
    dW = X_train.T.dot( d[0] ) 
    vw[0] = beta1 * vw[0] + (1-beta1) * dW
    vw_corr = vw[0] / float( 1 - beta1**t )
    sw[0] = beta2 * sw[0] + (1-beta2) * (dW**2)
    sw_corr = sw[0] / float( 1 - beta2**t )
    w[0] += learning * vw_corr / ( np.sqrt( sw_corr)+epsilon)

    db = np.sum( d[0], axis=0, keepdims = True  )
    vb[0] = beta1 * vb[0] + (1-beta1) * db
    vb_corr = vb[0] / float( 1 - beta1**t )
    sb[0] = beta2 * sb[0] + (1-beta2) * (db**2)
    sb_corr = sb[0] / float( 1 - beta2**t )
    b[0] += learning * vb_corr / ( np.sqrt( sb_corr ) + epsilon )

    
    if i % 100 == 0:
        print( 'Loss/accuracy: ', i,  str(round(error,5)) , str (round( (1 - error) * 100,2)) )
            

z[0] = np.dot( X_test, w[0] ) + b[0]
a[0] = func( z[0] )
for h in range(1,len(hidden)-1):
    z[h] = np.dot( a[h-1] , w[h] ) + b[h]
    a[h] = func( z[h] )
z[-1] = np.dot( a[-2] , w[-1] ) + b[-1]
a[-1] = last_layer_func( z[-1] )
error =  np.mean( np.abs( y_test - a[-1] ))
print( 'test loss/accuracy:',  str(round(error,5)) , str (round( (1 - error) * 100,2)) )
