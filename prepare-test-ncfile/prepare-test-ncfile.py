import netCDF4
import numpy
import sys

USED_VARS = set([
    'carbonmonoxide_total_column',
    'longitude',
    'latitude',
    'qa_value',
    'delta_time'])

def main():
    if len(sys.argv) != 3:
        print(f'{sys.argv[0]} infile outfile')
        sys.exit()
    infile = sys.argv[1]
    outfile = sys.argv[2]
    with netCDF4.Dataset(infile, 'r') as read_f:
        p_grp = read_f.groups['PRODUCT']
        with netCDF4.Dataset(outfile, 'w') as f:
            for attr in read_f.ncattrs():
                f.setncattr(attr, read_f.getncattr(attr))
            products = f.createGroup('/PRODUCT')
            for d in p_grp.dimensions.values():
                if d.name == 'scanline':
                    products.createDimension(d.name, 2)
                    print(f'importing dimension {d.name}(2) (was {d.size})')
                else:
                    products.createDimension(d.name, d.size)
                    print(f'importing dimension {d.name}({d.size})')

            for v in p_grp.variables.values():
                if v.name not in USED_VARS:
                    print(f'skipping {v.name}')
                    continue
                print(f'importing {v.name}({v.dtype, v.dimensions})')
                var = products.createVariable(v.name, v.dtype, v.dimensions)
                for a in v.ncattrs():
                    if not a.startswith('_'):
                        var.setncattr(a, v.getncattr(a))
                if v.dimensions[1] == 'scanline':
                    mid = int(len(v[0]) / 2)
                    print(f'slicing two scanline off at position {mid}')
                    var[:] = numpy.array([v[0][mid:mid+2]])
                else:
                    var[:] = v[:]
                #print(var[:][0])
                #print(len(var[:][0]))

if __name__ == '__main__':
    main()
