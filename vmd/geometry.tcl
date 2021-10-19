# ========== A slightly expanded version than the one from the VMD script library =====
# Calculate phi, psi and omega
# Usage:
#   phi <molid> <segid> <resid>
#   psi <molid> <segid> <resid>
#   omega <molid> <segid> <resid>
# The code will run well if you get all the values for a particular molid/segid
# pair at a time; every time you change the molid or segid it has to make an
# expensive atom selection.
# ====================================================
#  In most PDB files the segid is the last entry.
#  
#  You can query the segid as in the following example:
#  
#  # select some atoms:
#  set sel [atomselect top "resid 5"]
#  set mysegid [$sel get segid]
#  puts $mysegid
#  (This prints the segids for each atom.)
#  
#  You can set the segid for a selection with
#  
#  set mysegid "P1"
#  $sel set segid $mysegid
  

proc signed_angle { a b c } {
  set amag [veclength $a]
  set bmag [veclength $b]
  set dotprod [vecdot $a $b]
  
  set crossp [veccross $a $b]
  set sign [vecdot $crossp $c]
  if { $sign < 0 } { 
    set sign -1 
  } else { 
    set sign 1
  }
  return [expr $sign * 57.2958 * acos($dotprod / ($amag * $bmag))]
}
    
proc dihedral { a1 a2 a3 a4 } {
  if {[llength $a1] != 3 || [llength $a2] != 3 || [llength $a3] != 3 || [llength $a4] != 3} {
    return 0
  } 
 
  set r1 [vecsub $a1 $a2]
  set r2 [vecsub $a3 $a2]
  set r3 [vecscale $r2 -1]
  set r4 [vecsub $a4 $a3]

  set n1 [veccross $r1 $r2]
  set n2 [veccross $r3 $r4]
  
  return [signed_angle $n1 $n2 $r2]
}

proc reset_geometry_cache { } {
  global geometry_molid geometry_segid geometry_cache geometry_frame
  set geometry_molid -1
}

proc set_geometry_cache { molid segid } {
  global geometry_molid geometry_segid geometry_cache geometry_frame
  set frame [molinfo top get frame]
  if { [info exists geometry_molid] 
    && [info exists geometry_segid]  
    && [info exists geometry_frame] } {
    if { $molid == $geometry_molid 
      && $segid == $geometry_segid 
      && $frame == $geometry_frame } {
      return
    }
  }
  set geometry_molid $molid
  set geometry_segid $segid
  set geometry_frame $frame

  catch { unset geometry_cache }
   
  set n [atomselect $molid "segid $segid and name N" ]
  set ca [atomselect $molid "segid $segid and name CA" ]
  set c [atomselect $molid "segid $segid and name C" ]

  foreach resid [$n get resid] xyz [$n get {x y z}] {
    set geometry_cache($resid,n) $xyz
  }
  foreach resid [$ca get resid] xyz [$ca get {x y z}] {
    set geometry_cache($resid,ca) $xyz
  }
  foreach resid [$c get resid] xyz [$c get {x y z}] {
    set geometry_cache($resid,c) $xyz
  }
}

proc analyseNCAC { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache($resid,c)
	set a2 $geometry_cache($resid,ca)
	set a3 $geometry_cache($resid,n)
    } ] } { return 0 }
    set d1 [vecsub $a2 $a1]
    set d2 [vecsub $a2 $a3]
    set l1  [veclength $d1]
    set l2  [veclength $d2]
#      set s6  "  Position  C"
#      set s7  "  Position CA"
#      set s8  "  Position  C"
#      puts " ------------------   N CA C ANALYSIS ------------------------------ "
#      puts "$s6[expr $resid-2]     $a1"
#      puts "$s7[expr $resid-1]     $a2"
#      puts "$s8$resid     $a3"
    set s1  " Length Vector CA[expr $resid-1]-C[expr $resid-2]: "
    set s2  " Length Vector CA[expr $resid-1]-N$resid: "
    set s3  " Angle between the Vectors:  "  
    puts "$s1          $l1"
    puts "$s2          $l2"
    set alpha [ expr acos( [vecdot $d1 $d2] / [veclength $d1] / [veclength $d2] ) ]
    set alpha [expr $alpha*180/acos(-1)]
    puts  "$s3    $alpha"
    return alpha
}

proc distanceNCA { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache($resid,n)
	set a2 $geometry_cache($resid,ca)

    } ] } { return 0 }
    set d1 [vecsub $a2 $a1]

    return [veclength $d1]
}

proc distanceCAC { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache($resid,c)
	set a2 $geometry_cache($resid,ca)

    } ] } { return 0 }
    set d1 [vecsub $a2 $a1]

    return [veclength $d1]
}




proc analyse3CA { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache([expr $resid - 2],ca)
	set a2 $geometry_cache([expr $resid - 1],ca)
	set a3 $geometry_cache($resid,ca)
    } ] } { return 0 }
    set d1 [vecsub $a2 $a1]
    set d2 [vecsub $a2 $a3]
    set l1  [veclength $d1]
    set l2  [veclength $d2]
    puts " ===================  3 CA ANALYSIS ======================= "
#      set s6  "  Position CA"
#      set s7  "  Position CA"
#      set s8  "  Position CA"
#      puts "$s6[expr $resid-2]     $a1"
#      puts "$s7[expr $resid-1]     $a2"
#      puts "$s8$resid     $a3"
    set s1  " Length Vector CA[expr $resid-1]-CA[expr $resid-2]: "
    set s2  " Length Vector CA[expr $resid-1]-CA$resid: "
    set s3  " Angle between the Vectors:  "  
    puts "$s1          $l1"
    puts "$s2          $l2"
    set alpha [ expr acos( [vecdot $d1 $d2] / [veclength $d1] / [veclength $d2] ) ]
    set alpha [expr $alpha*180/acos(-1)]
    puts  "$s3    $alpha"
    return alpha
}



proc distance2CA { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache([expr $resid - 1],ca)
	set a2 $geometry_cache($resid,ca)
    } ] } { return 0 }
    set d1 [vecsub $a2 $a1]
    return  [veclength $d1]
}


proc vmd_draw_residueZaxisFromNCAC { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache($resid,n)
	set a2 $geometry_cache($resid,ca)
	set a3 $geometry_cache($resid,c)
    } ] } { return 0 }
    set d1 [vecsub $a1 $a2]
    set d2 [vecsub $a3 $a2]
    set d3 [veccross $d1 $d2]
    set start [vecadd  $a2      [vecscale    1.42227   $d1] [vecscale    1.26493  $d2] [vecscale   0.0360416  $d3] ]
    set end   [vecadd  $start   [vecscale   -0.293388  $d1] [vecscale    0.363519 $d2] [vecscale  -0.286081   $d3] ]

    puts  [veclength  [vecadd     [vecscale    1.42227   $d1] [vecscale    1.26493  $d2] [vecscale   0.0360416  $d3] ]]
    puts [veclength   [vecadd     [vecscale   -0.293388  $d1] [vecscale    0.363519 $d2] [vecscale  -0.286081   $d3] ]]

    draw color white
    draw arrow $a2 $a1
    draw arrow $a2 $a3
#    draw arrow $a2 [vecadd $a2 $d3]
    draw color orange
    draw arrow $a2 $start
    draw color red
    draw arrow $start $end
}

# 	set a1 $geometry_cache($resid,ca)
# 	set a2 $geometry_cache([expr $resid+1],ca)
# 	set a3 $geometry_cache([expr $resid+2],ca)


proc vmd_draw_residueZaxisFromThreeCA { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    if { [catch {
	set a1 $geometry_cache([expr $resid-2],ca)
	set a2 $geometry_cache([expr $resid-1],ca)
	set a3 $geometry_cache($resid,ca)
    } ] } { return 0 }
    set x  [vecsub $a1 $a2]
    set y  [vecsub $a3 $a2]
    set z  [veccross $x $y]
    set start [vecadd $a2    [vecscale   0.428984  $x]  [vecscale  0.428986  $y] [vecscale   1.95958e-07 $z] ] 
    set end   [vecadd $start [vecscale  -0.104829  $x]  [vecscale  0.104829  $y] [vecscale  -0.0574036   $z] ]

    puts  [veclength  [vecadd  [vecscale  -0.409029  $x]  [vecscale  0.267     $y] [vecscale   0.0887027  $z]]]
    puts  [veclength  [vecadd  [vecscale  -0.104829  $x]  [vecscale  0.104829  $y] [vecscale  -0.0574036  $z]]]

    draw color white
    draw arrow $a2 $a1
    draw arrow $a2 $a3
#    draw arrow $a2 [vecadd $a2 $z]
    draw color yellow
    draw arrow $a2 $start
    draw color green
    draw arrow $start $end
}





  proc phi { molid segid resid } {
    global geometry_cache
    set_geometry_cache $molid $segid
    
    if { [catch {
      set a1 $geometry_cache([expr $resid - 1],c)
      set a2 $geometry_cache($resid,n)
      set a3 $geometry_cache($resid,ca)
      set a4 $geometry_cache($resid,c)
    } ] } { return 0 }
  return [dihedral $a1 $a2 $a3 $a4]
  }


proc psi { molid segid resid } {
  global geometry_cache
  set_geometry_cache $molid $segid
  
  if { [catch {
    set a1 $geometry_cache($resid,n)
    set a2 $geometry_cache($resid,ca)
    set a3 $geometry_cache($resid,c)
    set a4 $geometry_cache([expr $resid + 1],n)
  } ] } { return 0 }
  return [dihedral $a1 $a2 $a3 $a4]
}

# Omega lies in between two residues.  I'll adopt the convention that
# asking for residue n gives you the omega between residues n and n+1.
proc omega { molid segid resid } {
  global geometry_cache
  set_geometry_cache $molid $segid
  
  if { [catch {
    set a1 $geometry_cache($resid,ca)
    set a2 $geometry_cache($resid,c)
    set a3 $geometry_cache([expr $resid + 1],n)
    set a4 $geometry_cache([expr $resid + 1],ca)
  } ] } { return 0 }
  return [dihedral $a1 $a2 $a3 $a4]
}


#####
# Commands for setting phi, psi and omega

proc setphi { molid segid resid value } {
  
  # We rotate about the N-CA bond.  
  #   0. Get the current value of phi
  #   1. Translate, putting CA at the origin  (T)
  #   2. Compute the axis along N-CA.
  #   3. Rotate just the N-terminus about the given axis. 
  #   4. Undo T.
  
  set oldphi [phi $molid $segid $resid]
 
  set nsel [atomselect $molid "segid $segid and resid $resid and name N"]
  set casel [atomselect $molid "segid $segid and resid $resid and name CA"]
  set n [lindex [$nsel get {x y z}] 0]
  set ca [lindex [$casel get {x y z}] 0]
  set seltext "((resid 1 to [expr $resid-1]) or (resid $resid and name N NH))"

  set all [atomselect $molid "segid $segid"]
  set sel [atomselect $molid "segid $segid and $seltext"]
  
  set axis [vecnorm [vecsub $n $ca]]
  set amount [expr $value - $oldphi]

  $all moveby [vecinvert $ca]
  $sel move [transabout $axis $amount]
  $all moveby $ca 

  reset_geometry_cache
}

proc setpsi { molid segid resid value } {
  
  # We rotate about the CA-C bond.  
  #   0. Get the current value of phi
  #   1. Translate, putting CA at the origin  (T)
  #   2. Compute the axis along N-CA.
  #   3. Rotate just the C-terminus about the given axis. 
  #   4. Undo T.
  
  set oldpsi [psi $molid $segid $resid]
 
  set casel [atomselect $molid "segid $segid and resid $resid and name CA"]
  set csel [atomselect $molid "segid $segid and resid $resid and name C"]
  set ca [lindex [$casel get {x y z}] 0]
  set c [lindex [$csel get {x y z}] 0]
  set seltext "((resid [expr $resid+1] to 9999) or (resid $resid and name C O))"

  set all [atomselect $molid "segid $segid"]
  set sel [atomselect $molid "segid $segid and $seltext"]
  
  set axis [vecnorm [vecsub $c $ca]]
  set amount [expr $value - $oldpsi]

  $all moveby [vecinvert $ca]
  $sel move [transabout $axis $amount]
  $all moveby $ca 

  reset_geometry_cache
}

