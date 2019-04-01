#!/bin/bash


folder=/space/erebus/1/users/data

function distortion_ABCD_iPAT2()
{
	protocol=$1 #ABCD or ipat
	mri=$2 #dmri fmri
	s=$3 #subjnect
	image=$6
	
	if [[ $4 == *pa* ]] || [[ $4 == *PA* ]]; then
		echo $4"---PA"
		pa_file=$4
		ap_file=$5
	else
		echo $4"---AP"
		ap_file=$4
		pa_file=$5
	fi


	out_folder=${folder}/preprocess/${s}/${protocol}

	remove=.nii.gz
	name=${image%${remove}}	
	image_motion=${name}_motion.nii.gz
	pa_ap_file=${name}_PA_AP.nii.gz
	image_corrected=${name}_topup.nii.gz
	
	if  [ "${mri}" = "fMRI"  ]; then
		mcflirt -in ${out_folder}//${image} -reffile ${out_folder}/${pa_file} -out ${out_folder}//${image_motion} -spline_final
		#mcflirt -in ${out_folder}//${image}  -out ${out_folder}//${image_motion} -spline_final
		#flirt -in ${out_folder}//${image_motion} -ref ${out_folder}/${pa_file} -out ${out_folder}//${image_motion} -2D -interp spline
	fi
	
	fslmerge -t ${out_folder}/${pa_ap_file} ${out_folder}/${pa_file} ${out_folder}/${ap_file}
	# --subsamp=1
	topup --imain=${out_folder}/${pa_ap_file} --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt  --out=${out_folder}/${name}_topup_results --iout=${out_folder}/${name}_itopup_results --config=b02b0.cnf --fout=${out_folder}/${name}_ftopup_results

	applytopup --imain=${out_folder}//${image_motion} --inindex=1 --method=jac  --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --topup=${out_folder}/${name}_topup_results --out=${out_folder}/${image_corrected}

	if [ "${mri}" = "dMRI"  ]; then
		bvecs=$7
	bvals=$8
	
		image_eddy=${name}_topup_eddy.nii.gz
		pa_ap_corrected=${name}_AP_PA_topup.nii.gz
		pa_ap_brain=${name}_AP_PA_brain.nii.gz
	
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

}
function distortion_CMRR()
{


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

}

function distortion_CMRR_2()
{
#/pbs/vsiless/pbsjob_1456
	echo "Starting distortion_CMRR_2"

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
	out_folder=${folder}/preprocess/${s}/ 
	#${protocol}

	if  [ "${mri}" = "dMRI"  ]; then
		bvecs=$8
		bvals=$9
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
	echo "hola"
	echo ${out_folder}
	echo "mri_info --nframes ${out_folder}/${pa_file}"
	echo $n
	if  [ $n -ge 4  ]; then
	
		echo "more than 4 volumes, use the b0"
		fslroi ${out_folder}/${pa_file} ${out_folder}/${pa_file%${remove}}_b0.nii.gz 0 3
		fslroi ${out_folder}/${ap_file} ${out_folder}/${ap_file%${remove}}_b0.nii.gz 0 3
		pa_file=${pa_file%${remove}}_b0.nii.gz
		ap_file=${ap_file%${remove}}_b0.nii.gz

	fi


	if  [ "$7" = "PA"  ]; then
		echo "to correct for PA"
		ind=1
		refvol=${pa_file}
	else
		echo "to correct for AP"
		ind=4
		refvol=${ap_file}
	fi
		
	
	

	#append both AP and PA file into one PA_AP file
	rm ${out_folder}/${pa_ap_file}
	fslmerge -t ${out_folder}/${pa_ap_file} ${out_folder}/${pa_file} ${out_folder}/${ap_file}
#	 --subsamp=1 
	topup --imain=${out_folder}/${pa_ap_file} --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --out=${out_folder}/${name}_topup_results --iout=${out_folder}/${name}_itopup_results --config=b02b0.cnf --fout=${out_folder}/${name}_ftopup_results


	#register image to the corresponding distortion map
	if  [ "${mri}" = "fMRI"  ]; then
		mcflirt -in ${out_folder}/${image} -reffile ${out_folder}/${refvol} -out ${out_folder}/${image_motion} -spline_final -plots 
	
		applytopup --imain=${out_folder}/${image_motion}  --topup=${out_folder}/${name}_topup_results --method=jac --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=${ind} --out=${out_folder}/${image%${remove}}_topup.nii.gz


	else		
		
		image_eddy=${name}_topup_eddy.nii.gz
		#image_eddy=${out_folder}/${name}_topup_eddy.nii.gz
		brain=${out_folder}/${name}_brain.nii.gz

		bet ${out_folder}/${pa_ap_corrected} ${out_folder}/${pa_ap_brain} -m -f 0.15

		#fslmerge -t  ${out_folder}/${name}_AP_PA.nii.gz ${out_folder}/${pa_file} ${out_folder}/${ap_file}
		rm ${out_folder}/double.b*
		cat ${out_folder}/${bvecs} ${out_folder}/${bvecs}  >> ${out_folder}/double.bvecs
		cat ${out_folder}/${bvals} ${out_folder}/${bvals}  >> ${out_folder}/double.bvals
		

		#list of 1 or 4 depends if correcting for AP or PA
		#num_frames=`mri_info --nframes ${out_folder}/${ap_file}`
		#echo $num_frames
		rm ${out_folder}//index.txt
		indx=""

	
		for ((i=0; i< ${n} ; ++i)); do indx="$indx 1"; done
		for ((i=0; i< ${n} ; ++i)); do indx="$indx 4"; done

		echo $indx > ${out_folder}//index.txt
		
		fslroi ${out_folder}/${name}_itopup_results.nii.gz ${brain} 0 1
		bet ${brain} ${brain} -m -f 0.15

#=		#topup?		
		#applytopup --imain=${out_folder}/${ap_motion} --topup=${out_folder}/${name}_topup_results --method=jac --datain=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --inindex=3 --out=${out_folder}/${ap_file%${remove}}_topup.nii.gz #$${name}_topup_AP.nii.gz

		#pbsubmit
		pbsubmit -n 2  -m rjj7 -c "eddy --imain=${out_folder}/${image} --mask=${brain} --acqp=${folder}/preprocess/datains/datain_${mri}_${protocol}.txt --index=${out_folder}/index.txt --bvecs=${out_folder}/${bvecs} --bvals=${out_folder}/${bvals} --topup=${out_folder}/${name}_topup_results --out=${out_folder}//${image_eddy}"

	fi

}

$@

