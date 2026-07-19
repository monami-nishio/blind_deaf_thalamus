# %%
import os 
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from scipy.spatial.distance import cdist

# %% additional preprocessing after fmriprep before fingerprint analysis
# do it for cortex / thalamus for each hemi separately
# 1. smooth with 2mm sigma gaussian kernel within the mask (provided in atlas folder)
# 2. linear detrend
# 3. zscore across all timepoints
# 4. concatenate all timepoints across all runs for each subject
# 5. optional for roi level data (i.e., cortex), average across all voxels within the roi
# 6. save the concatenated data as a numpy array

# %% set path and parameters
# --------------------------
# This cell should be the only part that needs to be changed
# --------------------------

# the root path of the dataset
dataset_root = '../Dataset/fingerprint_FC_dataset'  # change to your own path
indi_dir = os.path.join(dataset_root, 'indi_timeseries_Deaf')

for group in ['deaf','deaf_control']: 
    for hemi in ['lh', 'rh']:

        # 'source' in a fingerprint analysis refers to the data that is used as a reference.
        # 'target' in a fingerprint analysis refers to the data that is compared with the source.
        # In this case, the source is the cerebral cortex and the target is the thalamus,
        # which means we are trying to find the corresponding fingerprint of the thalamus in the cerebral cortex.
        # | Data format for both: numpy array, shape = (n_voxel/n_roi, n_timepoint)
        # | File naming format: make sure of sub-xxx_ as a prefix
        fingerprint_source_dataf = 'sub-01MN_func_resting_space-MNI152NLin2009cAsym_atlas-Schaefer400_hemi-'+hemi+'.npy' # change to your own file name
        fingerprint_target_dataf = 'sub-01MN_func_resting_space-MNI152NLin2009cAsym_atlas-Yeo-Thalamus_hemi-'+hemi+'.npy'  # change to your own file name
        #fingerprint_target_dataf = 'sub-eb01_func_judgement_01_space-MNI152NLin2009cAsym_atlas-THOMAS_hemi-'+hemi+'.npy' # change to your own file name
        source_dataf_tpl = os.path.join(indi_dir, fingerprint_source_dataf)
        target_dataf_tpl = os.path.join(indi_dir, fingerprint_target_dataf)

        # subject list which list all the subjects, which will be used to match the source and target data
        # | File format: one column, no header
        sublist_f = os.path.join(dataset_root, 'Deaf_'+group+'_subjects')
        sublist = pd.read_csv(sublist_f, sep='\t', names=['sub'], dtype=str)

        # the fingerprint FC will be saved as a numpy array in the following directory after the analysis
        save_dir = os.path.join(dataset_root, 'result_blinddeaf')

        # %% fingerprint correlation
        # 1. get the mean fc fingerprint source across all subjects
        sub_source = []
        fc_source = []
        for subid in sublist['sub']:
            source_dataf_sub = source_dataf_tpl.replace('sub-01MN', subid)
            target_dataf_sub = target_dataf_tpl.replace('sub-01MN', subid)
            if (not os.path.exists(source_dataf_sub)) or (not os.path.exists(target_dataf_sub)):
                continue

            # load data
            source_data = np.load(source_dataf_sub)

            # calculate FC
            fci = 1 - cdist(source_data, source_data, 'correlation')
            fc_source.append(fci)
            sub_source.append(subid)

        np.save(os.path.join(save_dir, group + '_fc_source'+hemi+'_Schaefer2YeoThalamus.npy'), fc_source)
        fc_source = np.sum(fc_source, axis=0)
        print('Step 1 Done.')

        #  2. leave one out cc-cc fingerprint
        fc_target = []
        fc_fingerprint = 0
        fc_fingerprints = []
        for i, subid in enumerate(sub_source):
            source_dataf_sub = source_dataf_tpl.replace('sub-01MN', subid)
            target_dataf_sub = target_dataf_tpl.replace('sub-01MN', subid)

            # load data
            source_data = np.load(source_dataf_sub)
            target_data = np.load(target_dataf_sub)
            print(target_data.shape)
            fc_targeti = 1 - cdist(target_data, source_data, 'correlation')
            fc_target.append(fc_targeti)
            # leave one out fc_source
            fc_sourcei = 1 - cdist(source_data, source_data, 'correlation')
            fc_source_loo = (fc_source - fc_sourcei) / (len(sub_source) - 1)
            # spearman correlation
            fc_source_loo = stats.rankdata(fc_source_loo, axis=-1)
            fc_targeti = stats.rankdata(fc_targeti, axis=-1)

            # fingerprint FC
            fc_fp = 1 - cdist(fc_targeti, fc_source_loo, 'correlation')
            fc_fingerprint += fc_fp
            fc_fingerprints.append(fc_fp)

        np.save(os.path.join(save_dir, group + '_fc_target'+hemi+'_Schaefer2YeoThalamus.npy'), fc_target)
        np.save(os.path.join(save_dir, group + 'source_'+group+'target_individual_fingerprint_fc_'+hemi+'_Schaefer2YeoThalamus.npy'), fc_fingerprints)
        fc_fingerprint /= len(sub_source)
        print('Step 2 Done.')

        # 3. save the fingerprint
        np.save(os.path.join(save_dir, group + 'source_'+group+'target_fingerprint_fc_'+hemi+'_Schaefer2YeoThalamus.npy'), fc_fingerprint)