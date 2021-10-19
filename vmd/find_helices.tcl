set prev "-10"
set sel [atomselect top alpha_helix]
# $sel get resid
foreach n [$sel get resid] { 
if {$n > [expr $prev+1]} { 
puts "$n"
$prev = $n
} 
}
