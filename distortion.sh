#!/bin/bash
#Viviana Siless vsiless@mgh.harvard.edu

if [[ ! ${SUBJECTS_DIR} ]]; then
        SUBJECTS_DIR=/space/erebus/1/users/data/preprocess
fi
	

function distortion_CMRR()
{
	protocol=$1
	mri=$2
	s=$3 #subject
	image=$4
	remove=.nii.gz
	name=${image%${remove}}	
	image_motion=${name}_motion.nii.gz
	pa_ap_file=${name}_PA_AP.nii.gz
	image_corrected=${name}_topup.nii.gz
	folder=/space/erebus/1/users/data
	out_folder=${PREPROCESS_DIR}/${s}/ 
	#${protocol}

	if  [ "${mri}" = "dMRI"  ]; then
		bvecs=$8
		bvals=$9
		numRef=${10}
	else
		numRef=$8
	fi
	if [[ $5 == *pa* ]] || [[ $5 == *PA* ]]; then
		echo $5"---PA"
		pa_file=$5
		ap_file=$6
	else
		echo $5"---AP"
		ap_file=$5
		pa_file=$6
	fi

	n=`mri_info --nframes ${out_folder}/${pa_file}`
	echo "${n}"
	echo ${out_folder}
	echo "mri_info --nframes ${out_folder}/${pa_file}"
	echo $n
	if  [ $n -ge 4  ]; then
	
		echo "more than 4 volumes, use the b0 ${numRef}"
		fslroi ${out_folder}/${pa_file} ${out_folder}/${pa_file%${remove}}_b0.nii.gz 0 ${numRef}
		fslroi ${out_folder}/${ap_file} ${out_folder}/${ap_file%${remove}}_b0.nii.gz 0 ${numRef}
		pa_file=${pa_file%${remove}}_b0.nii.gz
		ap_file=${ap_file%${remove}}_b0.nii.gz

	fi


	if  [ "$7" = "PA"  ]; then
		echo "to correct for PA"
		ind=1
		refvol=${pa_file}
	else
		echo "to correct for AP"
		ind=$(( $numRef + 1))
		refvol=${ap_file}
	fi
	
	

	#append both AP and PA file into one PA_AP file
	rm ${out_folder}/${pa_ap_file}
	fslmerge -t ${out_folder}/${pa_ap_file} ${out_folder}/${pa_file} ${out_folder}/${ap_file}
#	 --subsamp=1 
	topup --imain=${out_folder}/${pa_ap_file} --datain=${PREPROCESS_DIR}/datains/datain_${mri}_${protocol}.txt --out=${out_folder}/${name}_topup_results --iout=${out_folder}/${name}_itopup_results --config=b02b0.cnf --fout=${out_folder}/${name}_ftopup_results


	#register image to the corresponding distortion map
	if  [ "${mri}" = "fMRI"  ]; then
		mcflirt -in ${out_folder}/${image} -reffile ${out_folder}/${refvol} -out ${out_folder}/${image_motion} -spline_final -plots 
	
		applytopup --imain=${out_folder}/${image_motion}  --topup=${out_folder}/${name}_topup_results --method=jac --datain=${PREPROCESS_DIR}/datains/datain_${mri}_${protocol}.txt --inindex=${ind} --out=${out_folder}/${image%${remove}}_topup.nii.gz


	else		
		
		image_eddy=${name}_topup_eddymp.nii.gz
		brain=${out_folder}/${name}_brain.nii.gz

		#bet ${out_folder}/${pa_ap_corrected} ${out_folder}/${pa_ap_brain} -m -f 0.15

		#list of 1 or 4 depends if correcting for AP or PA
		rm ${out_folder}//index.txt
		indx=""

	
		for ((i=0; i< ${n} ; ++i)); do indx="$indx 1"; done
		for ((i=0; i< ${n} ; ++i)); do indx="$indx ${ind}"; done

		echo $indx > ${out_folder}//index.txt
		
		fslroi ${out_folder}/${name}_itopup_results.nii.gz ${brain} 0 1
		bet ${brain} ${brain} -m -f 0.15

		string="/usr/pubsw/packages/fsl/6.0.0/bin/eddy_openmp --imain=${out_folder}/${image} --mask=${brain} --acqp=${PREPROCESS_DIR}/datains/datain_${mri}_${protocol}.txt --index=${out_folder}/index.txt --bvecs=${out_folder}/${bvecs} --bvals=${out_folder}/${bvals} --topup=${out_folder}/${name}_topup_results --out=${out_folder}//${image_eddy} --cnr_maps "

		echo ${string}
		${string}

	fi

}

$@

