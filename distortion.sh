#!/bin/bash
protocol=$1 #ABCD or CMRR
mri=$2 #dmri fmri
s=$3 #subjnect
image=$6
bvecs=$7
bvals=$8
name=$9


if [[ $4 == *pa* ]] || [[ $4 == *PA* ]]; then
	echo $4"---PA"
	pa_file=$4
	ap_file=$5
else
	echo $4"---AP"
	ap_file=$4
	pa_file=$5
fi



folder=/space/erebus/1/users/data
out_folder=${folder}/preprocess/${s}/${protocol}
#mkdir ${out_folder}

#outputs
ap_motion=${name}_AP_motion.nii.gz
pa_motion=${name}_PA_motion.nii.gz
image_motion=${name}_motion.nii.gz
pa_ap_file=${name}_PA_AP.nii.gz
image_corrected=${name}_topup.nii.gz
image_eddy=${name}_topup_eddy.nii.gz
pa_ap_corrected=${name}_AP_PA_topup.nii.gz
pa_ap_brain=${name}_AP_PA_brain.nii.gz


if [ "${protocol}" = "ABCD"  ] || [ "${protocol}" = "iPAT2" ] ; then
	
	if  [ "${mri}" = "fMRI"  ]; then
		mcflirt -in ${out_folder}//${image} -refvol ${out_folder}/${pa_file} -out ${out_folder}//${image_motion} -spline_final
	fi
	

	fslmerge -t ${out_folder}/${pa_ap_file} ${out_folder}/${pa_file} ${out_folder}/${ap_file}

	topup --imain=${out_folder}/${pa_ap_file} --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt  --subsamp=1 --out=${out_folder}/${name}_topup_results --iout=${out_folder}/${name}_b0_unwarped --config=b02b0.cnf --fout=${out_folder}/${name}_fieldmap_Hz

	applytopup --imain=${out_folder}//${image_motion} --inindex=1 --method=jac  --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --topup=${out_folder}/${name}_topup_results --out=${out_folder}/${image_corrected}

	if [ "${mri}" = "dMRI"  ]; then
		applytopup --imain=${out_folder}//${pa_file},${out_folder}//${ap_file} --topup=${out_folder}/${name}_topup_results --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=1,3 --out=${out_folder}/${pa_ap_corrected}
		
		rm ${out_folder}//index.txt
		indx=""
	
		for ((i=0; i<100; ++i)); do indx="$indx 1"; done
	
		bet ${out_folder}/${pa_ap_corrected} ${out_folder}/${pa_ap_brain} -m -f 0.15
	
		echo $indx > ${out_folder}//index.txt

		eddy --imain=${out_folder}//${image_motion} --mask=${out_folder}/${pa_ap_brain} --acqp=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --index=${out_folder}/index.txt --bvecs=${out_folder}//${bvecs} --bvals=${out_folder}/${bvals} --topup=${out_folder}/${name}_topup_results --out=${out_folder}//${image_eddy}

	else
		applytopup --imain=${out_folder}//${pa_file},${out_folder}//${ap_file} --topup=${out_folder}/${name}_topup_results --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=1,2 --out=${out_folder}/${pa_ap_corrected}

	fi 

else




	if  [ "${mri}" = "fMRI"  ]; then
		mcflirt -in ${out_folder}/${pa_file}  -out ${out_folder}/${pa_motion} -spline_final
		mcflirt -in ${out_folder}/${ap_file}  -out ${out_folder}/${ap_motion} -spline_final
	fi
	
	fslroi ${out_folder}/${pa_motion} ${out_folder}/${name}_PA_b0.nii.gz 0 2
	fslroi ${out_folder}/${ap_motion} ${out_folder}/${name}_AP_b0.nii.gz 0 2

	fslmerge -t ${out_folder}/${name}_b0.nii.gz ${out_folder}/${name}_PA_b0.nii.gz ${out_folder}/${name}_AP_b0.nii.gz

	topup --imain=${out_folder}/${name}_b0.nii.gz --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt  --subsamp=1 --out=${out_folder}/${name}_topup_results --iout=${out_folder}/${name}_b0_unwarped --config=b02b0.cnf --fout=${out_folder}/${name}_fieldmap_Hz

	applytopup --imain=${out_folder}/${name}_PA_b0.nii.gz,${out_folder}/${name}_AP_b0.nii.gz  --topup=${out_folder}/${name}_topup_results --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=1,3 --out=${out_folder}/${pa_ap_corrected}
	remove=.nii.gz
	applytopup --imain=${out_folder}/${pa_motion}  --topup=${out_folder}/${name}_topup_results --method=jac --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=1 --out=${out_folder}/${pa_file%${remove}}_topup.nii.gz # ${name}_topup_PA.nii.gz
	applytopup --imain=${out_folder}/${ap_motion} --topup=${out_folder}/${name}_topup_results --method=jac --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=3 --out=${out_folder}/${ap_file%${remove}}_topup.nii.gz #$${name}_topup_AP.nii.gz
#	applytopup --imain=${out_folder}/${pa_file},${out_folder}/${ap_file} --topup=${out_folder}/${mri}_topup_results --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=1,3 --method=jac --out=${out_folder}/${mri}_topup_AP.nii.gz
	
#	fslmerge -t ${out_folder}/${name}_topup.nii.gz ${out_folder}/${name}_topup_PA.nii.gz ${out_folder}/${name}_topup_AP.nii.gz   
	if  [ "${mri}" = "dMRI"  ]; then
		rm ${out_folder}//index.txt
		indx=""

		for ((i=0; i<100; ++i)); do indx="$indx 1"; done
		for ((i=0; i<100; ++i)); do indx="$indx 3"; done

		echo $indx > ${out_folder}//index.txt
	
		bet ${out_folder}/${pa_ap_corrected} ${out_folder}/${pa_ap_brain} -m -f 0.15

		fslmerge -t  ${out_folder}/${name}_AP_PA.nii.gz ${out_folder}/${pa_motion} ${out_folder}/${ap_file}
		rm ${out_folder}/double.b*
		cat ${out_folder}/${bvecs} ${out_folder}/${bvecs}  >> ${out_folder}/double.bvecs
		cat ${out_folder}/${bvals} ${out_folder}/${bvals}  >> ${out_folder}/double.bvals
		
		pbsubmit -n 1  -m vsiless -c "eddy --imain=${out_folder}/${name}_AP_PA.nii.gz --mask=${out_folder}/${pa_ap_brain} --acqp=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --index=${out_folder}/index.txt --bvecs=${out_folder}/double.bvecs --bvals=${out_folder}/double.bvals --topup=${out_folder}/${name}_topup_results --out=${out_folder}//${image_eddy}"

		rm ${out_folder}//index_PA.txt
		indx=""

		for ((i=0; i<100; ++i)); do indx="$indx 1"; done
		echo $indx > ${out_folder}//index_PA.txt

		pbsubmit -n 1  -m vsiless -c "eddy --imain=${out_folder}/${pa_motion} --mask=${out_folder}/${pa_ap_brain} --acqp=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --index=${out_folder}/index_PA.txt --bvecs=${out_folder}/${bvecs} --bvals=${out_folder}/${bvals} --topup=${out_folder}/${name}_topup_results --out=${out_folder}/${name}_topup_eddy_PA.nii.gz"
		

	fi


fi

