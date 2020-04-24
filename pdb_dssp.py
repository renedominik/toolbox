#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



# Procedure to extract DSSP information from PDB files with multiple
# Chains, using Python 3.5, Biopython 1.66, and DSSP (mkdssp) 2.2.1
# 2016-12-02
# John J. Ladasky Jr., Ph.D.

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import DSSP 
from Bio.PDB.PDBExceptions import PDBConstructionWarning
import warnings
import sys

import numpy as np
import matplotlib.pyplot as plt

path = sys.argv[1]

_parser = PDBParser(QUIET=True)

multiple_chains = False
with open(path, "r") as f:
    with warnings.catch_warnings():
        warnings.simplefilter("error")      # warnings become exceptions
        try:
            structure = _parser.get_structure("tmp", path)
        except PDBConstructionWarning:
            # The Model in the PDB file consists of multiple Chains.
            # Calling DSSP with the current Model will concatenate 
            # all Chains, and this is unavoidable because it's 
            # external to Python.  The DSSP result will need to be
            # truncated after the fact.
            warnings.simplefilter("ignore")
            structure = PDBParser().get_structure("tmp", path)
            multiple_chains = True
    model = next(structure.get_models())    # I always work with Model 1
    output = DSSP(model, path)              # DSSP expects a Model, why?
    if multiple_chains:
        # A DSSP object is dictionary-like, but with ordered keys.
        # The keys are nested tuples which are structured like PDB 
        # Residue identifiers.  The first element of the tuple is
        # the Chain name (typically, "A").
        chain_a = output.keys()[0][0]
        subset_keys = [k for k in output.keys() if k[0] == chain_a]
        # Now use the keys in chain "A" to truncate output.  The 
        # output object need not be a DSSP object, it just needs to
        # yield the right values when iterated below.
        output = [output[k] for k in subset_keys]

    nr, aa, hh, st, exp = [],[],[],[], []

    for n in output:
        nr.append(n[0])
        aa.append(n[1])
        exp.append(n[3])
        if n[2] == "H":
            hh.append(1.0)
        else:
            hh.append(0.0)
        if n[2] == "E":
            st.append(1.0)
        else:
            st.append(0.0)

plt.plot( nr, hh,"b")
plt.plot( nr, st, "g")
plt.plot( nr, exp, "orange")
z = np.zeros( len(nr))
plt.fill_between(nr, hh, where=hh>=z, color='blue')
#plt.show()

plt.savefig( path[:-4] + ".pdf")
