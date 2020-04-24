import numpy as _np
import mdtraj as _md
from scipy.spatial.distance import pdist
from matplotlib import pyplot as _plt
"""
fragment 0 with 203 AAs GLU30-LYS232 NT-TM5
fragment 1 with  78 AAs PHE264-CYSP341 TM6-CT
fragment 2 with 379 AAs CYSP2-LEU394 Gprot1 NT(Gα)-S3(Gα)α-helical domain(Gα)-CT(Gα)
fragment 3 with 339 AAs SER2-ASN340 Gprot3 NT(Gβ)-CT(Gβ)
fragment 4 with  67 AAs ALA2-CYSG68 Gprot4 NT(Gγ)-CT(Gγ)
fragment 5 with   2 AAs P0G395-GDP396 ligands
"""

fragment_names =  [
"NT-TM5",
"TM6-CT",
"NT(Gα)-CT(Gα)",
"NT(Gβ)-CT(Gβ)",
"NT(Gγ)-CT(Gγ)",
"ligands",
]
fragment_names_short =  [
"B2AR",
"B2AR",
"Gα-ahlx",
"Gβ",
"Gγ",
"LIG",
]

fragment_names_B2AR = [
    'TM1', 'ICL1',
    "TM2", 'ECL1',
    'TM3', 'ICL2',
    'TM4', 'ECL2',
    'TM5', 'ICL3',
    'TM6', 'ECL3',
    'TM7', 'TM78',
    'H8'
]


def identify_boolean_blocks_in_sequence(binary_vector,
                                        minimum_block_length=1,
                                        max_block_interruption=0,
                                        verbose=False,
                                        names=["block","break"],
                                        ):
    blocks = []
    icounter = []
    ibreak = []

    for ii, ihx in enumerate(binary_vector):
        if ihx:
            icounter.append(ii)
            ibreak = []
        else:
            ibreak.append(ii)
        if verbose:
            print(ii, ihx, end=' ')
            if len(icounter) != 0:
                print('%u-%u' % (icounter[0], icounter[-1]), end=' ')
            else:
                print(icounter, end=' ')
            if len(ibreak) != 0:
                print('%u-%u' % (ibreak[0], ibreak[-1]))
            else:
                print(ibreak)

        if len(ibreak) > max_block_interruption:
            if len(icounter) > (minimum_block_length):
                if verbose:
                     print(names[0], icounter[0], icounter[-1])
                     print(names[1], ibreak[0], ibreak[-1])
                blocks.append(icounter)
                ibreak = []
            icounter = []

        # Catch the last break:
    if len(icounter) > minimum_block_length:
        if verbose:
            print(names[0], icounter[0], icounter[-1])
            try:
                print(names[1], ibreak[0], ibreak[-1])
            except IndexError:
                pass

        blocks.append(icounter)

    blocks = [_np.arange(ihx[0],ihx[-1]+1) for ihx in blocks]

    if _np.sum(binary_vector[:_np.ceil(max_block_interruption).astype(int)])>0:
        blocks[0]=_np.arange(0, blocks[0][-1]+1)

    return blocks

def identify_long_helices(geom, min_turns=5, aa_per_turn=3.6,
                          verbose=False, plot=False):



    ss_str = _md.compute_dssp(geom)[0]
    ss_vec = _np.zeros(len(ss_str), dtype=int)
    ss_vec[ss_str == 'H'] = 1

    helices = identify_boolean_blocks_in_sequence(ss_vec,
                                                  min_turns*aa_per_turn,
                                                  aa_per_turn,
                                                  verbose=verbose,
                                                  names=["hlx","brk"])
    if plot:
        _plt.figure()
        _plt.figure(figsize=(20, 5))
        _plt.plot(ss_vec, marker='.')
        iax = _plt.gca()
        xticks = _np.arange(geom.n_residues, step=15)
        iax.set_xticks(xticks)
        iax.set_xticklabels([geom.top.residue(ii).resSeq for ii in xticks])
        #iax.set_xticklabels([ii for ii in xticks])
        for ihx in helices:
            iax.axvspan(ihx[0]-.5, ihx[-1]+.5, alpha=.25)

        return helices, _plt.gca()
    else:
        return helices


def find_B_residues_in_A_using_fragment_info(
        fragmentsB,
        topB,
        fragmentsA,
        topA,
        fragA_to_fragB_dict):
    residxB_to_residxA_dict = {}

    for ii, ifragA in enumerate(fragmentsA):
        idx_fragB = fragA_to_fragB_dict[ii]
        ifragB = fragmentsB[idx_fragB]
        ifragB_resSeqs = _np.array([topB.residue(ii).resSeq for ii in ifragB])
        for residx in ifragA:
            residue_A = topA.residue(residx)
            match = _np.argwhere(ifragB_resSeqs == residue_A.resSeq).squeeze()
            # print(match)
            try:
                equivB_residue = topB.residue(ifragB[match])
            except TypeError:
                pass

            if str(equivB_residue) == str(residue_A):
                residx_B = equivB_residue.index
                residxB_to_residxA_dict[residx_B] = residue_A.index
                """
                if residue_A.n_atoms!=equivB_residue.n_atoms:
                    for aa in residue_A.atoms:
                        print(aa)
                    print()
                    for aa in equivB_residue.atoms:
                        print(aa)
                    raise
                """

        #if len(fr) == len(ft) != 0:
            #common_frags_ref_residxs.append(_np.array(fr))
            #common_frags_traj_residxs.append(_np.array(ft))
        # print()
    return residxB_to_residxA_dict

def _print_frag(ii, top,iseg,**print_kwargs):
    istr="fragment %u with %3u AAs %s(%u)-%s(%u)"%(ii, len(iseg),
                                                            top.residue(iseg[0]),
                                                            top.residue(iseg[0]).index,
                                                            top.residue(iseg[-1]),
                                                            top.residue(iseg[-1]).index)
    print(istr,**print_kwargs)

def get_fragments(top,
                  fragment_breaker_fullresname=None,
                              atoms=False,
                  join_fragments=None,
                  verbose=True,
                  auto_fragment_names=True,
                  frag_breaker_to_pick_idx=None,
                  method='resSeq'):
    r"""

    :param top:
    :param fragment_breaker_fullresname:
    :param atoms:
    :param join_fragments:
    :param verbose:
    :param method: either resSeq or bonds
    :return:
    """
    fragnames=None
    if auto_fragment_names:
        fragnames=fragment_names
    old = top.residue(0).resSeq
    if method=='resSeq':
        fragments = [[]]
        for ii, rr in enumerate(top.residues):
            delta = _np.abs(rr.resSeq - old)
            #print(delta, ii, rr, end=" ")
            if delta<=1:
                #print("appending")
                fragments[-1].append(ii)
            else:
                #print("new")
                fragments.append([ii])
            old = rr.resSeq
    elif method=='bonds':
        from msmtools.estimation import connected_sets as _connected_sets
        residue_bond_matrix = _np.zeros((top.n_residues, top.n_residues))
        for ibond in list(top.bonds):
            r1, r2 = ibond.atom1.residue.index, ibond.atom2.residue.index
            residue_bond_matrix[r1, r2] = 1
            residue_bond_matrix[r2, r1] = 1
        fragments = _connected_sets(residue_bond_matrix)
        fragments = [fragments[ii] for ii in _np.argsort([fr[0] for fr in fragments])]
    if verbose:
        print("Auto-detected fragments")
        for ii, iseg in enumerate(fragments):
            _print_frag(ii, top, iseg)


    if join_fragments is not None:
        assert len(join_fragments)>0
        assert all([len(ijoin)>1 for ijoin in join_fragments])
        for pair in _np.vstack(_np.triu_indices(len(join_fragments), k=1)).T:
            frag_pair = [join_fragments[pp] for pp in pair]
            for ifrag in frag_pair:
                assert len(ifrag)==len(_np.unique(ifrag)), "bad fragment %s"%ifrag
            assert len(_np.intersect1d(*frag_pair))==0, "Some fragment groups contain share elements %s"%(frag_pair)
        #for

    if fragment_breaker_fullresname is not None:
        if isinstance(fragment_breaker_fullresname,str):
            fragment_breaker_fullresname=[fragment_breaker_fullresname]
        for breaker in fragment_breaker_fullresname:
            idx = [rr.index for rr in top.residues if str(rr)==breaker]
            if len(idx)>0:
                if len(idx)==1:
                    idx = idx[0]
                elif len(idx)>1:
                    print("The fragment breaker %s appears in different places:"%breaker)
                    for ii, jidx in enumerate(idx):
                        print(ii,":",jidx, in_what_fragment(jidx,fragments, fragment_names=fragnames))
                    if frag_breaker_to_pick_idx is None:
                        idx2pick = int(input("Which index should I use (%s)?\n"%_np.arange(len(idx))))
                        idx=idx[idx2pick]
                    elif isinstance(frag_breaker_to_pick_idx,int):
                        idx=idx[frag_breaker_to_pick_idx]
                    else:
                        raise NotImplementedError
                ifrag = in_what_fragment(idx, fragments)
                # print('%s (index %s) found in %s %s' % (breaker, idx, ifrag, fragments[ifrag]))
                idx_split = _np.argwhere(idx == _np.array(fragments[ifrag])).squeeze()
                subfrags = [fragments[ifrag][:idx_split], fragments[ifrag][idx_split:]]
                # print("now breaking up into", subfrags)
                fragments = fragments[:ifrag] + subfrags + fragments[ifrag + 1:]

                print("New fragments after breaker %s:"%breaker)
                for ii, ifrag in enumerate(fragments):
                    _print_frag(ii, top, ifrag)
                print()

            elif len(idx)==0:
                print("The fragment breaker %s appears nowhere. Check input!" % breaker)
                #raise ValueError
            else:
                raise ValueError(idx)




    if not atoms:
        return fragments
    else:
        return [_np.hstack([[aa.index for aa in top.residue(ii).atoms] for ii in iseg]) for iseg in fragments]



def in_what_fragment(residx,
                    list_of_nonoverlapping_lists_of_residxs,
                    fragment_names=None):
    if fragment_names is not None:
        assert len(fragment_names)==len(list_of_nonoverlapping_lists_of_residxs)
    for ii, ilist in enumerate(list_of_nonoverlapping_lists_of_residxs):
        if residx in ilist:
            if fragment_names is None:
                return ii
            else:
                return fragment_names[ii]


# from https://www.rosettacode.org/wiki/Range_expansion#Python
def rangeexpand(txt):
    lst = []
    for r in txt.split(','):
        if '-' in r[1:]:
            r0, r1 = r[1:].split('-', 1)
            lst += range(int(r[0] + r0), int(r1) + 1)
        else:
            lst.append(int(r))
    return lst

def re_warp_idxs(lengths):
    """Return iterable with the indexes to reshape a vector
    in the shapes specified in in lengths

    Parameters
    ----------

    lengths : int or iterable of integers
        Lengths of the individual elements of the returned array. If only one int is parsed, all lengths will
        be that int

    Returns
    -------
    warped: list
    """

    idxs_out = []
    idxi = 0
    for ll in lengths:
        idxs_out.append(_np.arange(idxi, idxi + ll))
        idxi += ll
    return idxs_out

def in_what_N_fragments(idxs, fragments):
    return _np.argwhere([_np.in1d(idxs, iseg).sum() for ii, iseg in enumerate(fragments)]).squeeze()

def unique_pairlist_by_tuple_hashing(ilist, return_idxs=False):
    idxs_out = []
    ilist_out = []
    seen = []
    for ii, pair in enumerate(ilist):
        ih = hash(tuple(pair))
        if ih not in seen:
            ilist_out.append(pair)
            idxs_out.append(ii)
            seen.append(ih)
    if not return_idxs:
        return ilist_out
    else:
        return idxs_out

def interactive_fragment_picker_by_resSeq(resSeq_idxs, fragments, top, pick_first_fragment_by_default=False):
    resSeq2residxs = {}
    resSeq2segidxs = {}
    last_answer = 0
    for key in resSeq_idxs:
        cands = [rr.index for rr in top.residues if rr.resSeq == key]
        # print(key)
        cand_fragments = in_what_N_fragments(cands, fragments)
        if len(cands) == 0:
            print("No residue found with resSeq %s"%key)
        else:
            if len(cands) == 1:
                cands = cands[0]
                answer = cand_fragments
                # print(key,refgeom.top.residue(cands[0]), cand_fragments)
            elif len(cands) > 1:
                print("Ambivalent definition for resSeq %s" % key)
                for cc, ss in zip(cands, cand_fragments):
                    print(top.residue(cc), 'in fragment ', ss, "with index", cc)
                if not pick_first_fragment_by_default:
                    answer = input(
                        "input one fragment idx (out of %s) and press enter. Leave empty and hit enter to repeat last option [%s]\n" % (cand_fragments, last_answer))
                    if len(answer) == 0:
                        answer = last_answer
                    try:
                        answer = int(answer)
                    except:
                        print("Your answer has to be an integer in the of the fragment list %s" % cand_fragments)
                        raise Exception
                    assert answer in cand_fragments, (
                                "Your answer has to be an integer in the of the fragment list %s" % cand_fragments)
                    cands = cands[_np.argwhere([answer == ii for ii in cand_fragments]).squeeze()]
                    last_answer = answer
                else:
                    cands = cands[1]
                    answer = cand_fragments[1]
                    print("Automatically picked fragment %u"%answer)
                # print(refgeom.top.residue(cands))
                print()

            resSeq2residxs[key] = cands
            resSeq2segidxs[key] = answer

    return resSeq2residxs, resSeq2segidxs

mycolors=[
         'lightblue',
         'lightgreen',
         'salmon',
         'lightgray',
    ]
mycolors=[
         'magenta',
         'yellow',
         'lime',
         'maroon',
         'navy',
         'olive',
         'orange',
         'purple',
         'teal',
]


def ctc_freq_reporter_by_residue_neighborhood(ctcs_mean, resSeq2residxs, fragments, ctc_residxs_pairs, top,
                                              n_ctcs=5, select_by_resSeq=None,
                                              silent=False
                                              ):
    order = _np.argsort(ctcs_mean)[::-1]
    assert len(ctcs_mean)==len(ctc_residxs_pairs)
    final_look = {}
    if select_by_resSeq is None:
        select_by_resSeq=list(resSeq2residxs.keys())
    elif isinstance(select_by_resSeq, int):
        select_by_resSeq=[select_by_resSeq]
    for key, val in resSeq2residxs.items():
        if key in select_by_resSeq:
            order_mask = _np.array([ii for ii in order if val in ctc_residxs_pairs[ii]])
            print("#idx    Freq  contact             fragmentA-segB residxA   residxB   ctc_idx")

            isum=0
            for ii, oo in enumerate(order_mask[:n_ctcs]):
                pair = ctc_residxs_pairs[oo]
                if pair[0]!=val and pair[1]==val:
                    pair=pair[::-1]
                elif pair[0]==val and pair[1]!=val:
                    pass
                else:
                    print(pair)
                    raise Exception
                idx1 = pair[0]
                idx2 = pair[1]
                s1 = in_what_fragment(idx1, fragments)
                s2 = in_what_fragment(idx2, fragments)
                imean = ctcs_mean[oo]
                isum += imean
                print("%-6s %3.2f %8s-%-8s    %5u-%-5u %7u %7u %7u %3.2f" % ('%u:'%(ii+1), imean, top.residue(idx1), top.residue(idx2), s1, s2, idx1, idx2, oo, isum))

            if not silent:
                try:
                    answer = input("How many do you want to keep?\n")
                except KeyboardInterrupt:
                    break
                if len(answer) == 0:
                    pass
                else:
                    answer = _np.arange(_np.min((int(answer),n_ctcs)))
                    final_look[val] = order_mask[answer]
            else:
                answer=n_ctcs
                final_look[val]= order_mask[answer]

    # TODO think about what's best to return here
    return final_look
    # These were moved from the method to the API
    final_look = _np.unique(_np.hstack(final_look))
    final_look = final_look[_np.argsort(ctcs_mean[final_look])][::-1]
    return final_look

def xtcs2ctcs(xtcs, top, ctc_residxs_pairs, stride=1,consolidate=True,
              chunksize=1000, return_time=False, c=True):
    ctcs = []
    print()
    times = []
    inform = lambda ixtc, ii, running_f : print("Analysing %20s in chunks of "
                                                "%3u frames. chunks %4u frames %8u" %
                                                (ixtc, chunksize, ii, running_f), end="\r", flush=True)
    for ii, ixtc in enumerate(xtcs):
        ictcs = []
        running_f = 0
        inform(ixtc, 0, running_f)
        itime = []
        for jj, igeom in enumerate(_md.iterload(ixtc, top=top, stride=stride,
                                                chunk=_np.round(chunksize/stride)
                                   )):
            running_f += igeom.n_frames
            inform(ixtc, jj, running_f)
            itime.append(igeom.time)
            ictcs.append(_md.compute_contacts(igeom, ctc_residxs_pairs)[0])
            #if jj==10:
            #    break

        times.append(_np.hstack(itime))
        ictcs = _np.vstack(ictcs)
        #print("\n", ii, ictcs.shape, "shape ictcs")
        ctcs.append(ictcs)
        print()

    if consolidate:
        try:
            actcs = _np.vstack(ctcs)
            times = _np.hstack(times)
        except ValueError as e:
            print(e)
            print([_np.shape(ic) for ic in ctcs])
            raise
    else:
        actcs = ctcs
        times = times

    if not return_time:
        return actcs
    else:
        return actcs, times

def exclude_neighbors_from_residx_pairlist(pairlist, top, n_exclude,
                                           return_excluded_idxs=False,
                                           ):
    fragments = get_fragments(top, verbose=False)
    fragment_list = [in_what_fragment(ii, fragments) for ii in range(top.n_residues)]
    idx2keep_anyway = _np.array([idx for idx, pair in enumerate(pairlist) if
                                 fragment_list[pair[0]] != fragment_list[pair[1]]])

    # Exclude nearest neighbors by resSeq allowing for same resSeq in different fragments
    idxs2exclude = _np.array([idx for idx, pair in enumerate(pairlist) if
                              _np.abs(_np.diff([top.residue(ii).resSeq for ii in pair])) <= n_exclude and
                              idx not in idx2keep_anyway])

    if not return_excluded_idxs:
        return [pair for ii, pair in enumerate(pairlist) if ii not in idxs2exclude]
    else:
        return idxs2exclude

def exclude_same_fragments_from_residx_pairlist(pairlist, top,fragments=None,
                                                return_excluded_idxs=False):
    if fragments is None:
        fragments = get_fragments(top)
    idxs2exclude = [idx for idx, pair  in enumerate(pairlist) if
                    _np.diff([in_what_fragment(ii, fragments) for ii in pair]) == 0]

    #print("Idxs of same_fragments")
    #print(idxs2exclude)

    if not return_excluded_idxs:
        return [pair for ii, pair in enumerate(pairlist) if ii not in idxs2exclude]
    else:
        return idxs2exclude

def my_RMSD(geom, ref, atom_indices=None,
            ref_atom_indices=None,
            weights='masses',
            check_same_atoms=False):
    if atom_indices is None:
        atom_indices = _np.arange(geom.n_atoms)

    if ref_atom_indices is None:
        ref_atom_indices=atom_indices

    if check_same_atoms:
        for aa_idx_geom, aa_idx_ref in zip(atom_indices,
                                           ref_atom_indices):
            err_msg = 'geom %s is not equal ref %s (idxs %u vs %u)'%(
                    str(geom.top.atom(aa_idx_geom)), str(ref.top.atom(aa_idx_ref)),
                    aa_idx_geom, aa_idx_ref)

            assert str(geom.top.atom(aa_idx_geom)) == str(ref.top.atom(aa_idx_ref)), err_msg
    if weights != 'masses':
        raise NotImplementedError
    masses = _np.hstack([[aa.element.mass for aa in rr.atoms] for rr in geom.top.residues])
    masses = masses[atom_indices]
    assert len(masses)==len(atom_indices), masses

    return _np.sqrt(_np.average(_np.linalg.norm(geom.xyz[:,atom_indices,:]-ref.xyz[0,ref_atom_indices,:], axis=2)**2,
                              axis=1, weights=masses))

def xtcs2contactpairs_auto(xtcs, top, cutoff_in_Ang,
                           stride=1,
                           chunksize=500,
                           exclude_nearest_neighbors=2,
                           fragments=True):

    if isinstance(top,str):
        top = _md.load(top).top


    ctc_mins, ctc_pairs = xtcs2mindists(xtcs, top, chunksize=chunksize, stride=stride)

    ctc_pairs_cutoff = select_ctcmins_by_cutoff(ctc_mins, ctc_pairs,
                                                cutoff_in_Ang)
    #print("Before neighbors")
    #for pair in ctc_pairs_cutoff:
    #    print(pair)
    #print()
    ctc_pairs_cutoff = exclude_neighbors_from_residx_pairlist(ctc_pairs_cutoff, top, exclude_nearest_neighbors,
                                                              )

    #print("After neighbors before fragments")
    #for pair in ctc_pairs_cutoff:
    #    print(pair)
    #print()

    if fragments:
        ctc_pairs_cutoff = exclude_same_fragments_from_residx_pairlist(ctc_pairs_cutoff, top)

    #print("After fragments")
    #for pair in ctc_pairs_cutoff:
    #    print(pair)
    #print()

    ctc_pairs_cutoff = _np.array(ctc_pairs_cutoff)[_np.argsort([_np.ravel_multi_index(rr, (top.n_residues, top.n_residues)) for rr in ctc_pairs_cutoff])]

    return ctc_pairs_cutoff

def xtcs2mindists(xtcs, top,
                  stride=1,
                  chunksize=1000, **COM_kwargs):

    #TODO avoid code repetition with xtcs2ctcs
    inform = lambda ixtc, ii, running_f: print(
        "Analysing %20s in chunks of %3u frames. chunks read %4u. frames read %8u" % (ixtc, chunksize, ii, running_f),
        end="\r", flush=True)

    ctc_mins, ctc_pairs = [],[]
    for ii, ixtc in enumerate(xtcs):
        running_f = 0
        inform(ixtc, 0, running_f)
        ires = {}
        for jj, igeom in enumerate(_md.iterload(ixtc, top=top, stride=stride, chunk=_np.round(chunksize/stride))):
            running_f += igeom.n_frames
            inform(ixtc, jj, running_f)
            mins, pairs, pair_idxs = igeom2mindist_COMdist_truncation(igeom, **COM_kwargs)
            for imin, ipair, idx in zip(mins, pairs, pair_idxs):
                try:
                    ires[idx]["val"] = _np.min((ires[idx]["val"], imin))
                except:
                    ires[idx] = {"val":imin,
                                 "pair":ipair}

            #if jj==5:
            #   break

        pair_idxs = sorted(ires.keys())
        ctc_mins.append( _np.array([ires[idx]["val"] for idx in pair_idxs]))
        ctc_pairs.append(_np.array([ires[idx]["pair"] for idx in pair_idxs]))
    print()
    return ctc_mins, ctc_pairs

def select_ctcmins_by_cutoff(ctc_mins, ctc_idxs, cutoff_in_Ang):
    ctc_pairs = []
    highest_res_idx = _np.max([_np.max(ilist) for ilist in ctc_idxs])
    matrix_of_already_appended = _np.zeros((highest_res_idx+1, highest_res_idx+1))
    for ii, (ictc, iidxs) in enumerate(zip(ctc_mins, ctc_idxs)):
        tokeep_bool = ictc <= cutoff_in_Ang / 10
        tokeep = _np.argwhere(tokeep_bool).squeeze()
        pairs2keep = iidxs[tokeep]
        for pair in pairs2keep:
            ii,jj = pair
            # Append pair only if it hasn't been appended yet
            if not matrix_of_already_appended[ii,jj]:
                ctc_pairs.append(pair)
                matrix_of_already_appended[ii,jj]=1
                matrix_of_already_appended[jj,ii]=1

    ctc_pairs = _np.array(ctc_pairs)
    return ctc_pairs

def igeom2mindist_COMdist_truncation(igeom,
                                     res_COM_cutoff_Ang=25,
                                     ):


    COMs_xyz = geom2COMxyz(igeom)

    COMs_dist_triu = _np.array([pdist(ixyz) for ixyz in COMs_xyz])


    COMs_under_cutoff = COM_n_from_COM_dist_triu(COMs_dist_triu,
                                                 cutoff_nm=res_COM_cutoff_Ang/10)

    COMs_under_cutoff_pair_idxs = _np.argwhere(COMs_under_cutoff.sum(0) >= 1).squeeze()
    pairs = _np.vstack(_np.triu_indices(igeom.n_residues, 1)).T[COMs_under_cutoff_pair_idxs]
    try:
        ctcs, ctc_idxs_dummy = _md.compute_contacts(igeom, pairs)
    except MemoryError:
        print("\nCould not fit %u contacts for %u frames into memory"%(len(pairs), igeom.n_frames))
        raise


    assert _np.allclose(pairs, ctc_idxs_dummy)

    return ctcs.min(0), pairs, COMs_under_cutoff_pair_idxs


def COM_n_from_COM_dist_triu(COM_dist_triu,
                             cutoff_nm=2.5,
                             ):
    assert _np.ndim(COM_dist_triu)==2
    COM_dist_bool_int = (COM_dist_triu<=cutoff_nm).astype("int")
    return COM_dist_bool_int


def geom2COMxyz(igeom):
    masses = [_np.hstack([aa.element.mass for aa in rr.atoms]) for rr in igeom.top.residues]
    COMs_res_time_coords = [_np.average(igeom.xyz[:, [aa.index for aa in rr.atoms], :], axis=1, weights=rmass) for rr, rmass in
            zip(igeom.top.residues, masses)]
    COMs_time_res_coords = _np.swapaxes(_np.array(COMs_res_time_coords),0,1)
    return COMs_time_res_coords

# This is lifted from mdas, the original source shall remain there
def top2bondmatrix(top, create_standard_bonds=True):
    if len(top._bonds)==0:
        if create_standard_bonds:
            top.create_standard_bonds()
        else:
            raise ValueError("The parsed topology does not contain bonds! Aborting...")
    residue_bond_matrix = _np.zeros((top.n_residues, top.n_residues))
    for ibond in top._bonds:
        r1, r2 = ibond.atom1.residue.index, ibond.atom2.residue.index
        residue_bond_matrix[r1, r2] = 1
        residue_bond_matrix[r2, r1] = 1
    return residue_bond_matrix

def bonded_neighborlist_from_top(top, n=1):
    residue_bond_matrix = top2bondmatrix(top)
    neighbor_list = [[ii] for ii in range(residue_bond_matrix.shape[0])]
    for kk in range(n):
        for ridx, ilist in enumerate(neighbor_list):
            new_neighborlist = [ii for ii in ilist]
            #print("Iteration %u in residue %u"%(kk, ridx))
            for rn in ilist:
                row = residue_bond_matrix[rn]
                bonded = _np.argwhere(row == 1).squeeze()
                if _np.ndim(bonded)==0:
                    bonded=[bonded]
                toadd = [nn for nn in bonded if nn not in ilist and nn!=ridx]
                if len(toadd):
                    #print("neighbor %u adds new neighbor %s:"%(rn, toadd))
                    new_neighborlist += toadd
                    #print("so that the new neighborlist is: %s"%new_neighborlist)

            neighbor_list[ridx] = [ii for ii in _np.unique(new_neighborlist) if ii!=ridx]
            #break

    # Check that the neighborlist works both ways
    for ii, ilist in enumerate(neighbor_list):
        for nn in ilist:
            assert ii in neighbor_list[nn]

    return neighbor_list
