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
