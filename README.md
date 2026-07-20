# Primary and higher-order thalamic nuclei make distinct contributions to cortical reorganization in congenital sensory loss

## About
This repository contains the code and metadata supporting the study  
*"Primary and higher-order thalamic nuclei make distinct contributions to cortical reorganization in congenital sensory loss"*, posted in bioArxiv.

## Dataset (`/Dataset`)
The datasets are too large to be stored on GitHub. They are available on Zenodo DOI: **[10.5281/zenodo.21456505]**.

| Folder     | Description                         |
|------------|------------------------------|
| **blind**  | Participant information for the blind dataset                  | 
| **deaf** | Participant information for the deaf dataset                | 
| **template**  | Templates used in the study                   | 
| **fingerprint_FC_dataset**  | Time series and functional connectivity fingerprints computed for both the blind and deaf datasets     |

## How to Run (`/Script`)
| File     | Description                          |
|------------|------------------------------|
| `calculate_deformation_wholebrain`    | Calculate Jacobian deformation maps by registering each individual's T1-weighted image to the template space.                 | 
| `run_preprocessing_pipeline`   | Run the fMRIPrep preprocessing pipeline.           | 
| `wang_schaefer_overlap`   | Extract Schaefer400 parcels that overlap with the Wang or Julich atlas.               | 
| `summarize_freesurfer`   | Extract structural features from FreeSurfer outputs.       | 
| `create_npy_for_fingerprint`   | Create NumPy (.npy) files for functional fingerprint analysis.        | 
| `fingerprint_FC`    | Calculate functional connectivity fingerprints.               | 

## How to Run (`/Code`)
To reproduce the figures:

- **Figure 1** – `Fig1,6_thalamus_structural`, `Fig1,6_cortex_structural`, `Fig1_thalamus_cortex_structural`
- **Figure 2** – `Fig2_cortex_structural_hierarchy`  
- **Figure 3** – `Fig3,6_thalamus_fingerprint_yeothalamus`, `Fig3,6_thalamus_fingerprint_nuclei`, `Fig3,6_cortex_fingerprint`  
- **Figure 4** – `Fig4_cortex_fingerprint_hierarchy`
- **Figure 5** – `Fig5_thalamus_cortex_fingerprint_task`
- **Figure 6** – `Fig1,6_thalamus_structural`, `Fig1,6_cortex_structural`,`Fig3,6_thalamus_fingerprint_yeothalamus`,`Fig3,6_thalamus_fingerprint_nuclei`, `Fig3,6_cortex_fingerprint`  

All necessary data for running these scripts are stored in `/Dataset` or in `/Derivatives`.
