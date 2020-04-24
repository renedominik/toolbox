#!/home/perezheg/miniconda3/bin/python
import argparse
import numpy as np
import mdtraj as md
from matplotlib import pyplot as plt



from actor_utils import get_fragments, \
ctc_freq_reporter_by_residue_neighborhood, \
    xtcs2ctcs, rangeexpand, unique_pairlist_by_tuple_hashing, interactive_fragment_picker_by_resSeq, \
    in_what_fragment, mycolors, bonded_neighborlist_from_top

parser = argparse.ArgumentParser(description='Small residue-residue contact analysis tool, initially developed for the '
                                             'receptor-G-protein complex. The provides the residue indices')

parser.add_argument('topology',    type=str,help='Topology file')
parser.add_argument('trajectories',type=str,help='trajectory file(s)', nargs='+')
parser.add_argument('resSeq_idxs',type=str,help='the resSeq idxs of interest (in VMD these are called "resid"). Can be in a format 1,2-6,10,20-25')
parser.add_argument("--ctc_cutoff_Ang",type=float, help="The cutoff distance between two residues for them to be considered in contact. Default is 3 Angstrom.", default=3)
parser.add_argument("--stride", type=int, help="Stride down the input trajectoy files by this factor. Default is 1.", default=1)
parser.add_argument("--n_ctcs", type=int, help="Only the first n_ctcs most-frequent contacts will be written to the ouput. Default is 5.", default=5)
parser.add_argument("--n_nearest", type=int, help="Ignore this many nearest neighbors when computing neighbor lists. 'Near' means 'connected by this many bonds'. Default is 4.", default=4)
parser.add_argument("--chunksize_in_frames", type=int, help="Trajectories are read in chunks of this size (helps with big files and memory problems). Default is 10000", default=10000)
parser.add_argument("--nlist_cutoff_Ang", type=float, help="Cutoff for the initial neighborlist. Only atoms that are within this distance in the original reference "
                                                          "(the topology file) are considered potential neighbors of the residues in resSeq_idxs, s.t. "
                                                          "non-necessary distances (e.g. between N-terminus and G-protein) are not even computed. "
                                                          "Default is 15 Angstrom.", default=30)


parser.add_argument('--fragments',    dest='fragmentify', action='store_true', help="Auto-detect fragments (i.e. breaks) in the peptide-chain. Default is true.")
parser.add_argument('--no-fragments', dest='fragmentify', action='store_false')
parser.set_defaults(fragmentify=True)

parser.add_argument('--order',    dest='order', action='store_true', help="Order the resSeq_idxs list. Defaut is True")
parser.add_argument('--no-order', dest='order', action='store_false')
parser.set_defaults(order=True)

parser.add_argument('--ask_fragment',    dest='ask', action='store_true', help="Interactively ask for fragment assignemnt when input matches more than one resSeq")
parser.add_argument('--no-ask_fragment', dest='ask', action='store_false')
parser.set_defaults(ask=True)
parser.add_argument('--output_npy', type=str, help="Name of the output.npy file for storing this runs' results", default='output.npy')

a  = parser.parse_args()

xtcs = sorted(a.trajectories)
print("Will compute contact frequencies for the files:\n  %s\n with a stride of %u frames.\n"%("\n  ".join(xtcs),a.stride))

refgeom = md.load(a.topology)
if a.fragmentify:
    fragments = get_fragments(refgeom.top)
else:
    raise NotImplementedError("This feature is not yet implemented")

resSeq_idxs = rangeexpand(a.resSeq_idxs)
if a.order:
    resSeq_idxs = sorted(resSeq_idxs)

print("\nWill compute neighborhoods for the residues with resid")
print("%s"%resSeq_idxs)
print("excluding %u nearest neighbors\n"%a.n_nearest)


resSeq2residxs, _ = interactive_fragment_picker_by_resSeq(resSeq_idxs, fragments,refgeom.top,
                                                         pick_first_fragment_by_default=~a.ask,
                                                         )

print('%10s  %6s  %7s  %10s'%tuple(("residue  residx    fragment  input_resSeq".split())))
for key, val in resSeq2residxs.items():
    print('%10s  %6u  %7u  %10u'%(refgeom.top.residue(val), val, in_what_fragment(key, fragments), key))

# Create a neighborlist
nl = bonded_neighborlist_from_top(refgeom.top, n=a.n_nearest)
print(a.n_nearest)
for ii, inl in enumerate(nl):
    print(ii, inl)
ctc_idxs = np.vstack([[np.sort([val,ii]) for ii in range(refgeom.top.n_residues) if ii not in nl[val] and ii!=val   ] for val in resSeq2residxs.values()])


print("\nPre-computing likely neighborhoods by reducing the neighbor-list to %u Angstrom in the reference geom %s..."%(a.nlist_cutoff_Ang,a.topology),end="",flush=True)
ctcs, ctc_idxs = md.compute_contacts(refgeom, np.vstack(ctc_idxs))
print("done!")

ctc_idxs_small = np.argwhere(ctcs[0]<a.nlist_cutoff_Ang/10).squeeze()
_, ctc_idxs_small = md.compute_contacts(refgeom, ctc_idxs[ctc_idxs_small])
ctc_idxs_small = unique_pairlist_by_tuple_hashing(ctc_idxs_small)

print("From %u potential distances, the neighborhoods have been reduced to only %u potential contacts.\nIf this "
      "number is still too high (i.e. the computation is too slow), consider using a smaller nlist_cutoff_Ang "%(len(ctc_idxs), len(ctc_idxs_small)))

actcs, time_array = xtcs2ctcs(xtcs, refgeom.top, ctc_idxs_small, stride=a.stride, chunksize=a.chunksize_in_frames, return_time=True)

ctcs_mean = np.mean(actcs < a.ctc_cutoff_Ang / 10, 0)

final_look = ctc_freq_reporter_by_residue_neighborhood(ctcs_mean, resSeq2residxs,
                                                       fragments, ctc_idxs_small,
                                                       refgeom.top,
                                                       n_ctcs=a.n_ctcs)
#print("Will take a look at:")
split_by_neighborhood = True
if not split_by_neighborhood:
    myfig, myax = plt.subplots(len(final_look), 1, sharex=True, sharey=True)

    for ii, oo in enumerate(final_look):
        pair = ctc_idxs_small[oo]
        print([refgeom.top.residue(jj) for jj in pair])
        plt.sca(myax[ii])
        plt.plot(time_array/1e3, actcs[:, oo],
                 label='%s-%s (%u)' % (refgeom.top.residue(pair[0]), refgeom.top.residue(pair[1]), ctcs_mean[oo] * 100))
        plt.legend()
        # plt.yscale('log')
        plt.ylabel('d / nm')
        plt.ylim([0, 1])
        iax = plt.gca()
        iax.axhline(a.ctc_cutoff_Ang / 10, color='r')
    iax.set_xlabel('t / ns')
    plt.show()
else:
    print("The following files have been created")
    panelheight=3
    xvec = np.arange(np.max([len(val) for val in final_look.values()]))
    n_cols=np.min((4, len(resSeq2residxs)))
    n_rows = np.ceil(len(resSeq2residxs)/n_cols).astype(int)
    panelsize=4
    panelsize2font=3.5
    histofig, histoax = plt.subplots(n_rows,n_cols, sharex=True, sharey=True, figsize=(n_cols*panelsize*2, n_rows*panelsize))
    for jax, residx in zip(histoax.flatten(), resSeq2residxs.values()):# in np.unique([ctc_idxs_small[ii] for ii in final_look]):
        #toplot=[kk for kk in final_look if residx in ctc_idxs_small[kk]]
        toplot=final_look[residx]
        myfig, myax = plt.subplots(len(toplot), 1, sharex=True, sharey=True,
                                   figsize=(10,len(toplot)*panelheight))
        myax=np.array(myax,ndmin=1)
        anchor_seg = in_what_fragment(residx,fragments)
        res_and_fragment_str ='%s@seg%u'%(refgeom.top.residue(residx), anchor_seg)
        myax[0].set_title(res_and_fragment_str)
        xlabels = []
        jax.set_title("Contact frequency @%2.1f $\AA$\n%u nearest bonded neighbors excluded"%(a.ctc_cutoff_Ang,a.n_nearest))
        for ii, oo in enumerate(toplot):
            idx1,idx2 = ctc_idxs_small[oo]
            s1 = in_what_fragment(idx1, fragments)
            s2 = in_what_fragment(idx2, fragments)
            if residx==idx1:
                partner, partnerseg=idx2, s2
            else:
                partner, partnerseg=idx1, s1
            #print([refgeom.top.residue(jj) for jj in pair])
            plt.sca(myax[ii])
            plt.plot(time_array / 1e3, actcs[:, oo],
                     label='%s@seg%u-%s@seg%u (%u%%)' % (
                     refgeom.top.residue(idx1),s1,
                     refgeom.top.residue(idx2),s2,
                     ctcs_mean[oo] * 100))
            plt.legend()
            # plt.yscale('log')
            plt.ylabel('d / nm')
            plt.ylim([0, 1])
            iax = plt.gca()
            iax.axhline(a.ctc_cutoff_Ang / 10, color='r')
            xlabels.append('%s@seg%u'%(refgeom.top.residue(partner), partnerseg))

        # TODO re-use code from mdas.visualize represent vicinities
        patches = jax.bar(xvec[:len(toplot)], ctcs_mean[toplot],
                #label=res_and_fragment_str,
                         width=.25)
        jax.plot(-1,-1,'o', color=mycolors[anchor_seg], label=res_and_fragment_str)
        for ix, iy, ilab, ipatch in zip(xvec, ctcs_mean[toplot], xlabels, patches.get_children()):
            iy += .01
            if iy>.65:
                iy=.65
            jax.text(ix, iy, ilab,
                     va='bottom',
                     ha='left',
                     rotation=45,
                     fontsize=panelsize * panelsize2font,
                     backgroundcolor="white"
                     )
            iseg = ilab.split('@')[1].replace("seg","")
            assert all([ii.isnumeric() for ii in iseg])
            iseg = int(iseg)
            icol = mycolors[iseg]
            ipatch.set_color(icol)

            """
            isegs.append(iseg[0])
                
            
            isegs = _np.unique(isegs)
            _empty_legend(iax,
                          [binary_ctcs2flare_kwargs["fragment_names"][ii] for ii in isegs],
                          [_mycolors[ii] for ii in isegs],
                          'o' * len(isegs),
                          loc='upper right',
                          fontsize=panelsize * panelsize2font,
                          )
            """
        jax.set_ylim([0, 1])
        jax.set_xlim([-.5, len(toplot) - .5])
        jax.set_xticks([])
        jax.set_yticks([.25, .50, .75, 1])
        #jax.set_yticklabels([])
        [jax.axhline(ii, color="k", linestyle="--", zorder=-1) for ii in [.25, .50, .75]]
        jax.legend(fontsize=panelsize * panelsize2font)
        #plt.show()
        #plt.close()

        
        iax.set_xlabel('t / ns')
        myfig.tight_layout(h_pad=0,w_pad=0,pad=0)
        fname = 'neighborhood.%s.time_resolved.pdf'%res_and_fragment_str
        plt.savefig(fname,bbox_inches="tight")
        plt.close(myfig)
        print(fname)
        #plt.show()

    histofig.tight_layout(h_pad=2, w_pad=0, pad=0)
    fname = "neighborhoods_overall.pdf"
    histofig.savefig(fname)
    print(fname)

fname = a.output_npy
if not fname.endswith(".npy"):
    fname+=".npy"
np.save(fname,{"args":a,
                      "ctc_idxs":ctc_idxs_small, 
                      'ctcs':actcs, 
                      'time_array':time_array})
print(fname)
