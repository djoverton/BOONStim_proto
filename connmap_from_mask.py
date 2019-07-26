#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="Generate correlation map in surface space, given a mean masked timeseries and functional data in surface space.")
parser.add_argument(dest='mean_ts', metavar='MEAN_TS', type=str, help="Path to mean timeseries .csv file.")
parser.add_argument(dest='clean_func', metavar='PATH', type=str, help="Path to cleaned functional data in surface space.")
parser.add_argument(dest='temp_surf', metavar='PATH', type=str, help="Path to placeholder surface file.")
parser.add_argument(dest='out_surf', metavar='OUT', type=str, help="Output correlation map surface file.")
args = parser.parse_args()

import nilearn as nil
import nibabel as nib
import pandas as pd
from nilearn import plotting
from nilearn import regions
from nilearn.regions import connected_regions
from nilearn.regions import connected_label_regions
from nilearn.image import math_img

#"mean_masked_timeseries_clean.csv"
masked = pd.read_csv(args.mean_ts, header=None)

#"rest_01_clean_leftcortex.func.gii"
func_surf = nib.load(args.clean_func)
rs = []
for f in func_surf.darrays:
    rs.append(f.data)

rs_all = np.array(rs)

all_correl = []
for rs_time in rs_all.transpose():
    all_correl.append(np.corrcoef(masked.transpose(), rs_time)[0][1])

#"surf/func_masked.func.gii"
tmp = nib.load(args.temp_surf)
tmp.darrays[0].data = np.array(all_correl, dtype=np.float32)
#"ment_corr2.func.gii"
nib.save(tmp, args.out_surf)
