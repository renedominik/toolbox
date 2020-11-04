from pymol import cmd

def set_phipsi(selection, phi=None, psi=None):
    '''
DESCRIPTION

    Set phi/psi angles for all residues in selection.

SEE ALSO

    set_phi, set_psi, set_dihedral, phi_psi, cmd.get_phipsi, DynoPlot
    '''
    for model, index in cmd.index('byca (' + selection + ')'):
        atsele = [
            'first ((%s`%d) extend 2 and name C)' % (model, index), # prev C
            'first ((%s`%d) extend 1 and name N)' % (model, index), # this N
            '(%s`%d)' % (model, index),                             # this CA
            'last ((%s`%d) extend 1 and name C)' % (model, index),  # this C
            'last ((%s`%d) extend 2 and name N)' % (model, index),  # next N
        ]
        try:
            if phi is not None:
                cmd.set_dihedral(atsele[0], atsele[1], atsele[2], atsele[3], phi)
            if psi is not None:
                cmd.set_dihedral(atsele[1], atsele[2], atsele[3], atsele[4], psi)
        except:
            print ' Error: cmd.set_dihedral failed'

def set_phi(selection, phi):
    set_phipsi(selection, phi=phi)

def set_psi(selection, psi):
    set_phipsi(selection, psi=psi)

cmd.extend('set_phipsi', set_phipsi)
cmd.extend('set_phi', set_phi)
cmd.extend('set_psi', set_psi)

# vi:expandtab:smarttab:sw=4
