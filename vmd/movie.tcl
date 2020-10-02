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

# This is the number (not necessarily the number of frames)
global NumberOfMolecules 
set NumberOfMolecules 0
global CurrentMolecule
set CurrentMolecule 0


# Copyright (c) 2004-2005 by <Axel.Kohlmeyer@theochem.ruhr-uni-bochum.de>
proc movie {{loops 3} {delay 200} {from 0} {till 1000000}} {
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
proc load_frames {{a 0} {b 500} {pre "model"} {suf ".pdb"} {delta 1}} {
    global NumberOfMolecules
    axes location off
    rock off
    #set count 0
    for {set i $a} {$i <= $b} {incr i $delta} {
	
	# replaces %d with $i
	mol new [format "$pre%d$suf" $i]
	mol modstyle 0 $NumberOfMolecules Licorice
	mol modcolor 0 $NumberOfMolecules Index
	mol off $NumberOfMolecules
	set NumberOfMolecules [expr $NumberOfMolecules + 1]
    }
}



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

