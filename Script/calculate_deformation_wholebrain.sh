#!/bin/bash
#SBATCH --job-name=jacobian      # Job name
#SBATCH --output=jacobian_%j.out    # Standard output (%j expands to jobId)
#SBATCH --error=jacobian_%j.err     # Standard error
#SBATCH --time=120:00:00          # Time limit (hh:mm:ss)
#SBATCH --nodes=1                # Number of nodes
#SBATCH --ntasks=1               # Number of tasks
#SBATCH --cpus-per-task=8        # Number of CPU cores per task
#SBATCH --mem=65G                # Memory per node

# Set path to MNI template and atlas mask
#MNI_TEMPLATE="/mnt/DataDrive3/NishioM/Blind/template/MNI152_T1_1mm_brain.nii.gz"
MNI_TEMPLATE="../Dataset/template/tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w.nii.gz"
MNI_ROI_MASK="../Dataset/template/THOMAS_mask_resampled_thalamus.nii.gz"

# Set base directory
#BASEDIR="/mnt/DataDrive3/NishioM/Blind/derivatives/2023_Trento_plosBiology_YX_raw/fmriprep"
BASEDIR="../Dataset/deaf/fmriprep"

# Output summary files
ROI_RESULTS="roi_log_jacobian_summary.csv"
WHOLE_RESULTS="thalamus_log_jacobian_summary.csv"

echo "Subject,ROI,MeanLogJacobian" > $ROI_RESULTS
echo "Subject,MeanLogJacobian_AllROIs" > $WHOLE_RESULTS

# Number of ROIs (if used later)
N=28

# Global log directory
LOGDIR="log_jacobian"
mkdir -p $LOGDIR

# Loop over subjects
for subjdir in ${BASEDIR}/sub-K*; do
    [ -d "$subjdir" ] || continue

    subj=$(basename "$subjdir")
    echo "Processing $subj..."
    LOGFILE="${LOGDIR}/${subj}.log"
    if [ ! -f "${subjdir}/anat/log_jacobian_outputs/${subj}_to_MNI2009_Warped.nii.gz" ]; then 
        echo ">>> Processing subject: $subj"

        anatdir="${subjdir}/anat"
        T1="${anatdir}/${subj}_desc-preproc_T1w.nii.gz"
        BRAIN_MASK="${anatdir}/${subj}_desc-brain_mask.nii.gz"
        STRIPPED_T1="${anatdir}/${subj}_desc-brain_T1w.nii.gz"

        # === Create subfolder for output ===
        OUTDIR="${anatdir}/log_jacobian_outputs"
        mkdir -p "$OUTDIR"
        OUTPREFIX="${OUTDIR}/${subj}_to_MNI2009_"

        # Skull-strip T1 if needed
        if [ ! -f "$STRIPPED_T1" ]; then
            echo "Skull-stripping T1 image..."
            fslmaths "$T1" -mas "$BRAIN_MASK" "$STRIPPED_T1"
        fi

        # Run ANTs registration (native → MNI)
        echo "Running ANTs registration..."
        antsRegistrationSyN.sh -d 3 -f $MNI_TEMPLATE -m $STRIPPED_T1 -o $OUTPREFIX

        # Compute Jacobian (in MNI space)
        echo "Creating Jacobian determinant image..."
        CreateJacobianDeterminantImage 3 \
            ${OUTPREFIX}1Warp.nii.gz \
            ${OUTDIR}/${subj}_log_jacobian.nii.gz \
            1

        # Mask with thalamus ROI in MNI space
        echo "Masking Jacobian in MNI space..."
        fslmaths ${OUTDIR}/${subj}_log_jacobian.nii.gz \
            -mas $MNI_ROI_MASK \
            ${OUTDIR}/${subj}_log_jacobian_masked.nii.gz

        # Optionally calculate stats
        #mean_val=$(fslstats ${OUTDIR}/${subj}_log_jacobian_masked.nii.gz -M)
        #echo "${subj},${mean_val}" >> $WHOLE_RESULTS
        echo "✅ Finished $subj"
    fi
done

echo "✅ All subjects processed. Results and logs saved."
