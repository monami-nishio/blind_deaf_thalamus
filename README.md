# Primary and higher-order thalamic nuclei make distinct contributions to cortical reorganization in congenital sensory loss

## About
This repository contains the code and metadata supporting the study  
*"Primary and higher-order thalamic nuclei make distinct contributions to cortical reorganization in congenital sensory loss"*, posted in bioArxiv.

## Dataset (`/Dataset`)
The datasets are too large to be stored on GitHub. They are available on Zenodo: **[https://zenodo.org/uploads/16877128]**.

| Folder     | Description                         |
|------------|------------------------------|
| **blind**  | Participant information for the blind dataset                  | 
| **deaf** | Participant information for the deaf dataset                | 
| **template**  | Templates used in the study                   | 
| **fingerprint_FC_dataset**  | Time series and functional connectivity fingerprints computed for both the blind and deaf datasets     |

## How to Run (`/Script`)
| File     | Description                          |
|------------|------------------------------|
| `calculate_deformation_wholebrain`    | Calculate Jacobian deformation from individual T1w to Template space                  | 
| `run_preprocessing_pipeline`   | Run fmriprep for preprocessing             | 
| `wang_schaefer_overlap`   | Extract the Schaefer400 parcels which overlap with Wang (or Julich) atlas               | 
| `summarize_freesurfer`   | Extract structural features from Freesurfer outputs          | 
| `create_npy_for_fingerprint`   | Creat npy for which is used for funcitonal finerprint analysis         | 
| `fingerprint_FC`    | Calculate the funcitonal finerprint                 | 

## How to Run (`/Code`)
To reproduce the figures:

- **Figure 1** – `Fig1,6_thalamus_structural`, `Fig1,6_cortex_structural`, `Fig1_thalamus_cortex_structural`
- **Figure 2** – `Fig2_cortex_structural_hierarchy`  
- **Figure 3** – `Fig3,6_thalamus_fingerprint_yeothalamus`, `Fig3,6_thalamus_fingerprint_nuclei`, `Fig3,6_cortex_fingerprint`  
- **Figure 4** – `Fig4_cortex_fingerprint_hierarchy`
- **Figure 5** – `Fig5_thalamus_cortex_fingerprint_task`
- **Figure 6** – `Fig1,6_thalamus_structural`, `Fig1,6_cortex_structural`,`Fig3,6_thalamus_fingerprint_yeothalamus`, `Fig3,6_thalamus_fingerprint_nuclei`, `Fig3,6_cortex_fingerprint`  

All necessary data for running these scripts are stored in `/Dataset` or in `/Derivatives`.
