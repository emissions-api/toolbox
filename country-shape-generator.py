import geojson
import shapefile
from pathlib import Path

# This is a python file that generates a country shape python file.
# The input file must provide the needed data naming that are used in
# https://www.naturalearthdata.com shape files.
fileName = "archive\\ne_110m_admin_0_countries.shp"

# load shapefile and get records
shape = shapefile.Reader(fileName)
records = shape.shapeRecords()

# open export file
export = open(fileName + ".py", "w")

# write header
export.writelines(['# flake8: noqa\n',
                   '# source-file: ' + Path(fileName).name + '\n',
                   '\n',
                   '# mapping from A2 to A3 names\n',
                   'country_A2_to_A3 = {\n'])

# write A2 to A3 table
for x in records:
    # read record as dict for easier access
    # e.g.does not chrash if key is not available
    dct = x.record.as_dict()

    # check if A2 is set. -99 is the 'not-set' value in the shp of naturalearth
    if dct.get('ISO_A2', '-99') != '-99':
        # if ISO A3 is not available, use US A3 version
        if dct.get('ISO_A3') != '-99':
            export.write(f'    \'{dct["ISO_A2"]}\':\'{dct["ISO_A3"]}\',\n')
        else:
            export.write(f'    \'{dct["ISO_A2"]}\':\'{dct["ADM0_A3_US"]}\',\n')
# write end of map
export.writelines(['}\n', '\n', 'country_A3_shape = {\n'])

# write country shape table with A3 as key
for x in records:
    # if ISO A3 is not available, use US A3 version
    if x.record['ISO_A3'] != '-99':
        export.write(f'    \'{x.record["ISO_A3"]}\':')
    else:
        export.write(f'    \'{x.record["ADM0_A3_US"]}\':')
    # write country name
    export.write(f'(\'{x.record["ADMIN"]}\',(')

    # export shape points
    array = []
    for p in x.shape.points:
        # append and limit the precision (to reduce file size)
        array.append("{0:.6f},{1:.6f}".format(p[0], p[1]))
    export.write(','.join(array))
    export.write(')),\n')

# write end of map and add tailing linefeed to file
export.writelines(['}\n'])
export.close()
