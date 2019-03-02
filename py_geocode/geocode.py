import csv
import os

import geocoder

datadir =  os.path.abspath(os.path.join(__file__ ,"../..", 'data'))

inpath = os.path.join(datadir, 'violations_jan2.csv')
outpath = os.path.join(datadir, 'violations_jan2_gc.csv')

with open(inpath, 'r') as csvfile:
    with open(outpath, 'wb') as outfile:
        jan2csv = csv.DictReader(csvfile)
        outfields = jan2csv.fieldnames + ['ZIP'] + ['LAT'] + ['LON']
        outcsv = csv.DictWriter(outfile, outfields)
        outcsv.writeheader()
        for row in jan2csv:
            address = ' '.join([row['ADDRESS'], row['CITY'], row['STATE']])
            g = geocoder.osm(address)
            if g.ok:
                print address, g.postal
                row['LAT'] = g.y
                row['LON'] = g.x
                row['ZIP'] = g.postal
                outcsv.writerow(row)
