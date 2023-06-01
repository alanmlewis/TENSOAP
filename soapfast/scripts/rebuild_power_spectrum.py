#!/usr/bin/env python
import numpy as np
import sys
import argparse
import math
import time
from ase.io import read
from os import remove
from glob import glob

parser = argparse.ArgumentParser(description="Rebuild power spectrum from blocks.")
parser.add_argument("-lm",  "--lam", type=int, required=True,    help="Spherical tensor order.")
parser.add_argument("-c", "--coords", type=str, required=True, help="Coordinates file.")
parser.add_argument("-nb", "--nblocks",   type=int,   required=True, help="Number of blocks.")
parser.add_argument("-f", "--fname", type=str, default="slice",help="Input file prefix.")
parser.add_argument("-cl", "--cleanup", action='store_true', help="Clean up partial files.")
args = parser.parse_args()

lam = int(args.lam)
coords = str(args.coords)
nblocks = int(args.nblocks)
fname = str(args.fname)

all_coords = read(coords,':')
ndata = len(all_coords)

blocksize = int(math.ceil(float(ndata)/float(nblocks)))

# Put power spectra of individual blocks together into a single power spectrum
pslices = []
#natom_slices = []
natoms = []
for i in range(nblocks):
    pslices.append(np.load(fname + "_" + str(i) + ".npy"))
    natoms += list(np.load(fname + "_" + str(i) + "_natoms.npy"))
#    natom_slices.append(np.load(fname + "_" + str(i) + "_natoms.npy"))
    if args.cleanup:
        remove(fname + "_" + str(i) + ".npy")
        remove(fname + "_" + str(i) + "_natoms.npy")
        remove(glob("*_" + str(i) + ".xyz")[0])
	

power = np.vstack(pslices)
#natoms = np.vstack(natom_slices)
natoms = np.array(natoms)

np.save(fname + ".npy",power)
np.save(fname + "_natoms.npy",natoms)
