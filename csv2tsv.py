#!/usr/bin/python3

import sys, csv

if len(sys.argv) < 3:
    print("USAGE:", sys.argv[0],"IN_CSV OUT_TSV")
    exit(1)


with open( sys.argv[2], 'w', newline='') as w:
    writer = csv.writer( w, delimiter='\t', quotechar='"')
    with open( sys.argv[1], newline='' ) as r:
        reader = csv.reader(r, dialect='excel')
        headline = next(reader)
        markers = []
        for h in headline:
            markers.append( h.strip().replace(' ', '_' ) )
        writer.writerow( markers )
        for row in reader:
            writer.writerow(row)
            
