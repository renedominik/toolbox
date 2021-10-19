# vmd tcl procedure: animate by turning all molecules on and off 
#
# $Id: molmovie.tcl,v 1.1 2005/01/03 14:06:39 akohlmey Exp $
# Time-stamp: <akohlmey 02.01.2005 16:18:10 timburton.site>
#
# Copyright (c) 2004-2005 by <Axel.Kohlmeyer@theochem.ruhr-uni-bochum.de>
#
# The molmovie procedure creates an animation by 
# sequentially turning the molecules on and off.
# The default is to wait a 500 miliseconds between 'frames'.




global ExistScoreList 
set ExistScoreList "false"
global ExistPlotBox 
set ExistPlotBox "false"
global NumberOfMembranes
set NumberOfMembranes 0
# This is the number (not necessarily the number of frames)
global NumberOfMolecules 
set NumberOfMolecules 0
global CurrentMolecule
set CurrentMolecule 0



# Copyright (c) 2004-2005 by <Axel.Kohlmeyer@theochem.ruhr-uni-bochum.de>
# modified: Rene Staritzbichler, Andrew Levin 
proc movie {{loops 10} {delay 200} {from 0} {till 1000000}} {
#    global molmovie_last
    global ExistScoreList
    global ExistPlotBox
    global NumberOfMembranes
    global NumberOfMolecules
    global CurrentMolecule
    puts "NumberOfMolecules = " 
    puts $NumberOfMolecules
    clearpdbs

    if {$NumberOfMolecules < $till} {
	set till $NumberOfMolecules
    }

    # if there are plot boxes then continously switch frame 2 * NumberOfMolecules + 1 on
    
    if {$ExistPlotBox == "true"} {
	for {set i 0} {$i <= $NumberOfMembranes} {incr i} {
	    mol on [expr 2 * $NumberOfMolecules + $i]
	    puts "ExistPlotBox = True"
	}
    } else {
	for {set i 0} {$i <= $NumberOfMembranes} {incr i} {	  
	    mol on [expr $NumberOfMolecules + $i]
	}	
    }

    
    for {set i 0} {$i < $loops} {incr i} {
	mol on $from
	#set [molinfo num]
	mol on [expr $from + $NumberOfMolecules]
	after $delay
	for {set n [expr $from + 1]} {$n < $till} {incr n} {
            display update
            display update ui
	    #	    mol on [expr $number_of_molecules - 1]
            mol on $n
	    if {$ExistPlotBox == "true"} {
		mol on [expr $n + $NumberOfMolecules]
	    }
	    mol off [expr $n - 1]
	    if {$ExistPlotBox == "true"} {
		mol off [expr $n + $NumberOfMolecules - 1]
	    }
	    set CurrentMolecule $n
            after $delay
        }
	if {[expr $i + 1] < $loops} {
	    mol off [expr $till -1]
	    mol off [expr $till + $NumberOfMolecules -1]
	}
    }
}

# Copyright (c) 2004-2005 by <Axel.Kohlmeyer@theochem.ruhr-uni-bochum.de>
proc simple_movie {{loops 10} {delay 200} {from 0} {till 1000000}} {
    global molmovie_last
    clearpdbs
    set number_of_molecules [molinfo num]
    if {![info exists molmovie_last]} {
        set molmovie_last [expr $number_of_molecules - 1]
    }

    if {$number_of_molecules < $till} {

	set till $number_of_molecules
    }
    
    for {set i 0} {$i < $loops} {incr i} {
        for {set n $from} {$n < $till} {incr n} {
            display update
            display update ui
            mol on $n
            mol off $molmovie_last
            set molmovie_last $n
            after $delay
        }
    }
}


# author: Rene Staritzbichler, 13.7.2006
#"pre" means prefix and "suf" means suffix
#Leaves the procedure when the pdb model does not exist
proc load_frames {{a 0} {b 500} {pre "model"} {suf ".pdb"}} {
    global NumberOfMolecules
    axes location off
    rock off
    #set count 0
    for {set i $a} {$i <= $b} {incr i} {
	
	# replaces %d with $i
	mol new [format "$pre%d$suf" $i]
	mol modstyle 0 $NumberOfMolecules Licorice
	mol modcolor 0 $NumberOfMolecules Index
	mol off $NumberOfMolecules
	set NumberOfMolecules [expr $NumberOfMolecules + 1]
    }
  
}

# author: Rene Staritzbichler, 13.7.2006
proc score_list { } {

    global ExistScoreList
    global ExistPlotBox
    set ExistScoreList "true"

    set number_of_molecules [molinfo num]

#      if {![info exists molmovie_last]} {
#  	set molmovie_last [expr $number_of_molecules - 1]
#      }

      
    for {set i 0} {$i < $number_of_molecules} {incr i} {
	
	if {$ExistPlotBox == "false"} {
	    mol new
	}
	set j  [expr $i + $number_of_molecules]

	graphics $j color white
	
	graphics $j text {-0.5 -1.4 -2} "this frame  [expr $i]" size 0.8
	graphics $j text {-0.5 -1.55 -2} "[molinfo $i get numatoms] atoms" size 0.8
	set remarkss [molinfo $i get remarks]
	set first [string first "scoresum:" $remarkss]
	graphics $j text {-0.5 -1.7 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "aadist:" $remarkss]
	graphics $j text {-0.5 -1.85 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "aaenv" $remarkss]
	graphics $j text {-0.5 -2  -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "rgyr2:" $remarkss]
	graphics $j text {-0.5 -2.15 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "loop:" $remarkss]
	graphics $j text {-0.5 -2.3 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "ssealign" $remarkss]
	graphics $j text {-0.5 -2.45 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "ssepack:" $remarkss]
	graphics $j text {-0.5 -2.6 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "ssecont:" $remarkss]
	graphics $j text {-0.5 -2.75 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	set first [string first "rmsd:" $remarkss]
	graphics $j text {-0.5 -2.9 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
    }


     for {set i 0} {$i < $number_of_molecules} {incr i} {
 	if {$i < $number_of_molecules - 1} {
 	    set j [expr $i + $number_of_molecules + 1]
 	    graphics $j text {-2.4 -1.4 -2} "previous frame  [expr $i]" size 0.8
 	    graphics $j text {-2.4 -1.55 -2} "[molinfo $i get numatoms] atoms" size 0.8
 	    set remarkss [molinfo $i get remarks]
# 	    set remarkss [molinfo [expr $i + 1] get remarks]
 	    set first [string first "scoresum:" $remarkss]
 	    graphics $j text {-2.4 -1.7 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "aadist:" $remarkss]
 	    graphics $j text {-2.4 -1.85 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "aaenv" $remarkss]
 	    graphics $j text {-2.4 -2 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "rgyr2:" $remarkss]
 	    graphics $j text {-2.4 -2.15 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "loop:" $remarkss]
 	    graphics $j text {-2.4 -2.3 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "ssealign" $remarkss]
 	    graphics $j text {-2.4 -2.45 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "ssepack:" $remarkss]
 	    graphics $j text {-2.4 -2.6 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	    set first [string first "ssecont:" $remarkss]
	    graphics $j text {-2.4 -2.75 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	    set first [string first "rmsd:" $remarkss]
	    graphics $j text {-2.4 -2.9 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	}
 
 
 	if {$i  > 0} {
 	    set j [expr $i + $number_of_molecules - 1]
 	    graphics $j text {1.4 -1.4 -2} "next frame  [expr $i]" size 0.8
 	    graphics $j text {1.4 -1.55 -2} "[molinfo $i get numatoms] atoms" size 0.8
# 	    set remarkss [molinfo [expr $i - 1] get remarks]
 	    set remarkss [molinfo $i get remarks]
 	    set first [string first "scoresum:" $remarkss]
 	    graphics $j text {1.4 -1.7 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "aadist:" $remarkss]
 	    graphics $j text {1.4 -1.85 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "aaenv" $remarkss]
 	    graphics $j text {1.4 -2 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "rgyr2:" $remarkss]
 	    graphics $j text {1.4 -2.15 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "loop:" $remarkss]
 	    graphics $j text {1.4 -2.3 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "ssealign" $remarkss]
 	    graphics $j text {1.4 -2.45 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	    set first [string first "ssepack:" $remarkss]
 	    graphics $j text {1.4 -2.6 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	    set first [string first "ssecont:" $remarkss]
	    graphics $j text {1.4 -2.75 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
	    set first [string first "rmsd:" $remarkss]
	    graphics $j text {1.4 -2.9 -2} [string range $remarkss $first [expr $first + 20]] size 0.8
 	}
# 	mol fix [expr $i + $number_of_molecules]
# 
# #	mol off [expr $i + $number_of_molecules]
#     }

    for {set i 0} {$i < $number_of_molecules} {incr i} {
 	mol fix [expr $i + $number_of_molecules]
    }
}



# from vmd guide
proc arrow {mol start end} {
    # an arrow is made of a cylinder and a cone
    set middle [vecadd $start [vecscale 0.9 [vecsub $end $start]]]
    graphics $mol cylinder $start $middle radius 0.15
    graphics $mol cone $middle $end radius 0.25
}

# author: Rene Staritzbichler, 13.7.2006
proc bodies { } {

    set number_of_molecules [molinfo num]

    for {set i 0} {$i < $number_of_molecules} {incr i} {
	#find body info

	set remark_string [molinfo $i get remarks]
	set begin [string first "bcl::Body" $remark_string] 
	while {$begin >= 0} {
	    #extract information from string
	    set end [string first "bcl::math::Vector3D" $remark_string]
	    set substring [string range $remark_string [expr $begin + 10] [expr $end - 2]]
	    scan $substring "%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f" a b v1_x v1_y v1_z c v2_x v2_y v2_z d v3_x v3_y v3_z e o_x o_y o_z


	    # modify string for next iteration
	    set remark_string [string range $remark_string [expr $end + 1] [string length $remark_string]]
#	    set cut [string first "bcl::Vector3D" $remark_string]
#	    set remark_string [string range $remark_string $cut [string length $remark_string]]

#	    set remark_string [string range $remark_string $end [string length $remark_string]]
	    set begin [string first "bcl::Body" $remark_string] 

	    #write into vectors
	    set vec_x "$v1_x $v1_y $v1_z"
	    set vec_y "$v2_x $v2_y $v2_z"
	    set vec_z "$v3_x $v3_y $v3_z"
	    set origin "$o_x $o_y $o_z"

	    #display it
	    graphics $i color green
	    set peak [vecadd $vec_x $origin]
	    arrow $i $origin $peak
  	    graphics $i color yellow
  	    set peak  [vecadd $vec_y $origin]
  	    arrow $i $origin $peak
  	    graphics $i color red	 	  		 
  	    set peak  [vecadd $vec_z $origin]
  	    arrow $i $origin $peak
	}
    }
}

# Author: Rene Staritzbichler, 7.11.2006
#Note that TCL will stop and leave the procedure when it encounters a command it cannot execute (i.e. output a nonexistent variable)
#center_matrix actually moves molecules in relation to one another; you can only edit the fourth entry in each line
#rotate_matrix also moves molecules relative to each other when you zoom in or out
#Note that changes the settings for the top molecule only does that for the top molecule so it can mess up the relative configuration of molecules
#molinfo center is set automatically to the origin for membrane, but it is set to some other value for the pdb
#Setting all of the molinfo centers equal does not help
#The last column in center_matrix allows you to change the position of the molecule in 3D? space
proc membrane {{color yellow} {thick 40}} {

    global NumberOfMembranes

    set number_of_molecules [molinfo num]
    puts "center  [molinfo 0 get center]"
    puts "center_matrix  [molinfo 0 get center_matrix]"
    puts "scale_matrix  [molinfo 0 get scale_matrix]"
    puts "global_matrix  [molinfo 0 get global_matrix]"
    mol new
    molinfo $number_of_molecules set scale_matrix [molinfo 0 get scale_matrix]
    molinfo $number_of_molecules set center_matrix [molinfo 0 get center_matrix]
    graphics $number_of_molecules color $color
    graphics $number_of_molecules material Glass
#    change_transparency 0.9
    set z [expr $thick * 0.5]
    graphics $number_of_molecules triangle "-75 -50 -$z" "75 -50 -$z" "0 75 -$z"
    graphics $number_of_molecules triangle "-75 -50  $z" "75 -50  $z" "0 75  $z"
    set NumberOfMembranes [expr $NumberOfMembranes + 1]
}

proc membraneXX {{color yellow} {thick 40}} {

    global NumberOfMembranes
    global NumberOfMolecules
    global ExistPlotBox
    # Defines where the view starts
    #VMD defines a scale matrix and a perspective
    puts "center  [molinfo 0 get center]"
    puts "center_matrix  [molinfo 0 get center_matrix]"
    puts "scale_matrix  [molinfo 0 get scale_matrix]"
    puts "global_matrix  [molinfo 0 get global_matrix]"
   
    
   # puts "[expr 2*$NumberOfMolecules] :  [molinfo num]"
    
   
    mol new
    #puts "[expr 2*$NumberOfMolecules] :  [molinfo num]"
    
    
    
    #puts molinfo $NumberOfMolecules get center_matrix
    #change_transparency 0.9
    set z [expr $thick * 0.5]
    #defines the three endpoints of the triangular membrane
    graphics [expr 2*$NumberOfMolecules+1] triangle "-75 -50 -$z" "75 -50 -$z" "0 75 -$z"
    graphics [expr 2*$NumberOfMolecules+1] triangle "-75 -50  $z" "75 -50  $z" "0 75  $z"
    set NumberOfMembranes [expr $NumberOfMembranes + 1]
    
    #molinfo 2 set center_matrix [molinfo 0 get scale_matrix]
    
    #molinfo 0 set {center_matrix} {{{1.000000 0.000000 0.000000 1.051054} {0.000000 1.000000 0.000000 -1.044969} {0.000432000 0.000000 1.000000 0.079573} {0.000000 0.000000 0.000000 1.000000}}}
    #molinfo 1 set {center_matrix} {{{1.000000 0.000000 0.000000 1.051054} {0.000000 1.000000 0.000000 -1.044969} {0.000432000 0.000000 1.000000 0.079573} {0.000000 0.000000 0.000000 1.000000}}}
    #molinfo 2 set {center_matrix} {{{1.000000 0.000000 0.000000 1.051054} {0.000000 1.000000 0.000000 -1.044969} {0.000432000 0.000000 1.000000 0.079573} {0.000000 0.000000 0.000000 1.000000}}}
    #molinfo [molinfo top] set {center_matrix} {{{0.000000 0.000000 0.000000 0.051054} {0.000000 1.000000 0.000000 -1.044969} {0.000432000 0.000000 1.000000 1.079573} {0.000000 0.000000 0.000000 13.000000}}}
    
    
    #molinfo 0 set {view_matrix} {{{0.000000 0.000000 0.000000 0.051054} {0.000000 1.000000 0.000000 -1.044969} {0.000432000 0.000000 1.000000 1.079573} {0.000000 0.000000 0.000000 13.000000}}}

    puts "view_matrix: [molinfo 0 get view_matrix]"
    puts "view_matrix: [molinfo 1 get view_matrix]"
    puts "view_matrix: [molinfo 2 get view_matrix]"
    puts "view_matrix: [molinfo 3 get view_matrix]"


    puts "center  [molinfo 0 get center]"
    puts "center  [molinfo 1 get center]"
    puts "center  [molinfo 2 get center]"
    puts "center  [molinfo 3 get center]"
   
    puts "The following line contains the current value of center_matrix for id 0"
    puts [molinfo 0 get center_matrix] 
    puts "The following line contains the current value of center_matrix for id 1"
    puts [molinfo 1 get center_matrix] 
    puts "The following line contains the current value of center_matrix for id 2"
    puts [molinfo 2 get center_matrix] 
    puts "The following line contains the current value of center_matrix for id 3"
    puts [molinfo 3 get center_matrix]
    puts "The following line contains the current value of scale_matrix for id 0"
    
    puts [molinfo 3 get global_matrix]
    puts "The following line contains the current value of rotate_matrix for id 3"
    puts [molinfo 3 get rotate_matrix]
    puts "The following line contains the current value of center for id 3"
    puts [molinfo 3 get center]
}

# Author: Rene Staritzbichler, 7.11.2006
proc solid_membrane {{color yellow} {thick 40}} {

    set number_of_molecules [molinfo num]
    mol new
    graphics $number_of_molecules color $color
#    graphics $number_of_molecules material Glass
#    change_transparency 0.9
    set z [expr $thick * 0.5]
    graphics $number_of_molecules triangle "-75 -50 -$z" "75 -50 -$z" "0 75 -$z"
    graphics $number_of_molecules triangle "-75 -50  $z" "75 -50  $z" "0 75  $z"
}


# Author: Rene Staritzbichler, 7.11.2006
proc plot_box {{first "frames"} second {location {0.8 1.5 -2}} {width 1.8} {height 1.2}} {

    global ExistScoreList
    global ExistPlotBox
    global NumberOfMolecules

    set frame {0.1 0.1 0}

    set number_of_molecules [molinfo num] 

    if {$ExistPlotBox == "true"} {
	puts "no frames we added previously"
	set number_of_molecules [expr [expr [molinfo num] - 1] / 2]
    }
    if {$ExistScoreList == "true" && $ExistPlotBox == "false"} {
	puts "ScoreList was added previously"
	set number_of_molecules [expr 0.5 * [molinfo num]]
    }
    
    puts "number of molecules: $number_of_molecules"
    puts "number of frames: [molinfo num]"
    
    set first_max  -10000
    set first_min   10000
    set second_max -10000
    set second_min  10000

    
    #collect data in list
    for {set i 0} {$i < $number_of_molecules} {incr i} {

 	set remark_string [molinfo $i get remarks]

	if {$first != "frames"} {
	    set begin [string first $first $remark_string]
	    set substring [string range $remark_string $begin [expr $begin + 25]]
	    scan $substring "%s %f" tmp first_value

	    set list_first($i) $first_value

	    # determine range of values for scaling
	    if {$first_value < $first_min} {
		set first_min $first_value
	    }
	    if {$first_value > $first_max} {
		set first_max $first_value
	    }
	} else {
	    set list_first($i) [expr $i + 0.0]
	    set first_min 0
	    set first_max $number_of_molecules
	}
	
 	set begin [string first $second $remark_string]
	set substring [string range $remark_string $begin [expr $begin + 25]]
	scan $substring "%s %f" tmp second_value
	
 	set list_second($i) $second_value


	# determine range of values for scaling
  	if {$second_value < $second_min} {
 	    set second_min $second_value
 	}
 	if {$second_value > $second_max} {
	    set second_max $second_value
 	}
    }

    
    #normalize data and expand  
    foreach  i [lsort [array names list_first]] {
	set list_first($i) [expr [expr $list_first($i) - $first_min] / [expr $first_max - $first_min]]
	set list_first($i) [expr $width * $list_first($i)]
    }
    foreach  i [array names list_first] {
	set list_second($i) [expr [expr $list_second($i) - $second_min] / [expr $second_max - $second_min]]
	set list_second($i) [expr $height * $list_second($i)]
    }
      
    for {set i 0} {$i < $number_of_molecules} {incr i} {
	if {$ExistScoreList == "false" && $ExistPlotBox == "false"} {
	    mol new 
	} 
   	set j  [expr $i + $number_of_molecules]
   	
   	graphics $j color red
#   	graphics $j point [vecadd "$list_first($i) $list_second($i) 0" $location]
   	graphics $j sphere [vecadd "$list_first($i) $list_second($i) 0" $location] radius 0.02 
      }


    if {$ExistPlotBox == "false"} {
	mol new 
    }
    set nmols [expr [molinfo num] - 1]

    graphics $nmols color white

    graphics $nmols line [vecsub $location $frame] [vecadd $location "-[lindex $frame 0] [expr $height + [lindex $frame 1]] 0"]
    graphics $nmols line [vecsub $location $frame] [vecadd $location "[expr $width + [lindex $frame 0]] -[lindex $frame 1] 0"]
    graphics $nmols line [vecadd $location "[expr $width + [lindex $frame 0]] -[lindex $frame 1] 0"] [vecadd $location [vecadd "$width $height 0" $frame]]
    graphics $nmols line [vecadd $location "-[lindex $frame 0] [expr $height + [lindex $frame 1]] 0"] [vecadd $location [vecadd "$width $height 0" $frame]]

    graphics $nmols text [vecadd $location "[expr 0.4 * $width] [expr [lindex $frame 0] - 0.35] 0"] $first size 0.6
    graphics $nmols text [vecadd $location "-[expr [lindex $frame 0] + 0.5] [expr 0.5 * $height ] 0"] $second size 0.6

    graphics $nmols line [vecsub $location "0 [lindex $frame 0] 0"]  [vecsub $location "0 [expr 0.8 *[lindex $frame 0]] 0"]
    graphics $nmols line [vecsub $location "[lindex $frame 1] 0 0"]  [vecsub $location "[expr 0.8 *[lindex $frame 1]] 0 0"]
    graphics $nmols line [vecsub $location "-$width [lindex $frame 0] 0"]  [vecsub $location "-$width [expr 0.8 *[lindex $frame 0]] 0"]
    graphics $nmols line [vecsub $location "[lindex $frame 1] -$height 0"]  [vecsub $location "[expr 0.8 *[lindex $frame 1]] -$height 0"]


#    graphics $nmols line [vecsub $location $frame] [vecadd $location "[expr $width + [lindex $frame 0]] -[lindex $frame 1] 0"]
#    graphics $nmols line [vecadd $location "[expr $width + [lindex $frame 0]] -[lindex $frame 1] 0"] [vecadd $location [vecadd "$width $height 0" $frame]]
#    graphics $nmols line [vecadd $location "-[lindex $frame 0] [expr $height + [lindex $frame 1]] 0"] [vecadd $location [vecadd "$width $height 0" $frame]]    

    graphics $nmols text [vecsub $location "0 [expr 1.6 *[lindex $frame 0]] 0"] $first_min size 0.4
    graphics $nmols text [vecsub $location "-$width [expr 1.6 *[lindex $frame 0]] 0"] $first_max size 0.4
    graphics $nmols text [vecsub $location "[expr 0.3 + [lindex $frame 0]] 0 0"] $second_min size 0.4
    graphics $nmols text [vecsub $location "[expr 0.3 + [lindex $frame 0]] -$height 0"] $second_max size 0.4


    
    for {set i 0} {$i < $number_of_molecules} {incr i} {
#   	graphics $number_of_molecules point [vecadd "$list_first($i) $list_second($i) 0" $location]
   	graphics $nmols sphere [vecadd "$list_first($i) $list_second($i) 0" $location] radius 0.01 
    }
    for {set i 0} {$i <= $number_of_molecules} {incr i} {
   	mol fix [expr $i + $number_of_molecules]
    }

    set ExistPlotBox "true"
}


##  proc next { } {
##      global this_frame
##      
##      if {![info exists this_frame]} {
##  	for {set i 0} {$i < [molinfo num]} {incr i} {
##  	    if {[molinfo $i get drawn]} {
##  		set this_frame $i
##  	    }
##  	}
##      }
##      mol off $this_frame
##      mol on [expr $this_frame +1]
##  }

# author: Rene Staritzbichler, 13.7.2006
# modified:  Andrew Levin, Rene Staritzbichler 8.2.2007 

proc prev { } {
    
    global ExistPlotBox
    global NumberOfMolecules
    global CurrentMolecule
    puts "prev: current "
    
    if {$CurrentMolecule > 0} {
	puts "old frame: $CurrentMolecule"
	puts "new frame: [expr $CurrentMolecule - 1]"
	mol on [expr $CurrentMolecule - 1]
	mol off $CurrentMolecule
	if {$ExistPlotBox == true} {
	    mol on [expr $CurrentMolecule + $NumberOfMolecules - 1]
	    mol off [expr $CurrentMolecule + $NumberOfMolecules]
	}
	display update
	display update ui
	set CurrentMolecule [expr $CurrentMolecule - 1]
    }
    puts "prev: current $CurrentMolecule"
    
}

# author: Rene Staritzbichler, 13.7.2006
# modified:  Andrew Levin, Rene Staritzbichler 8.2.2007 
proc next { } {

    global ExistPlotBox
    global NumberOfMolecules
    global CurrentMolecule


    puts "$NumberOfMolecules"
    puts "next: current $CurrentMolecule"

    if {$CurrentMolecule < [expr $NumberOfMolecules - 1]} {
	puts "old frame: $CurrentMolecule"
	puts "new frame: [expr $CurrentMolecule + 1]"
	mol on [expr $CurrentMolecule + 1]
	mol off $CurrentMolecule
	if {$ExistPlotBox == true} {
	    mol on [expr $CurrentMolecule + $NumberOfMolecules + 1]
	    mol off [expr $CurrentMolecule + $NumberOfMolecules]
	}
	display update
	display update ui
	set CurrentMolecule [expr $CurrentMolecule + 1]
    }
    puts "next: current $CurrentMolecule"
    
}



# author: Rene Staritzbichler, 13.7.2006
proc clearpdbs {} {
    for {set i 0} {$i < [molinfo num]} {incr i} {
	mol off $i
    }
}
## author: Rene Staritzbichler, 13.7.2006
proc clr {} {
    clearpdbs
}


# author: Rene Staritzbichler, 13.7.2006
# modified:  Andrew Levin, Rene Staritzbichler 8.2.2007 
proc frame {{a 0}} {
    global NumberOfMolecules
    global ExistPlotBox
    global NumberOfMembranes
    global CurrentMolecule
    
    puts "frame: current $CurrentMolecule"
    if {$CurrentMolecule != $a} {
	mol off $CurrentMolecule
	
	mol on $a
	
	if {$ExistPlotBox == true} {
	    mol off [expr $CurrentMolecule + $NumberOfMolecules]
	    mol on [expr $a + $NumberOfMolecules]
	    mol on [expr 2*$NumberOfMolecules]
	    
	    if {$NumberOfMembranes > 0} {
		for {set i 1} {$i <= $NumberOfMembranes} {incr i} {
		    mol on [expr 2 * $NumberOfMolecules + $i]
		}
	    }
	} else {
	for {set i 0} {$i < $NumberOfMembranes} {incr i} {	  
	    mol on [expr $NumberOfMolecules + $i]
	}
	}
	display update
	display update ui
	set CurrentMolecule $a
    } else {
	puts "That is the current frame."
    }
    puts "frame: current $CurrentMolecule"
}


#Author: Sergei Izrailev
#standard: 0.3
proc change_transparency {new_alpha} {
        # This will always get the correct colors even if VMD
        # gains new definitions in the future
        set color_start [colorinfo num]
        set color_end [expr $color_start * 2]
        # Go through the list of colors (by index) and 
        # change their transp. value
        for {set color $color_start} {$color < $color_end} {incr color} {
                color change alpha $color $new_alpha
        }
}


#You can even make a new popup window to do this:   
#Sergei Izrailev
#user add menu Transp
#for {set i 0} {$i < 10} {incr i} {
#   set f [expr $i / 10.0]
#   user add subitem Transp $f "change_transparency $f"
#}



# see ~/progs/vmd/bucky.vmd
proc color_residues {{term "envmem"} {final "\n\n"} {midpoint 0.5}} {
    puts "color_residues"
    global ExistScoreList 
    global ExistPlotBox 
    global NumberOfMembranes
    global NumberOfMolecules
    puts "color_residues"
    
    set min  10000
    set max -10000
    #BGR means red-green-blue and defines the coloring scale
    color scale method BGR
    color scale midpoint $midpoint

    set number_of_molecules $NumberOfMolecules
    

    
    # find global max and min and collect values in list
    #molinfo remarks gets a list of freeform remarks for this molecule
    #"string first $term $remarkstring" searches $remarkstring for a sequence of characters that exactly matches that found in $term
#"string range first last" returns a range of consecutive characters from string, starting with the character whose index is first and ending with the character whose index is last
#"lappend list_of_lists $value_list" appends value_list to list_of_lists
    list list_of_lists
    for {set i 0} {$i < $number_of_molecules} {incr i} {
	list value_list
	set remarkstring [molinfo $i get remarks]
	set start_block [string first $term $remarkstring]
	set block [string range $remarkstring $start_block [string length $remarkstring]]
	set end_block   [string first $final $block]
	set block [string range $block 0 $end_block]
	

	set first [string first "\n" $block]
	set block [string range $block [expr [string first "\n" $block] + 1] [string length $block]]

	while {[string length $block] > 10} {
	    ###	for {set i 0} {$i < 5} {incr i} {}
	    set first [string first "\n" $block]
	    set line [string range $block 0 $first]
	    set block [string range $block [expr $first + 1] [string length $block]]
	    scan $line "%d %s %f %f: %f" id type xa xb value
	    puts "$id $type $value"
	    lappend value_list "$id $type $value"
	}
  	lappend list_of_lists $value_list
    }
    set a 0
    foreach molecule $list_of_lists {
	set b 0
	foreach residue $molecule {
	    # assign all atoms in a residue the user values
	    puts "residue $b value [lindex $residue 2]"
	    set atoms [atomselect $a "residue $b"]
	    foreach atom $atoms {
		$atom set user [lindex $residue 2]
	    }
	    incr b
	}
	mol modcolor 0 $a user
	incr a
    }
}





proc color_membrane {} {
    global ExistScoreList 
    global ExistPlotBox 
    global NumberOfMembranes
    
#    mol color User
    
    color scale method BGR
    
    set number_of_molecules [molinfo num]

    set number_of_molecules [expr $number_of_molecules - $NumberOfMembranes]

    if {$ExistPlotBox == "true"} {
	set number_of_molecules [expr $number_of_molecules - 1]
    }
    if {$ExistScoreList == "true" || $ExistPlotBox == "true"} {
	set number_of_molecules [expr 0.5 * $number_of_molecules]
    }
    

    for {set i 0} {$i < $number_of_molecules} {incr i} {
#	mol modcolor 0 $i User

#	set sel [atomselect $i "name CA"]
	set sel [atomselect $i all]
	set dlist ""
	foreaExistScoreListch dist [$sel get z] {
	    lappend dlist [expr sqrt( $dist * $dist)]
	}
	$sel set user $dlist
	mol modcolor 0 $i User
    }    
}
