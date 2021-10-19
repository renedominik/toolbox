set n [molinfo num] 
for { set i 0 } { $i < $n } { incr i } {
set sel [atomselect $i "all"] 
$sel writepdb model_$i.pdb
}
