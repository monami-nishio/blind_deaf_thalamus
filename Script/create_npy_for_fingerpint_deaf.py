from nilearn.input_data import NiftiLabelsMasker
from nilearn import datasets
import nibabel as nib
import pandas as pd
import os
import glob
import shutil
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
from nilearn.image import resample_to_img
from collections import defaultdict

func_files = glob.glob("../Dataset/deaf/fmriprep/sub-*/func/sub-*_task-resting_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz")

#thalamus_mask = nib.load('../Dataset/deaf/template/atlas/THOMAS_mask_Deaf.nii.gz')
thalamus_mask = nib.load('../Dataset/template/ThalamusParcellation/1000subjects_TightThalamus_clusters014_ref_deaf.nii.gz')
thalamus_mask_data = thalamus_mask.get_fdata()
schaefer = NiftiLabelsMasker(labels_img='../Dataset/template/atlas_Schaefer2018_400Parcels_17Networks_order_FSLMNI152_2mm_Deaf.nii.gz', standardize=True)
Wang = NiftiLabelsMasker(labels_img="../Dataset/template/Wang_maxprob_surf_both_extended_roionly_deaf.nii.gz", standardize=True)
Julich = NiftiLabelsMasker(labels_img='../Dataset/template/JulichBrainAtlas_3.0_areas_MPM_b_N10_nlin2ICBM152asym2009c_public_Deaf.nii.gz', standardize=True)
for func_file in func_files:
    print(func_file)
    sub = func_file.split('/')[-3]
    ses = func_file.split('/')[-2]
    task = os.path.basename(func_file).split('task-')[1].split('_')[0]
    #if not os.path.exists(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-Wang_hemi-rh.npy'):
    #print(sub, ses)
    func_img = nib.load(func_file)
    func_data = func_img.get_fdata() 
    #right_mask = (thalamus_mask_data >= 1) & (thalamus_mask_data < 14)
    #left_mask = (thalamus_mask_data >= 15) & (thalamus_mask_data < 28)
    #left_mask = (thalamus_mask_data >= 1) & (thalamus_mask_data < 8)
    #right_mask = (thalamus_mask_data >= 8) & (thalamus_mask_data < 15)   
    # Thalamus label per voxel
    #flat_mask = thalamus_mask_data.flatten()
    #right_mask = (flat_mask >= 8) & (flat_mask < 15)
    #left_mask = (flat_mask >= 1) & (flat_mask < 8)
    #right_labels = flat_mask[right_mask].astype(int)  # values 1–13
    #left_labels = flat_mask[left_mask].astype(int)    # values 14–27
    #np.save('/mnt/DataDrive3/NishioM/Blind/derivatives/yeo_thalamus_right_labels_Deaf.npy', right_labels)
    #np.save('/mnt/DataDrive3/NishioM/Blind/derivatives/yeo_thalamus_left_labels_Deaf.npy', left_labels)
    # Extract left thalamus
    #right_ts = func_data[right_mask]  # shape: (n_voxels_right, T)
    #left_ts = func_data[left_mask]
    # Detrend and z-score each voxel (per row)
    #left_ts = scipy.signal.detrend(left_ts, axis=1)
    #left_ts = scipy.stats.zscore(left_ts, axis=-1, nan_policy='omit')
    #right_ts = scipy.signal.detrend(right_ts, axis=1)
    #right_ts = scipy.stats.zscore(right_ts, axis=-1, nan_policy='omit')
    #print(left_ts.shape, right_ts.shape)
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-Yeo-Thalamus_hemi-lh.npy', left_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-Yeo-Thalamus_hemi-rh.npy', right_ts)
    # Schaefer
    #time_series = schaefer.fit_transform(func_file)
    #time_series = time_series.T
    #time_series = scipy.signal.detrend(time_series, axis=-1)
    #time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    # Split hemispheres
    #lh_ts = time_series[:200, :]  # left hemisphere
    #rh_ts = time_series[200:, :]  # right hemisphere
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-Schaefer400_hemi-lh.npy', lh_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-Schaefer400_hemi-rh.npy', rh_ts)
    # MMP
    #time_series = MMP.fit_transform(func_file)
    #time_series = time_series.T
    #time_series = scipy.signal.detrend(time_series, axis=-1)
    #time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    # Split hemispheres
    #lh_ts = time_series[180:, :] 
    #rh_ts = time_series[:180, :]
    #print(lh_ts.shape, rh_ts.shape)
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-MMP_hemi-lh.npy', lh_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-MMP_hemi-rh.npy', rh_ts)
    time_series = Wang.fit_transform(func_file)
    #time_series = Julich.fit_transform(func_file)
    time_series = time_series.T
    time_series = scipy.signal.detrend(time_series, axis=-1)
    time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    # Split hemispheres
    lh_ts = time_series[25:, :] 
    rh_ts = time_series[:25, :]
    #lh_ts = time_series[:156, :] 
    #rh_ts = time_series[156:, :]
    #print(lh_ts.shape, rh_ts.shape)
    # Save
    np.save(f'../Dataset/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-originalWang_hemi-lh.npy', lh_ts)
    np.save(f'../Dataset/fingerprint_FC_dataset/indi_timeseries_Deaf/{sub}_{ses}_{task}_space-MNI152NLin2009cAsym_atlas-originalWang_hemi-rh.npy', rh_ts)