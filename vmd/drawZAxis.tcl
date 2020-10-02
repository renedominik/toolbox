set sel [atomselect top "chain B and helix and name C CA N"]
set mysegid "P2"
$sel set segid $mysegid
source geometry.tcl
  


set i 0
foreach m [$sel get resid] { 
    draw  residueZaxisFromThreeCA P2 $i
#    draw  residueZaxisFromNCAC P2 $i
    if $i>2 {
    draw  residueZaxisFromThreeCA P2 $i
    puts "$i"
    }
    set i [expr $i+1]
}