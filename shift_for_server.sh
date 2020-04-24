#!/bin/tcsh
awk '{if ( $0 ~ "position" ) {print substr ( $0,0,19 ) sprintf ("%4d",substr ( $0,20,4 ) + '"$2"' ) substr ( $0,24,1000 ) ; } else {print ; }}' $1
