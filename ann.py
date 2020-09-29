#!/usr/bin/python3

import sys, numpy as np,copy

def Logistic(  x ):
    return 1.0 / ( 1.0 + np.exp( x ) )

def ReadData( filename ):
    x = []
    y = []
    with open( filename) as f:
        for l in f:
            c = [float(s) for s in l.split()]
            x.append( np.array(c[:-1] ,ndmin=2 ))
            #print( np.array(c[:-1] ,ndmin=2 ).shape)
            y.append( c[-1] )
    return np.array(x),np.array(y)

def InitializeWeights( length0, length1 ):
    print( 'InitializeWeights', length0, length1 )
    return  np.random.randn( length1,length0 ) * np.sqrt( 1.0 / float(length0) )

def Mean( arrofarr):
    cp = np.array( copy.deepcopy(arrofarr[0]), dtype = object)
    for i in range(1,len(arrofarr)):
        cp = np.add( cp,  np.array( arrofarr[i], dtype = object) )
    cp = np.divide( cp, len(arrofarr) )
    return cp
                
def Update( w, mean_slopes, alpha):
    #print( alpha)
    for i in range( 0, len(w)):
        #print( 'update', i, w[i].shape, mean_slopes[i].shape)
        w[i] +=  alpha * mean_slopes[i]
    return w

def UpdateT( w, mean_slopes, alpha):
    #print( alpha)
    for i in range( 0, len(w)):
        #print( 'update', i, w[i].shape, mean_slopes[i].shape)
        w[i] +=  alpha * mean_slopes[i].T
    return w


alpha = 0.01

data,ref = ReadData( sys.argv[1] )

hidden = [12,8,1]

iterations = 1500

z = [None] * len(hidden) 
a = [None] * len(hidden) 
w = [None] * len(hidden) 
b = [None] * len(hidden) 

# initialize weights and other objects
w[0] = InitializeWeights( data[0].shape[1] , hidden[0] )
b[0] = np.array( np.zeros( hidden[0]),ndmin=2 )
z[0] = np.array( np.empty( hidden[0]),ndmin=2 )
a[0] = np.array( np.empty( hidden[0]),ndmin=2 )
for i in range( 1, len(hidden)):
    w[i] = InitializeWeights( hidden[i-1], hidden[i] ) 
    b[i] = np.array( np.zeros( hidden[i] ), ndmin=2)
    z[i] = np.array( np.empty( hidden[i] ), ndmin=2)
    a[i] = np.array( np.empty( hidden[i] ), ndmin=2)



for i in range( 0, len(hidden)):
    print( 'z', z[i].shape)
    print( 'w', w[i].shape)
    print( 'a', a[i].shape)
    print( 'b', b[i].T.shape)

# main loop
for i in range(0, iterations):
    slopes = []
    deltas = []
    error = 0
    for d,r in zip(data,ref):
        #predicted = forward_propagation( w, b, data )
        z[0] = w[0].dot(d.T) + b[0].T
        a[0] = Logistic( z[0] )
        for h in range(1,len(hidden)):
            z[h] = w[h].dot( a[h-1]) + b[h].T
            a[h] = Logistic( z[h] )
        
        #slope,delta = backward_propagation( )
        derivative_b = [None] * len(hidden)
        derivative_w = [None] * len(hidden)
        derivative_b[-1] = (a[-1] - r ) 
        error += derivative_b[-1] ** 2
        derivative_w[-1] =  derivative_b[-1].dot( a[-2].T)    # what if output dim > 1 ????, must match weight dims,
        for h in range( len(hidden) - 2, -1, -1 ):
            if derivative_b[h+1].shape == (1,1):
                derivative_b[h] = np.multiply( w[h+1].T , np.multiply( a[h], np.subtract( 1 , a[h] ))) * derivative_b[h+1] 
            else:
                derivative_b[h] = np.multiply( w[h+1].T , np.multiply( a[h], np.subtract( 1 , a[h] ))).dot( derivative_b[h+1] )
            if h > 0:
                derivative_w[h] = derivative_b[h].dot( a[h-1].T) 
            else:
                derivative_w[h] =  derivative_b[h].dot( d)
        slopes.append( derivative_w)
        deltas.append( derivative_b)
    mean_slopes = Mean( slopes )
    mean_deltas = Mean( deltas )
    w = Update( w, mean_slopes, alpha)
    b = UpdateT( b, mean_deltas, alpha)


    if i % 5 == 0:
        print( 'prediction quality:', i, np.sqrt(error)[0][0] )
            

