import numpy as np


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def Length( v):
    return np.linalg.norm(v)


def Distance( v1, v2):
    return Length( v1 - v2 )


def Angle( v1, v2):
    return np.arccos( np.clip( np.dot( v1, v2) / (Length(v1) * Length(v2)), -1.0, 1.0 )) 


def Dihedral( v1, v2, v3, v4):
#    b0 = -1.0*(v2 - v1)
    b0 = v1 - v2
    b1 = v3 - v2
    b2 = v4 - v3

#    b0xb1 = np.cross(b0, b1)
#    b1xb2 = np.cross(b2, b1)
#
#    b0xb1_x_b1xb2 = np.cross(b0xb1, b1xb2)
#
#    y = np.dot(b0xb1_x_b1xb2, b1)*(1.0/np.linalg.norm(b1))
#    x = np.dot(b0xb1, b1xb2)
#
#    return np.degrees(np.arctan2(y, x))

    # more efficient???
    
    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= np.linalg.norm(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross( b1 , v ), w)
    return np.degrees(np.arctan2(y, x))  ##  DEGREES ????  ## 





def VectorPlaneAngle( v, p1, p2, p3):
    n = np.cross( p2-p1 , p2-p3 )
    p = np.cross( n, np.cross( n,v ) )
    return Angle( p , v )



def Str( v, c=' '):
    s = ""
    for x in v:
        s += str(x) + c
    return s[:-len(c)]
