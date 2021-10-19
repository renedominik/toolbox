#!/usr/bin/python3
from pyrosetta import *
import sys

if len(sys.argv) % 3 != 0:
    print( "USAGE:", sys.argv[0], "INPDB OUTPDB RESID1 PHI1 PSI1 ... " )
    print( "example:", sys.argv[0], "IN.pdb OUT.pdb 287 -64 -41 288 -64 -41 289 -64 -41")
    print( "sets three residues to helical conformation" )
    exit(1)
    
init()

name = sys.argv[1]
clean = name[:-4] + ".clean.pdb"
out = sys.argv[2]

pose = Pose()
toolbox.cleanATOM( name )
pose = pose_from_pdb( clean )

print( "nr residues: ", pose.total_residue() )

for i in range( 0, int(len(sys.argv)/3)-1 ):
    ind = int( sys.argv[3*i+3] )
    phi = float( sys.argv[3*i+4] )
    psi = float( sys.argv[3*i+5] )
    print( "residue", ind, pose.residue(ind).name() )
    pose.set_phi(ind,phi)
    pose.set_psi(ind,psi)
    
pose.dump_pdb( out )

