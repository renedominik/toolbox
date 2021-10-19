source /home/levinam/workspace/benchmark/vmd/molmovie.tcl
set a 1
set x 249
set delay 10
for {set i $a} {$i < $x} {incr i} {
    mol new [format "proteinmodel%d.pdb" $i]
}


set nmols [molinfo num]
if {![info exists molmovie_last]} {
    set molmovie_last [expr $nmols - 1]
}

for {set i 0} {$i < $nmols} {incr i} {
    mol modstyle 0 $i Licorice
    mol modcolor 0 $i Index
    mol off $i
}


for {set n 0} {$n < $nmols} {incr n} {
display update
display update ui
mol on $n
mol off $molmovie_last
render snapshot [format "proteinmodel%d.tga" $n]
set molmovie_last $n
after $delay
}
