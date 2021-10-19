#!/usr/bin/python3

import operator


def HessaScale():
    # https://www.nature.com/articles/nature03216#Sec11
    # suppl mat 1
    a = {}
    a[ "Ala".upper() ] =   0.11
    a[ "Arg".upper() ] =   2.58
    a[ "Asn".upper() ] =   2.05
    a[ "Asp".upper() ] =   3.49
    a[ "Cys".upper() ] =  -0.13
    a[ "Gln".upper() ] =   2.36
    a[ "Glu".upper() ] =   2.68
    a[ "Gly".upper() ] =   0.74
    a[ "His".upper() ] =   2.06
    a[ "Ile".upper() ] =  -0.6
    a[ "Leu".upper() ] =  -0.55
    a[ "Lys".upper() ] =   2.71
    a[ "Met".upper() ] =  -0.1
    a[ "Phe".upper() ] =  -0.32
    a[ "Pro".upper() ] =   2.23
    a[ "Ser".upper() ] =   0.84
    a[ "Thr".upper() ] =   0.52
    a[ "Trp".upper() ] =   0.3
    a[ "Tyr".upper() ] =   0.68
    a[ "Val".upper() ] =  -0.31
    return a


pol = HessaScale()

sort = sorted( pol.items(), key=operator.itemgetter(1), reverse=True)

for k,v in sort:
    print( k,v)

    
