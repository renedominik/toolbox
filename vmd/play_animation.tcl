source /home/rene/progs/vmd/lib/molmovie.tcl
set a 1
set x 503
set delay 1000
axis location off
rock off
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
    graphics $i color white
    graphics $i text {20 -10 0} "frame  [expr $i+1]"
    graphics $i text {20 -12 0} "[molinfo $i get numatoms] atoms"
    set remarkss [molinfo $i get remarks]
    set first [string first "score" $remarkss]
    graphics $i text {20 -14 0} [string range $remarkss $first [expr $first + 15]]

    mol off $i
}


molmovie 1 $delay
