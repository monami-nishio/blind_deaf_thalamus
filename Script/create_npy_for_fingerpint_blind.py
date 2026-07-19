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

func_files = glob.glob("../Dataset/blind/fmriprep/sub-*/func/sub-eb*_task-resting_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz") #task-judgement_run-*_

#thalamus_mask = nib.load('../Dataset/blind/template/atlas/THOMAS_mask_resampled.nii.gz')
thalamus_mask = nib.load('../Dataset/template/ThalamusParcellation/1000subjects_TightThalamus_clusters014_ref_resampled_blind.nii.gz')
#thalamus_pilot_mask = nib.load('../Dataset/blind/template/atlas/THOMAS_mask_pilot_resampled.nii.gz')
thalamus_mask_data = thalamus_mask.get_fdata()
#thalamus_pilot_mask_data = thalamus_pilot_mask.get_fdata()
schaefer = NiftiLabelsMasker(labels_img='../Dataset/template/atlas_Schaefer2018_400Parcels_17Networks_order_FSLMNI152_2mm_resampled.nii.gz', standardize=True)
masker = NiftiLabelsMasker(labels_img='../Dataset/template/Wang_maxprob_surf_both_extended_roionly_Italy.nii.gz', standardize=True)
Julich = NiftiLabelsMasker(labels_img='../Dataset/template/JulichBrainAtlas_3.0_areas_MPM_b_N10_nlin2ICBM152asym2009c_public_Blind.nii.gz', standardize=True)
for func_file in func_files:
    sub = func_file.split('/')[-3]
    print(sub)
    ses = func_file.split('/')[-1].split('_')[1]
    run = func_file.split('/')[-1].split('_')[2]
    #if not os.path.exists(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Schaefer400_hemi-rh.npy'):
    func_img = nib.load(func_file)
    func_data = func_img.get_fdata() 
    #print(func_data.shape)
    #if 'pilot' in sub:
    #    right_mask = (thalamus_pilot_mask_data >= 1) & (thalamus_pilot_mask_data < 14)
    #    left_mask = (thalamus_pilot_mask_data >= 15) & (thalamus_pilot_mask_data < 28)
    #else:
    #    right_mask = (thalamus_mask_data >= 1) & (thalamus_mask_data < 14)
    #    left_mask = (thalamus_mask_data >= 15) & (thalamus_mask_data < 28)   
    #left_mask = (thalamus_mask_data >= 1) & (thalamus_mask_data < 8)
    #right_mask = (thalamus_mask_data >= 8) & (thalamus_mask_data < 15)    
    #print(np.sum(left_mask), np.sum(right_mask))
    # Thalamus label per voxel
    #flat_mask = thalamus_mask_data.flatten()
    #right_mask = (flat_mask >= 8) & (flat_mask < 15)
    #left_mask = (flat_mask >= 1) & (flat_mask < 8)
    #right_labels = flat_mask[right_mask].astype(int)  # values 1–13
    #left_labels = flat_mask[left_mask].astype(int)    # values 14–27
    #np.save('/mnt/DataDrive3/NishioM/Blind/derivatives/yeo_thalamus_right_labels_Italy.npy', right_labels)
    #np.save('/mnt/DataDrive3/NishioM/Blind/derivatives/yeo_thalamus_left_labels_Italy.npy', left_labels)
    #right_ts = func_data[right_mask]  # shape: (n_voxels_right, T)
    #left_ts = func_data[left_mask]
    # Detrend and z-score each voxel (per row)
    #left_ts = scipy.signal.detrend(left_ts, axis=1)
    #left_ts = scipy.stats.zscore(left_ts, axis=-1, nan_policy='omit')
    #right_ts = scipy.signal.detrend(right_ts, axis=1)
    #right_ts = scipy.stats.zscore(right_ts, axis=-1, nan_policy='omit')
    #print(left_ts.shape, right_ts.shape)
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Yeo-Thalamus_hemi-lh.npy', left_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Yeo-Thalamus_hemi-rh.npy', right_ts)
    # Cortical Mask
    #if 'pilot' in sub:
    #    time_series = pilot_masker.fit_transform(func_file)
    #else:
    time_series = masker.fit_transform(func_file)
    time_series = time_series.T
    time_series = scipy.signal.detrend(time_series, axis=-1)
    time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    # Split hemispheres
    lh_ts = time_series[25:, :]  # left hemisphere
    rh_ts = time_series[:25, :]  # right hemisphere
    #print(lh_ts.shape, rh_ts.shape)
    # Save
    np.save(f'../Dataset/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-originalWang_hemi-lh.npy', lh_ts)
    np.save(f'../Dataset/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-originalWang_hemi-rh.npy', rh_ts)
    # MMP
    #if 'pilot' in sub:
    #    time_series = pilot_MMP.fit_transform(func_file)
    #else:
    #    time_series = MMP.fit_transform(func_file)
    #time_series = time_series.T
    #time_series = scipy.signal.detrend(time_series, axis=-1)
    #time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    # Split hemispheres
    #lh_ts = time_series[180:, :]  # left hemisphere
    #rh_ts = time_series[:180, :]  # right hemisphere
    #print(lh_ts.shape, rh_ts.shape)
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-MMP_hemi-lh.npy', lh_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-MMP_hemi-rh.npy', rh_ts)
    # Schaefer
    #if 'pilot' in sub:
    #    time_series = pilot_Schaefer.fit_transform(func_file)
    #else:
    #    time_series = schaefer.fit_transform(func_file)
    #time_series = time_series.T
    #time_series = scipy.signal.detrend(time_series, axis=-1)
    #time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    # Split hemispheres
    #lh_ts = time_series[:200, :]  # left hemisphere
    #rh_ts = time_series[200:, :]  # right hemisphere
    #print(lh_ts.shape, rh_ts.shape)
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Schaefer400_hemi-lh.npy', lh_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Schaefer400_hemi-rh.npy', rh_ts)
    #time_series = Julich.fit_transform(func_file)
    #time_series = time_series.T
    #time_series = scipy.signal.detrend(time_series, axis=-1)
    #time_series = scipy.stats.zscore(time_series, axis=-1, nan_policy='omit')
    ## Split hemispheres
    #lh_ts = time_series[:157, :] 
    #rh_ts = time_series[157:, :]
    #print(lh_ts.shape, rh_ts.shape)
    # Save
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Julich_hemi-lh.npy', lh_ts)
    #np.save(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Julich_hemi-rh.npy', rh_ts)
    #print(f'/mnt/DataDrive3/NishioM/Blind/derivatives/fingerprint_FC_dataset/indi_timeseries_Italy/{sub}_{ses}_{run}_space-MNI152NLin2009cAsym_atlas-Julich_hemi-lh.npy')
