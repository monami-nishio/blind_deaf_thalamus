#!/usr/bin/env bash
#!/bin/bash
#SBATCH --job-name=fmriprepNishioM       # Job name
#SBATCH --output=myjob_%j.out    # Standard output (%j expands to jobId)
#SBATCH --error=myjob_%j.err     # Standard error
#SBATCH --time=120:00:00          # Time limit (hh:mm:ss)
#SBATCH --nodes=1                # Number of nodes
#SBATCH --ntasks=1               # Number of tasks
#SBATCH --cpus-per-task=8        # Number of CPU cores per task
#SBATCH --mem=65G                # Memory per node

set -euo pipefail

#########################
# CONFIGURATION
#########################

# Update these paths
BIDS_DIR=/mnt/DataDrive1/data_preproc/human_mri/2023_Trento_plosBiology_YX_raw/2023_Trento_plosBiology_YX_raw
OUT_DIR="/mnt/DataDrive3/NishioM/Blind/derivatives/2023_Trento_plosBiology_YX_raw"
FS_LICENSE="$FREESURFER_HOME/license.txt"
# Automatically detect subjects with T2w images
SUBJECTS=""
for d in "${BIDS_DIR}"/sub-sc*; do
  [ -d "$d" ] || continue
  sub_id=$(basename "$d")
  if compgen -G "${d}/anat/*.nii.gz" > /dev/null || \
     compgen -G "${d}/anat/*.nii.gz" > /dev/null; then
      preproc_file="${BIDS_DIR}/${sub_id}/anat/${sub_id}_T2w.nii.gz"
      if [ -f "$preproc_file" ]; then
        SUBJECTS+="${sub_id#sub-} "
      fi
  fi
done

if [ -z "$SUBJECTS" ]; then
  echo "No subjects with T2w images found. Exiting."
  exit 1
fi

echo "Subjects with T2w found: ${SUBJECTS}"

# Threading settings
NTHREADS=8
MEM_MB=16000

# Output folders
MRIQC_OUT="${OUT_DIR}/mriqc"
FMRIPREP_OUT="${OUT_DIR}/fmriprep"
WORK_DIR="/tmp/fmriprep_work"

LOG_DIR="${OUT_DIR}/logs"
mkdir -p "${LOG_DIR}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

#########################
# MRIQC
#########################

#echo "Running MRIQC..."
#docker run --rm -it \
#  -v "${BIDS_DIR}":/data:ro \
#  -v "${MRIQC_OUT}":/out \
#  -v "${WORK_DIR}/mriqc":/work \
#  nipreps/mriqc:latest /data /out participant \
#  --participant-label ${SUBJECTS} \
#  --verbose-reports \
#  2>&1 | tee "${LOG_DIR}/mriqc_${TIMESTAMP}.log"

#########################
# fMRIPrep
#########################
#--cifti-output 91k \

echo "Running fMRIPrep..."
docker run --rm \
  -v "${BIDS_DIR}":/data:ro \
  -v "${FMRIPREP_OUT}":/out \
  -v "${WORK_DIR}/fmriprep":/work \
  -v "${FS_LICENSE}":/opt/freesurfer/license.txt \
  nipreps/fmriprep:latest \
  /data /out participant \
  --participant-label ${SUBJECTS} \
  --fs-license-file /opt/freesurfer/license.txt \
  --output-spaces MNI152NLin2009cAsym T1w \
  --nthreads ${NTHREADS} \
  --omp-nthreads ${NTHREADS} \
  --mem_mb ${MEM_MB} \
  --task-id judgement \
  --skip_bids_validation \
  2>&1 | tee "${LOG_DIR}/fmriprep_${TIMESTAMP}.log"

echo "Pipeline complete ✅"
