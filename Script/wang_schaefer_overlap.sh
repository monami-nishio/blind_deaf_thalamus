input_nii="../Dataset/template/Wang/MNI152NLin2009cAsym/atlas-WangDilatedSA160_space-MNI152NLin2009cAsym_res-01_resampled.nii.gz"  # Replace with your actual file name
atlas_nii="../Dataset/template/atlas_Schaefer2018_400Parcels_17Networks_order_FSLMNI152_2mm.nii.gz"

for X in {1..50}; do
    output_nii="output_value_${X}.nii.gz"
    binarized_nii="binarized_${X}.nii.gz"
    masked_nii="../Dataset/template/Wang/schaefer_mask/schaefer_${X}"
    fslmaths $input_nii -thr $X -uthr $X $output_nii
    fslmaths $output_nii -bin $binarized_nii
    fslmaths $atlas_nii -mas $binarized_nii $masked_nii.nii.gz
    max_intensity=$(fslstats $masked_nii -R | awk '{print $2}')
    fslstats $masked_nii -k $masked_nii -H 10000 $max_intensity > histogram.txt
    awk '{if ($2 > 0) print $1}' histogram.txt > unique_labels.txt
    echo $max_intensity
done