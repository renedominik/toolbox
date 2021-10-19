#!/usr/bin/python3

############### Made by Adam ######################

import os
import shutil

boolean = False

def current_path():
    return os.getcwd()

def move_dir(file_names, tomovedir):
    for dir in file_names:
        if dir != mvdir:
            shutil.move(os.path.join(current_path(), dir), os.path.join(current_path(), tomovedir))
        else:
            continue
    return 0

def make_dir(listofdir):
    for idx, var in enumerate(listofdir):
        if os.path.isdir(var) == True:
            boolean = True
            continue
        else:
            os.mkdir(var)
        if idx == 5:
            os.mkdir(os.path.join(var, 'clhood/'))
        if idx == 4:
            os.mkdir(os.path.join(var, 'clrmsd/'))
        if idx == 6:
            os.mkdir(os.path.join(var, 'rmsd/'))
    return 0

def copy_analysis_files(dir_of_files, list_of_files):
    for idx, var in enumerate(list_of_files):
        if idx == 0:
            shutil.copy(os.path.join(dir_of_files, var), os.path.join(current_path(), 'energy'))
        elif (idx == 1) or (idx == 2):
            shutil.copy(os.path.join(dir_of_files, '../clustering/', var), os.path.join(current_path(), 'clustering'))
        else:
            if boolean == False:
                shutil.copy(os.path.join(dir_of_files, '../../../compare_run_analysis/rmsd/', var), os.path.join(current_path(), '../../compare_run_analysis/rmsd/'))
            else:
                continue
    return 0

newdir = 'married/'
mvdir = 'con500/' #Trashpiledirectory
fildir = '/home/hildilab/projects/peptide_gpcr/1_gpcr/delta/6pt2/damgo/sims/run1/married/energy/'
anadir = ['clustering', 'energy', 'rmsdf', 'hood', 'clustering/clst', 'clustering/reclst', '../../compare_run_analysis'] #directories which are created for every analysis
anafiles = ['more_energy.sh', 'cl_neighborhood.sh', 'cl_rmsd.sh', 'mvav.sh']

if os.path.isdir(os.path.join(current_path(),newdir)) == True:
    os.chdir(newdir)
    file_names = os.listdir(current_path())
    if len(file_names) != 0:
        if os.path.isdir(os.path.join(current_path(),mvdir)) == False:
            os.mkdir(mvdir)
        move_dir(file_names, mvdir)
    make_dir(anadir)
    copy_analysis_files(fildir, anafiles)
else:
    os.mkdir(newdir)
    os.chdir(newdir)
    make_dir(anadir)
    copy_analysis_files(fildir, anafiles)

print("""Have fun analysing my dear friend! 

\"The surest sign that intelligent life exists elsewhere in the universe is that it has never tried to contact us.\" - Bill Waterson""")
