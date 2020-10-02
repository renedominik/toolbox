set sel [atomselect top "name CA"]
source grafix.tcl


set i 0
foreach m [$sel get resid] { 
    set calpha [ $sel get { x y z }]
    set end [vecadd $calpha $displacement]
    draw arrow $calpha $end
    set i [expr $i+1]
}
