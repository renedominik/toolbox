#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import pdb_atoms as at
import sys

max_dist = 8

chains = []
chain = []
prev_chain = 'xxx'
with open( sys.argv[1] ) as f:
    for l in f:
        l = l.strip()
        if "ATOM" != l[:4] and "HETATM" != l[:6]: continue
        atom = at.PDBAtom(l)
#        print l
#        print atom.chain, atom.residue_name, atom.residue_id
        if atom.chain != prev_chain and len(chain) > 0:
            chains.append(chain)
            chain = []
        chain.append( atom )
        prev_chain = atom.chain

if len(chain) > 0:
    chains.append(chain)

#for c in chains:
    #print len(c)

contacts = dict()
    
for t in range(0,len(chains)-1):
    for i in range(t,len(chains)-1):
        for j in range( t+1,len(chains)):
            #print t,i,j
            for a1 in chains[i]:
                for a2 in chains[j]:
                    d = at.Distance( a1, a2)
                    if d > max_dist: continue
                    key = a1.chain + ':' + str(a1.residue_id) + ':' + a1.residue_name + '-' + a2.chain + ':' + str(a2.residue_id) + ':' + a2.residue_name
                    if key in contacts:
                        if d < contacts[key]:
                            contacts[key] = d
                    else:
                        contacts[key] = d




for k,v in contacts.iteritems():
    print k, v
