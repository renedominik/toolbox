proc make_movie_files {} {
    set frame 0
    for {set i 0} {$i < 100} {incr i 1} {
	set filename snap.[format "%04d" $frame].rgb
	gopython drawSE[ format "%04d" $frame].py
	render snapshot $filename
	incr frame
    }
    for {set i 0} {$i < 360} {incr i 20} {
	set filename snap.[format "%04d" $frame].rgb
	render snapshot $filename
	incr frame
	rotate y by 20
    }
# 
# add pdb of solved structure (if any )
# add red lines to show distances of Ca-Ca
}
