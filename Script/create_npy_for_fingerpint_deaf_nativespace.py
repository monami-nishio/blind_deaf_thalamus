from nilearn.input_data import NiftiLabelsMasker
from nilearn import datasets
import nibabel as nib
import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
from nilearn.image import resample_to_img

# Functional files
func_files = glob.glob(
    "../Dataset/deaf/fmriprep/sub-*/func/sub-*_task-resting_space-T1w_desc-preproc_bold.nii.gz"
)

output_dir = "../Dataset/fingerprint_FC_dataset/indi_timeseries_Deaf"
os.makedirs(output_dir, exist_ok=True)

for func_file in func_files:
    sub = func_file.split("/")[-3]
    ses = func_file.split("/")[-2]
    print(f"Processing {sub}, {ses}")
    if not os.path.exists(os.path.join(output_dir, f"{sub}_{ses}_space-MNI152NLin2009cAsym_atlas-nativespace_THOMAS_hemi-rh.npy")):

        # Subject-specific THOMAS mask
        mask_file = f"../Dataset/deaf/fmriprep/{sub}/anat/sthomas_LR_labels.nii.gz"
        if not os.path.exists(mask_file):
            print(f"⚠️  Mask not found for {sub}, skipping...")
            continue

        func_img = nib.load(func_file)
        mask_img = nib.load(mask_file)

        # Resample mask to functional space if needed
        if mask_img.shape != func_img.shape[:3]:
            print("Resampling mask to functional resolution...")
            mask_img = resample_to_img(mask_img, func_img, interpolation="nearest")

        func_data = func_img.get_fdata()
        mask_data = mask_img.get_fdata().astype(int)
        print(func_data.shape)

        # Define left/right masks based on label parity
        left_mask = np.isin(mask_data, np.arange(1, 39, 2))   # 1,3,5,...,37
        right_mask = np.isin(mask_data, np.arange(2, 39, 2))  # 2,4,6,...,38

        # Extract voxelwise time series (voxel × time)
        left_ts = func_data[left_mask, :]
        right_ts = func_data[right_mask, :]

        # Detrend and z-score each voxel (axis=1 = time)
        left_ts = scipy.signal.detrend(left_ts, axis=1)
        left_ts = scipy.stats.zscore(left_ts, axis=1, nan_policy='omit')
        right_ts = scipy.signal.detrend(right_ts, axis=1)
        right_ts = scipy.stats.zscore(right_ts, axis=1, nan_policy='omit')

        # --- Get voxelwise label arrays (to group later) ---
        left_labels = mask_data[left_mask]
        right_labels = mask_data[right_mask]

        # --- Save voxelwise time series ---
        np.save(
            os.path.join(output_dir, f"{sub}_{ses}_space-MNI152NLin2009cAsym_atlas-nativespace_THOMAS_hemi-lh.npy"),
            left_ts,
        )
        np.save(
            os.path.join(output_dir, f"{sub}_{ses}_space-MNI152NLin2009cAsym_atlas-nativespace_THOMAS_hemi-rh.npy"),
            right_ts,
        )

        # --- Save corresponding label arrays ---
        np.save(
            os.path.join(output_dir, f"{sub}_nativespace_thalamus_left_labels.npy"),
            left_labels
        )
        np.save(
            os.path.join(output_dir, f"{sub}_nativespace_thalamus_right_labels.npy"),
            right_labels
        )
        print(len(right_labels))

        print(f"✅ Saved left/right time series and label files for {sub}")

