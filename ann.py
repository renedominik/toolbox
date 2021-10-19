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

learning = 0.0000005  
regularization = 0.000001 

X,ref = ReadData( sys.argv[1] )

hidden = [10,20,10,1]  # hidden plus output!!

iterations = 50000

test = 0.75

func = TanH
last_layer_func = func
deriv = TanH_Derivative

if hidden[-1] > 1:
    last_layer_func = SoftMax

np.random.seed(108)

print( '# learning rate: ', learning, 'regularization', regularization, 'hidden and output', hidden, 'iterations', iterations, 'test data ratio', test )
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

# initialize weights and other objects
w[0] = InitializeWeights( X_train[0].shape[0] , hidden[0] )  
b[0] = np.zeros( (1, hidden[0]))  #,ndmin=2 )
#z[0] = np.empty( (1, hidden[0]))  #,ndmin=2 )
#a[0] = np.empty( (1, hidden[0]))  #,ndmin=2 )
for i in range( 1, len(hidden)):
    w[i] = InitializeWeights( hidden[i-1], hidden[i] ) 
    b[i] = np.zeros( (1, hidden[i]))  #, ndmin=2)
    #z[i] = np.empty( (1, hidden[i]))  #, ndmin=2)
    #a[i] = np.empty( (1, hidden[i]))  #, ndmin=2)

#e = np.array( 1, len(hidden) )
#d = np.empty( (1, len(hidden)) )

#print( 'X', X_train.shape)
#print( 'y', y.shape)
#for i in range( 0, len(hidden)):
#    #print( 'z', z[i].shape)
#    print( 'w', w[i].shape)
#    #print( 'a', a[i].shape)
#    print( 'b', b[i].T.shape)


    
# main loop
for i in range(0, iterations):
    
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
    dW -= regularization * w[-1]
    w[-1] += learning * dW

    db = np.sum( d[-1], axis = 0, keepdims = True )
    b[-1] += learning * db

    # middle layers
    for h in range( len(hidden) - 2, -1, -1 ):
        d[h] = d[h+1].dot( w[h+1].T ) * deriv( a[h] )
        dW = a[h-1].T.dot( d[h] ) - regularization * w[h]
        w[h] += learning * dW
        db = np.sum( d[h], axis=0, keepdims=True )
        b[h] += learning * db
        
    # first layer
    d[0] = d[1].dot( w[1].T ) * deriv( a[0] )
    dW = X_train.T.dot( d[0] ) - regularization * w[h]
    w[0] += learning * dW
    db = np.sum( d[0], axis=0, keepdims = True  )
    b[0] += learning * db
    
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
print( '### test loss/accuracy:',  str(round(error,5)) , str (round( (1 - error) * 100,2)) )
