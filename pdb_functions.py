import numpy as np
import Bio.PDB
import vector_functions as vf



def position( line):
    return np.array( [ float(line[30:38]) , float(line[38:46]) , float(line[46:54]) ] )

def write_position( line, pos):
    l = line[:30] + '{:8.3f}{:8.3f}{:8.3f}'.format(pos[0],pos[1],pos[2]) + line[54:]
    return l
    

def resid( line):
    return int( line[22:26].strip() )

def residue_id( line):
    return resid( line )

def residue_name( line ):
    return line[17:20]

def atom_name( line):
    return line[12:16].strip() 

def atom_id( line):
    return int( line[6:11].strip() )
 
def chain( line ):
    return line[21]

def occupancy( line):
    return float( line[54:60].strip() )

def bfactor( line):
    return float( line[60:66] )


def single_letter( residue ):
    if residue.upper() == "Gly".upper(): return "G"                                                               
    if residue.upper() == "Ala".upper(): return "A"                                                               
    if residue.upper() == "Leu".upper(): return "L"                                                               
    if residue.upper() == "Met".upper(): return "M"                                                               
    if residue.upper() == "Phe".upper(): return "F"                                                               
    if residue.upper() == "Trp".upper(): return "W"                                                               
    if residue.upper() == "Lys".upper(): return "K"                                                               
    if residue.upper() == "Gln".upper(): return "Q"                                                               
    if residue.upper() == "Glu".upper(): return "E"                                                               
    if residue.upper() == "Ser".upper(): return "S"                                               
    if residue.upper() == "Pro".upper(): return "P"                           
    if residue.upper() == "Val".upper(): return "V"                           
    if residue.upper() == "Ile".upper(): return "I"                   
    if residue.upper() == "Cys".upper(): return "C"                
    if residue.upper() == "Tyr".upper(): return "Y"                
    if residue.upper() == "His".upper(): return "H"                
    if residue.upper() == "Hsd".upper(): return "H"                
    if residue.upper() == "Arg".upper(): return "R"                
    if residue.upper() == "Asn".upper(): return "N"                   
    if residue.upper() == "Asp".upper(): return "D"     
    if residue.upper() == "Thr".upper(): return "T"   
    return "X"

def CooFromPDB( name, chain = ''):
    coo = []
    with open( name) as r:
        for l in r:
            if l[:4] == "ATOM" or l[:6] == 'HETATM':
                #if (chain != '' and l[21] != chain) or l[12:16].strip() != 'CA': continue
                if chain != '' and l[21] != chain: continue
                coo.append( position(l) )
    return np.array(coo)

def WriteCooToPDB( infile, coo, outfile ):
    with open( outfile, 'w') as w:
        count = 0
        with open( infile) as r:
            for l in r:
                if l[:4] == "ATOM" or l[:6] == 'HETATM':
                    w.write( write_position( l, coo[count]))
                    count += 1
                else:
                    w.write( l )
