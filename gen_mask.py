#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Given a Neurosynth association test map and a known cluster number (from visual inspection), generate a weighted mask that excludes this cluster.")
parser.add_argument(dest='nsynth', metavar='PATH', type=str, help="Path to Neurosynth .nii.gz")
parser.add_argument(dest='clust', metavar='INT', type=int, help="Cluster label to exclude (integer)")
parser.add_argument(dest='out', metavar='OUTPUT', type=str, help="Output")
parser.add_argument("--inspect", help="Use this flag the first time you run the script to determine the cluster of interest", action="store_true")
args = parser.parse_args()

import nibabel as nib
from nilearn.regions import connected_label_regions
from nilearn.image import math_img

#Load neurosynth z-scores
ment = nib.load(args.nsynth)
ment_bin = math_img("img > 0", img = ment)
cr = regions.connected_label_regions(ment_bin, min_size = 100)

#Save and manually inspect clusters (to find dmPFC in this case, which is 17)
if args.inspect:
    nib.save(cr, "clust_for_inspection.nii.gz")

#Remove desired cluster and binarize remaining clusters
else:
    dmpfc = math_img("img == {}".format(args.clust), img = cr)
    dmpfc = math_img("img > 0", img = dmpfc)
    cr = math_img("img > 0", img = cr)
    bin_no_dmpfc = math_img("img1 - img2", img1 = cr, img2 = dmpfc)

    #Save network mask
    nib.save(bin_no_dmpfc, args.out)
