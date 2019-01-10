import os
import sys
from argparse import ArgumentParser
import nibabel as nib
import numpy as np
import pickle as pkl

class Converter:

    def __init__(self, input, output, t_in, t_out, s):
        self.input = input
        self.output = output
        self.t_in = t_in
        self.t_out = t_out
        self.s = s

    def run(self):
        typestr = ".%s" % t_in
        for root, dirs, files in os.walk(self.input):
            structure = ''
            if self.s:
                structure = os.path.join(self.output, root[len(self.input)+1:])
                if not os.path.isdir(structure):
                    os.mkdir(structure)
            for fn in files:
                if typestr in fn:
                    print('Converting %s' % fn)
                    outpath = output
                    if self.s:
                        outpath = structure
                    outstr = os.path.join(outpath, '%s.pkl' % fn[0:-4])
                    f = open(outstr, 'wb')
                    img = nib.load(os.path.join(root, fn))
                    if self.t_in == 'nii':
                        #get nifti image arrays
                        pass
                    else:
                        arrs = img.darrays
                        for v in arrs:
                            a = np.array(v.data)
                            pkl.dump(a, f)
                        f.close()
                        print('Wrote data to %s' % outstr)

#entry point
if __name__ == "__main__":
    parser = ArgumentParser(description='')
    parser.add_argument('--input', help='input path')
    parser.add_argument('--output', help='output path')
    parser.add_argument('--t_in', help='input type (nii, gii)')
    parser.add_argument('--t_out', help='output type (np)')
    parser.add_argument('--struct', help='maintain folder structure from input path', action='store_true')
    args = parser.parse_args()

    print('--------------------------------------------------\n')
    print('\t\t   fMRI2mat')
    print('\tTarrlab @ Carnegie Mellon University\n')
    print('--------------------------------------------------\n')

    input = args.input
    output = args.output
    t_in = args.t_in
    t_out = args.t_out
    s = False
    if args.struct:
        s = True

    conv = Converter(input, output, t_in, t_out, s)
    print('Extracting data from %s files in %s, writing to %s as %s' % (t_in, input, output, t_out))
    conv.run()
