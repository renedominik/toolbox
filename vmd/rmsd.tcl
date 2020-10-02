set sel1 [atomselect 0 "backbone"] 
set sel2 [atomselect 1 "backbone"] 
measure rmsd $sel1 $sel2