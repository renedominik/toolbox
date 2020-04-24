#!/usr/bin/python


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################



import sys, os
import Bio.PDB
import numpy as np

types = {
    'positive': ["ARG","LYS"], #,"HIS"],
    'negative': ["ASP","GLU"],
    'polar':["SER","THR","ASN","GLN"],
    'special':["CYS","SEC","GLY","PRO"],
    'hydrophobic':["ALA","VAL","ILE","LEU","MET","PHE","TYR","TRP"],
    'aromatic':["PHE","TYR","TRP"], #,"HIS"],
    'donor':["ARG","ASN","GLN","LYS","SER","THR","TRP","TYR"], #,"HIS"],
    'acceptor':["ASN","ASP","CYS","GLN","GLU","MET","SER","THR","TYR"], #,"HIS"],
    #'helix':["ALA","ARG","GLN","GLU","LEU","LYS","MET","PHE"] # Deleage > 1.1
    #'helix':["ALA","CYS","GLN","GLU","HIS","LEU","LYS","MET"] # LEVIT > 1.1
    'helix':["ALA","GLN","GLU","LEU","LYS","MET"], # LEVIT > 1.1 & Deleage > 1.1
    'his_pos_aro_don_acc':["HIS"]
    }



def Type( residue ):
    t = ""
    for typ,res in types.iteritems():
        if residue in res:
            if len(t) > 0:
                t += "_"
            t += typ
    return t



                
    

def Analyse( files , chain , bins  ):
    pdb_parser = Bio.PDB.PDBParser( QUIET=True )

    data = []

    print "analyse: ",len(files), chain, bins
    ii = 0
    for f in files:
        if ii % 25 == 0:
            print ii,
            sys.stdout.flush()
        ii += 1
        
        structure = pdb_parser.get_structure( f, f )[0]
        others = []
        ligand = ""
        
        for c in structure:
            if c.get_id() == chain:
                ligand = c
            else:
                others.append(c)
        length = len(ligand)
        #print length

        if length == 0:
            print "no ligand found"

        count = 0

        for r1 in ligand:

            pos = []
            neg = []
            pho = []
            pol = []
            aro = []
            acc = []
            his = []
            
            if len(data) < length:
                data.append([ r1.get_resname() , Type(r1.get_resname()) , [] , [] , [] , [] , [] , [], [] ] )
                
            for c in others:
                for r2 in c:
                    d = ShortestDistance( r1,r2 )
                    #print "shortest:", d, bins[-1]
                    if d == None or d > bins[-1]:
                        continue
                    t = Type( r2.get_resname() )
                    #print r1.get_resname(), count, r2.get_resname(), t, d
                    if "positive" in t:
                        pos.append( d )
                    elif "negative" in t:
                        neg.append( d )
                    elif "polar" in t:
                        pol.append( d )
                    elif "hydrophob" in t:
                        pho.append( d )
                        
                    if "aromatic" in t:
                        aro.append( d )
                    if "accept" in t:
                        acc.append( d )
                    if "his" in t:
                        his.append( d )
                        
            #print "###", count, len( data)
            
            data[count][2].extend(pos)  
            data[count][3].extend(neg)  
            data[count][4].extend(pho)  
            data[count][5].extend(pol)  
            data[count][6].extend(aro)  
            data[count][7].extend(acc)
            data[count][8].extend(his)
            
            count += 1

    for i in range( 0, length ):
        for j in range(2,9):
            h = np.histogram( np.array(data[i][j]) , bins )[0] # , density=True )[0]
            data[i][j] = h
    return data

def Score( name , typ ):
    with open(name) as f:
        for l in f:
            if typ in l:
                return float(l.split()[-1])
    return None

def ShortestDistance( r1 , r2 ):
    maximum = 25
    minimum = 1e12
    types = ['C','CA','O','N', 'HA', 'H' ]
    for a1 in r1:
        if a1.get_name() in types: continue
        for a2 in r2:
            if a2.get_name() in types: continue
            d = a2 - a1
            if d < minimum:
                minimum = d
            elif d > maximum:
                return 
    return minimum


directory = sys.argv[1]
prefix = sys.argv[2]
first = int( sys.argv[3] )  # cluster id
last = int( sys.argv[4] )
suffix = sys.argv[5]
chain = sys.argv[6]
 

# dir/prefix.first.1.pdb  # first element in cluster
if directory[-1] == '/':
    directory = directory[:-1]
    
out = open( directory + ".tex", 'w')
out.write( '\\documentclass{article}\n' )
out.write( '\\usepackage{graphicx}\n' )
out.write( '\\usepackage{pgfplots}\n' )
out.write( '\\pagenumbering{gobble}\n' )
out.write( '\\begin{document}\n' )

if not os.path.exists( directory + '/img' ):
    os.makedirs( directory + '/img' )
if not os.path.exists( directory + '/chains' ):
    os.makedirs( directory + '/chains' )

out.write( '\\section{Contact map} \n\n')
out.write( 'Contact map of all poses, ligand versus receptor, transition count funtion, contacts smaller 4A are scored 1, contacts with smallest distance larger 12 are scored 0, in between cos transitions. Second images uses 3A and 9A. Third 2A and 8A. Last image in this section shows secondary structure and exposure.  \\\\ \n\n')
out.write( '\\includegraphics[width=\\linewidth]{models/heatmap.pdf}\n' )
out.write( '\\includegraphics[width=\\linewidth]{models/contactmap_3_9.pdf}\n' )
out.write( '\\includegraphics[width=\\linewidth]{models/contactmap_2_8.pdf}\n' )
out.write( '\\includegraphics[width=\\linewidth]{/home/hildilab/projects/peptide_gpcr/1_gpcr/kappa_mu_delta_msa2.png}\n' )

out.write( '\\includegraphics[width=\\linewidth]{models/contactmap_2_8_sub1.pdf}\n' )
out.write( '\\includegraphics[width=\\linewidth]{models/contactmap_2_8_sub2.pdf}\n' )
out.write( '\\includegraphics[width=\\linewidth]{models/contactmap_2_8_sub3.pdf}\n' )


work_dir = os.getcwd()
print "work dir", work_dir
if "6dde" in work_dir:
    name = "6dde"
elif "6b73" in work_dir:
    name = "6b73"
else:
    name = "undefined"
    
out.write( '\\includegraphics[width=\\linewidth]{../../' + name + '.pdf}\n' )
out.write( '\\newpage \n\n')



out.write( '\\section{Cluster centers: ' + str(first) + ' ' + str(last) + '} \n\n')

vmd = "vmd -dispdev none -e ~/projects/peptide_gpcr/dev/vmd/render.vmd -args "

name = "cluster_centers"
if not os.path.isfile(  directory + "/img/cluster_centers_top.png") or not  os.path.isfile(  directory + "/img/cluster_centers_side.png"):
    
    cmd = vmd
    ###  medusa pic of cluster centers:  ###
    for nr in range(first,last+1):
        name = "." + str(nr) + ".1.pdb"                # cluster center
        for f in os.listdir( directory):
            if name in f:
                cmd += directory + '/' + f + " "  

    os.system( cmd)
    print ""
    print "vmd done" 
    print "convert"
    os.system( "convert scene_top.dat.tga " + directory + "/img/" + name + "_top.png")
    os.system( "convert scene_side.dat.tga " + directory + "/img/" + name + "_side.png")
    os.system( "echo convert done" )
    
print ""
out.write( '\n\n\\includegraphics[width=\\linewidth]{' + directory + '/img/' +name +'_top}\n' )
out.write( '\\includegraphics[width=\\linewidth]{' + directory + '/img/' +name +'_side}\n' )
out.write( "\\newpage\n")


    


###  per cluster analysis  ###
for nr in range(first,last+1):
    name = prefix + str(nr) + suffix
    print "now", name
    files = []
    scores = []
    cmd = vmd
    ii = 0
    for f in os.listdir( directory):
        if name in f:
            if not os.path.isfile(  directory + '/chains/' + f ):
                os.system( 'grep " B " ' + directory + '/' + f + ' > ' + directory + '/chains/' + f ) 
            files.append( directory + '/' + f)
            if ii == 0:
                cmd += directory + '/' + f + " "      
            else:
                cmd += directory + '/chains/' + f + " "
            ii += 1
            #scores.append( Score(  directory + '/' + f, "reweighted") )
    
    if len(files) == 0:
        continue
    
    name = name.replace('.','')
    if not os.path.isfile(  directory + "/img/" + name + "_top.png") or not  os.path.isfile(  directory + "/img/" + name + "_side.png"):
        os.system( cmd)
        print ""
        print "vmd done" 
        print "convert"
        os.system( "convert scene_top.dat.tga " + directory + "/img/" + name + "_top.png")
        os.system( "convert scene_side.dat.tga " + directory + "/img/" + name + "_side.png")
        os.system( "echo convert done" )
    print ""
    sys.stdout.flush()
    out.write( '\\section{Cluster: ' + str(nr) + '} \n\n')
    out.write( "Cluster size (number of models contained in cluster):  " + str(len(files)) + ' \\\\ \n \\\\ \n')
    out.write( "NOTE: counts in histograms are devided by cluster size!! \\\\ \\\\ \n")

    out.write( 'Type assignment of amino acids: \\\\ \n')
    out.write( '\\begin{tabular}{l l} \n')
    for k,v in types.iteritems():
        out.write( k.replace('_','\_') + ': & ')
        for x in v:
            out.write(x + ' ' )
        out.write('\\\\\n')
    out.write( '\\end{tabular} \n\n')
   
    if len(scores) > 0 and scores[0] != None:
        out.write( "minimum score: " + str(np.max( scores ) ) + ' \\\\ \n')
        out.write( "mean score:    " + str(np.mean(scores) ) + ' \\\\ \n')
        out.write( "stddev:        " + str(np.std(scores) ) + ' \\\\ \n')
        out.write( "maximum score: " + str(np.min(scores) ) + ' \\\\ \n')
    
    bins = range(0,11)
    print "Analyse..."
    residue_histograms = Analyse( files , chain , bins )

    out.write( '\\vspace{1cm}\\noindent\n' )
    out.write( 'Characterization of ligand sequence: \\\\ \n')
    out.write( '\\begin{tabular}{l l} \n')
    for r in  residue_histograms:
        out.write(  r[0] + ' & ' + r[1].replace("_","\_") + '\\\\ \n' )
    out.write( '\\end{tabular} \n')

    
    out.write( '\n\n\\includegraphics[width=\\linewidth]{' + directory + '/img/' +name +'_top}\n' )
    out.write( '\\includegraphics[width=\\linewidth]{' + directory + '/img/' +name +'_side}\n' )
    out.write( "\\newpage\n")

    
    out.write( '\\vspace*{-4.4cm} \\hspace{-4cm} \\begin{tabular}{ c | c c c c c c c}\n\\hline\n' )
    out.write( 'AA & positive & negative & hydrophobic  & polar & aromatic & acceptor & histidine \\\\ \n' )
    out.write( '\\hline\n')
    
    for rh in residue_histograms:
        out.write( '\\rotatebox{90}{' + rh[0] + '} & ' )
        rc = 0
        for hist in rh[2:]:
            out.write( '\\begin{tikzpicture}[scale=0.3]\n' )
            out.write( '\\begin{axis}[\n' )
            out.write( '    ymin=0, ymax=10,\n' )
            out.write( '    minor y tick num = 1,\n' )
            out.write( '    area style,\n' )
            out.write( ']\n' )
            out.write( '\\addplot+[ybar interval,mark=no] plot coordinates {' )
            for h,b in zip(hist,bins[:-1]):
                out.write( '(' + str(b) + ',' + str(h/float(len(files))) + ')' )
            out.write( '};\n' )
            out.write( '\\end{axis}\n' )
            out.write( '\\end{tikzpicture}' )
            rc += 1
            if rc < len(rh[2:]):
                out.write(' & \n')
            else:
                out.write( ' \\\\ \n' )

    out.write( "\\end{tabular}\n" )
    out.write( "\\newpage\n" )
        
out.write( '\\end{document}\n' )
out.close()
