protocol=$1 #ABCD or CMRR
mri=$2 #dmri fmri
s=$3 #subjnect

pa_file=$4
ap_file=$5
diffusion=$6
bvecs=$7
bvals=$8

folder=/space/erebus/1/users/data
out_folder=${folder}/preprocess/${s}/${protocol}
mkdir ${out_folder}

#outputs
pa_ap_file=${mri}_PA_AP.nii.gz
diffusion_corrected=${mri}_topup.nii.gz
diffusion_eddy=${mri}_topup_eddy.nii.gz
pa_ap_corrected=${mri}_AP_PA_topup.nii.gz
pa_ap_brain=${mri}_AP_PA_brain.nii.gz

<<COMMENT
s=PANDA005
pa_file=datain.txt
ap_file=ABCD_dMRI_DistortionMap_AP.nii.gz
diffusion=ABCD_dMRI_pedi.nii.gz

#outputs
pa_ap_file=ABCD_dMRI_DistortionMap.nii.gz
diffusion_corrected=ABCD_dMRI_pedi_topup.nii.gz
pa_ap_corrected=ABCD_dMRI_DistortionMap_topup.nii.gz
pa_ap_brain=ABCD_dMRI_DistortionMap_brain.nii.gz
COMMENT



fslmerge -t ${folder}/preprocess/${s}/${pa_ap_file} ${folder}/preprocess/${s}/${pa_file} ${folder}/preprocess/${s}/${ap_file}

topup --imain=${folder}/preprocess/$s/${pa_ap_file} --datain=${folder}/preprocess/datain.txt  --subsamp=1 --out=${out_folder}/${mri}_topup_results --iout=${out_folder}/b0_unwarped --config=b02b0.cnf --fout=${out_folder}/fieldmap_Hz


applytopup --imain=${folder}/preprocess/$s/${diffusion} --inindex=3  --method=jac  --datain=${folder}/preprocess/datain.txt --topup=${out_folder}/${mri}_topup_results --out=${out_folder}/${diffusion_corrected}

applytopup --imain=${folder}/preprocess/$s/${pa_file},${folder}/preprocess/$s/${ap_file} --topup=${out_folder}/${mri}_topup_results --datain=${folder}/preprocess/datain.txt --inindex=1,3 --out=${out_folder}/${pa_ap_corrected}

bet ${out_folder}/${pa_ap_corrected} ${out_folder}/${pa_ap_brain} -m -f 0.2

indx=""
for ((i=0; i<103; ++i)); do indx="$indx 3"; done
#for ((i=0; i<65; ++i)); do indx="$indx 2"; done
echo $indx > ${out_folder}//index.txt

if [ "${bvecs}" <> "" ] ; then
	eddy --imain=${out_folder}/${pa_ap_corrected} --mask=${out_folder}/${pa_ap_brain}  --acqp=${folder}/preprocess/datain.txt --index=${out_folder}/index.txt --bvecs=${folder}/preprocess/$s/${bvecs} --bvals=${folder}/preprocess/$s/${bvecs} --topup=${out_folder}/${mri}_topup_results --out=${out_folder}//${diffusion_eddy}

fi


