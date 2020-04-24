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

