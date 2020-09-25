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
            x.append( np.array(c[:-1]) )
            y.append( c[-1] )
    return np.array(x),np.array(y)

def InitializeWeights( length0, length1 ):
    print( 'InitializeWeights', length0, length1 )
    return  np.random.randn( length1,length0 ) * np.sqrt( 1.0 / float(length0) )

def Mean( arrofarr):
    cp = copy.deepcopy(arrofarr[0])
    for i in range(1,len(arrofarr)):
        cp = np.add( cp, arrofarr[i] )
    cp = np.devide( cp, len(arrofarr) )
#        for j in range( 0, len(cp)):
#            for k in range( 0, len( cp[j] ) ):
#                cp[j][k] += arrofarr[i][j][k]
#    for j in range( 0, len(cp)):
#        for k in range( 0, len( cp[j] ) ):
#            cp[j][k] = cp[j][k] / len(arrofarr)
    return cp
                


alpha = 0.00000025

data,ref = ReadData( sys.argv[1] )

hidden = [4,8,12,1]

iterations = 1000

z = [None] * len(hidden) 
a = [None] * len(hidden) 
w = [None] * len(hidden) 
b = [None] * len(hidden) 

# initialize weights and other objects
w[0] = InitializeWeights( len(data[0]) , hidden[0] )
b[0] = np.zeros( hidden[0] )
z[0] = np.empty( hidden[0] )
a[0] = np.empty( hidden[0] )
for i in range( 1, len(hidden)):
    w[i] = InitializeWeights( hidden[i-1], hidden[i] ) 
    b[i] = np.zeros( hidden[i] )
    z[i] = np.empty( hidden[i] )
    a[i] = np.empty( hidden[i] )

#print( 'weights:' , w)
#z = np.array(z,dtype=object)
#w = np.array(w,dtype=object)
#a = np.array(a,dtype=object)
#b = np.array(b,dtype=object)

for i in range( 0, len(hidden)):
    print( 'z', z[i].shape)
    print( 'w', w[i].shape)
    print( 'a', a[i].shape)
    print( 'b', b[i].shape)

# main loop
for i in range(0, iterations):
    slopes = []
    deltas = []
    for d in data:
        #predicted = forward_propagation( w, b, data )
        z[0] = w[0] * d + b[0]
        a[0] = Logistic( z[0] )
        print( 'layer 0:', 'z', z[0].shape, 'w', w[0].shape, 'd', d.shape,'b', b[0].shape,'a', a[0].shape)
        print( a[0] )
        for h in range(1,len(hidden)):
            print( 'layer ' + str(h) + ':', 'z', z[h].shape, 'w', w[h].shape, 'b', b[h].shape, 'a', a[h-1].shape)
            z[h] = w[h] * a[h-1] + b[h]
            a[h] = Logistic( z[h] )
        
        #slope,delta = backward_propagation( )
        derivative_b = []
        derivative_w = []
        derivative_b.append( (a[-1] - d ) )
        derivative_w.append( derivative_b[-1] * a[-2].T )
        for h in range( len(hidden) - 2, -1, -1 ):
            derivative_b.append( w[h+1].multiply( a[h] * ( 1 - a[h] )) * ( a[h+1] - d ))
            derivative_w.append( derivative_b[-1] * a[h-1].T )

        slopes.append( derivative_w)
        deltas.append( derivative_b)
    w -= alpha * Mean( slopes ) # doesnt work
    b -= alpha * Mean( deltas )

    if i % 25 == 0:
        print( i, np.linalg.norm( predicted - ref) )
            

