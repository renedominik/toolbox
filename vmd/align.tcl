# compute the transformation matrix 
set reference_sel [atomselect 9 "backbone and resid 4 to 10"] 
set comparison_sel [atomselect 1 "backbone and resid 4 to 10"] 
set transformation_mat [measure fit $comparison_sel $reference_sel]

# apply it to all of the molecule 1 
set move_sel [atomselect 1 "all"] 
$move_sel move $transformation_mat

