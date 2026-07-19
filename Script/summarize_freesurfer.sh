#!/usr/bin/env bash
#!/bin/bash
#SBATCH --job-name=XCPD       # Job name
#SBATCH --output=myjob_%j.out    # Standard output (%j expands to jobId)
#SBATCH --error=myjob_%j.err     # Standard error
#SBATCH --time=120:00:00          # Time limit (hh:mm:ss)
#SBATCH --nodes=1                # Number of nodes
#SBATCH --ntasks=1               # Number of tasks
#SBATCH --cpus-per-task=8        # Number of CPU cores per task
#SBATCH --mem=65G                # Memory per node

SUBJECTS_DIR=../Dataset/blind/fmriprep/sourcedata/freesurfer
#SUBJECTS_DIR=/mnt/DataDrive3/NishioM/Blind/derivatives/Deaf/fmriprep/sourcedata/freesurfer
export SUBJECTS_DIR

PARCELLATION_DIR=../Dataset/template/fsaverage/
export PARCELLATION_DIR

# List of subjects:
SUBJECT_LIST=$(ls -d $SUBJECTS_DIR/sub-* | xargs -n 1 basename)

# Define parcellations (without hemisphere prefix or file extension)
PARCELLATIONS=("JulichBrain" "atlas-wang_space-fsaverage" "HCP-MMP1" "Schaefer2018_400Parcels_17Networks_order")

OUTPUT_FILE="blind_parcel_stats.tsv"
echo -e "subject\themi\tparcellation\tlabel\tn_vertices\tsurf_area_mm2\tgraymatter_volume\tavg_thickness_mm\tstd_thickness_mm\tmean_curvature\tgausian_curvature\tfold_index\tcurvature_index" > $OUTPUT_FILE

for subject in $SUBJECT_LIST; do
  echo "Extracting stats for subject: $subject"

  for parc in "${PARCELLATIONS[@]}"; do
    for hemi in lh rh; do
      stats_out=$(mktemp)  # Temporary file to store output

      annot_file=$SUBJECTS_DIR/$subject/label/${hemi}.${parc}.native.annot
      
      # Skip if annotation file doesn't exist
      if [[ ! -f $annot_file ]]; then
        #echo "  Warning: Missing $annot_file, skipping."
        #continue
        # Source FSaverage annotation (template)
        template_annot=${PARCELLATION_DIR}/${hemi}.${parc}.annot

        if [[ ! -f $template_annot ]]; then
            echo "  ERROR: Missing template parcellation: $template_annot"
            echo "  Cannot generate $annot_file. Skipping."
            continue
        fi

        # Use FreeSurfer to map fsaverage parcellation → subject native space
        mri_surf2surf \
            --srcsubject fsaverage \
            --trgsubject $subject \
            --hemi $hemi \
            --sval-annot $template_annot \
            --tval $annot_file

        if [[ ! -f $annot_file ]]; then
            echo "  ERROR: Failed to generate $annot_file — skipping."
            continue
        fi

        echo "  Successfully created $annot_file."
      fi

      # Run stats command
      mris_anatomical_stats -a $annot_file -f $stats_out -b $subject $hemi
      # Extract data and append to main output
      grep -v '^#' "$stats_out" | while read -r line; do
        # Get the last 10 columns as numbers
        nverts=$(echo "$line" | awk '{print $(NF-8)}')
        area=$(echo "$line" | awk '{print $(NF-7)}')
        grayvol=$(echo "$line" | awk '{print $(NF-6)}')
        thickavg=$(echo "$line" | awk '{print $(NF-5)}')
        thickstd=$(echo "$line" | awk '{print $(NF-4)}')
        meancurv=$(echo "$line" | awk '{print $(NF-3)}')
        gauscurv=$(echo "$line" | awk '{print $(NF-2)}')
        foldind=$(echo "$line" | awk '{print $(NF-1)}')
        curvind=$(echo "$line" | awk '{print $(NF)}')
        # The label is everything before these 10 numeric columns
        label=$(echo "$line" | awk '{for(i=1;i<=NF-9;i++) printf $i " "; print ""}' | sed 's/ *$//')
        echo -e "${subject}\t${hemi}\t${parc}\t${label}\t${nverts}\t${area}\t${grayvol}\t${thickavg}\t${thickstd}\t${meancurv}\t${gauscurv}\t${foldind}\t${curvind}" >> $OUTPUT_FILE
      done

      rm -f "$stats_out"
    done
  done
done
