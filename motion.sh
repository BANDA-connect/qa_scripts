#!/bin/bash


function ltaDiff()
{
	s=$1 #BANDA001 
	setenv SUBJECTS_DIR /autofs/space/erebus_001/users/data/preprocess/FS/MGH_HCP
	cd /space/erebus/1/users/data/preprocess/${s}/motion
	
	files=(T1.nii.gz dMRI_AP1.nii.gz dMRI_PA1.nii.gz fMRI_rest1_AP.nii.gz fMRI_rest2_PA.nii.gz dMRI_AP2.nii.gz dMRI_PA2.nii.gz fMRI_rest3_AP.nii.gz fMRI_rest4_PA.nii.gz  tfMRI_gambling1_AP.nii.gz tfMRI_gambling2_PA.nii.gz tfMRI_faceMatching1_AP.nii.gz tfMRI_faceMatching2_PA.nii.gz tfMRI_conflict1_AP.nii.gz tfMRI_conflict2_PA.nii.gz tfMRI_conflict3_AP.nii.gz tfMRI_conflict4_PA.nii.gz T2.nii.gz)

	size=${#files[@]}

	lta_diff ${files[1]%%.*}2T1.lta identity.nofile 7 > ${files[1]%%.*}_2_T1.lta_diff

	for ((i=2;i<size;i++)); 
	do
		t1=${files[i]%%.*}2T1.lta
		t2=${files[$(($i-1))]%%.*}2T1.lta 
		tf=${files[i]%%.*}_2_${files[$(($i-1))]%%.*}.lta
		mri_concatenate_lta -invert2 $t1 $t2 $tf
		lta_diff $tf identity.nofile 7 > ${tf%%.*}.lta_diff
	done

}

function everything2T1Motion()
{
	s=$1 #BANDA001 
	setenv SUBJECTS_DIR /autofs/space/erebus_001/users/data/preprocess/FS/MGH_HCP
	cd /space/erebus/1/users/data/preprocess/${s}

	mkdir motion
	IFS=","
	while read scan skip niftyName protocol
        do
		echo $niftyName
		echo $skip
		echo $scan
		echo $protocol
		if [[ ${niftyName} != *SpinEcho* ]];
		then
			#string="bbregister --s $s --mov  /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz --reg  /space/erebus/1/users/data/preprocess/${s}/motion/${niftyName}2T1.lta --bold"
			#pbsubmit -n 1  -c ${string}
			if [[ ${niftyName} == *T1* ]];
			then	
				string="bbregister --s $s --mov  /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz --reg  /space/erebus/1/users/data/preprocess/${s}/motion/${niftyName}2T1.lta --t1"
			elif [[ ${niftyName} == *T2* ]];
			then	
				string="bbregister --s $s --mov  /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz --reg  /space/erebus/1/users/data/preprocess/${s}/motion/${niftyName}2T1.lta --t2"
			elif [[ ${niftyName} == *dMRI* ]];
			then
				string="bbregister --s $s --mov  /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz --reg  /space/erebus/1/users/data/preprocess/${s}/motion/${niftyName}2T1.lta --dti"
			else
				string="bbregister --s $s --mov  /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz --reg  /space/erebus/1/users/data/preprocess/${s}/motion/${niftyName}2T1.lta --bold"
			fi
			pbsubmit -n 1  -c ${string}

		fi


	done < dicom2nifty.csv
	
}

function everything2T1SNR()
{
	s=$1 #BANDA001 
	setenv SUBJECTS_DIR /autofs/space/erebus_001/users/data/preprocess/FS/MGH_HCP
	cd /space/erebus/1/users/data/preprocess/${s}

	mkdir snr
	IFS=","
	while read scan skip niftyName protocol
        do
		if [[ ${niftyName} != *SpinEcho* ]] ;
		then
			echo $niftyName
			echo $scan
					
			file=${niftyName}.nii.gz
			if [[ ${niftyName} == *T1* ]];
			then			
				file=/space/erebus/1/users/data/preprocess/${s}/${niftyName}_brain.nii.gz
				bet /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz ${file}
				type=t1	
			elif [[ ${niftyName} == *T2* ]];
			then	
				file=/space/erebus/1/users/data/preprocess/${s}/${niftyName}_brain.nii.gz
				bet /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz ${file}
				type=t2
			elif [[ ${niftyName} == *dMRI* ]];
			then
				type=dti
			else
				type=bold
			fi
			bbregister --s $s --mov ${file}  --reg  /space/erebus/1/users/data/preprocess/${s}/snr/${niftyName}2T1.lta --${type}
		fi

	done < dicom2nifty.csv
	
}
function GetB0s()
{
	
	s=$1 
	echo $s
	cd /space/erebus/1/users/data/preprocess/${s}
	mkdir snr
	frame=[0 1 17 33 49 65 81]

	mri_convert --frame 0 1 17 33 49 65 81  dMRI_AP1.nii.gz  dMRI_AP1_lowb.nii.gz
	mri_convert --frame 0 1 17 33 49 65 81  dMRI_PA1.nii.gz  dMRI_PA1_lowb.nii.gz
	mri_convert --frame 0 1 17 33 49 65 81  dMRI_AP2.nii.gz  dMRI_AP2_lowb.nii.gz
	mri_convert --frame 0 1 17 33 49 65 81  dMRI_PA2.nii.gz  dMRI_PA2_lowb.nii.gz 

:<<COMMENT
	fslroi dMRI_topup_eddy.nii.gz snr/dMRI1_b0.nii.gz 0 2
	fslroi dMRI_topup_eddy.nii.gz snr/dMRI2_b0.nii.gz 99 2
	fslroi dMRI_topup_eddy.nii.gz snr/dMRI3_b0.nii.gz 199 2
	fslroi dMRI_topup_eddy.nii.gz snr/dMRI4_b0.nii.gz 298 2
COMMENT

}
function T1aparc2all()
{
	s=$1 
	setenv SUBJECTS_DIR /autofs/space/erebus_001/users/data/preprocess/FS/MGH_HCP
	cd /space/erebus/1/users/data/preprocess/${s}

	IFS=","
	while read scan skip niftyName protocol
        do
		echo $niftyName
		echo $skip
		echo $scan
		echo $protocol
		if [[ ${niftyName} != *SpinEcho* ]] ;
		then
	

			file=${niftyName}.nii.gz
			if [[ ${niftyName} == *T1* ]];
			then			
				file=/space/erebus/1/users/data/preprocess/${s}/${niftyName}_brain.nii.gz
				bet /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz ${file}
				type=t1	
			elif [[ ${niftyName} == *T2* ]];
			then	
				file=/space/erebus/1/users/data/preprocess/${s}/${niftyName}_brain.nii.gz
				bet /space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz ${file}
				type=t2
			elif [[ ${niftyName} == *dMRI* ]];
			then
				type=dti
			else
				type=bold
			fi
			bbregister --s $s --mov ${file}  --reg  /space/erebus/1/users/data/preprocess/${s}/snr/${niftyName}2T1.lta --${type}


			reg="/space/erebus/1/users/data/preprocess/${s}/snr/${niftyName}2T1.lta" 
			if [[ ${niftyName} == *T2* ]];
			then	
				file="/space/erebus/1/users/data/preprocess/${s}/${niftyName}_brain.nii.gz"
			elif [[ ${niftyName} == *T1* ]];
			then
				file="/space/erebus/1/users/data/preprocess/${s}/${niftyName}_brain.nii.gz"
			#elif [[ ${niftyName} == *dMRI* ]];
			#then
			#	file="/space/erebus/1/users/data/preprocess/${s}/dMRI_topup_eddy.nii.gz"
			#	reg="/space/erebus/1/users/data/preprocess/${s}/snr/${niftyName}2T1.lta"

				#mri_vol2vol --mov /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/wmparc.mgz --targ $file --o /space/erebus/1/users/data/preprocess/${s}/snr/wmparc_2dMRI.nii.gz --lta $reg --nearest		
				#mri_binarize --i /space/erebus/1/users/data/preprocess/${s}/snr/wmparc_2dMRI.nii.gz --o /space/erebus/1/users/data/preprocess/${s}/snr/WMROI4010_2dMRI.nii.gz  --match 4010
				#mri_binarize --i /space/erebus/1/users/data/preprocess/${s}/snr/wmparc_2dMRI.nii.gz --o /space/erebus/1/users/data/preprocess/${s}/snr/WMROI5001_2dMRI.nii.gz  --match 5001
			#elif [[ ${niftyName} == *T1* ]];
			#then
			#	file="/space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz"
			#	reg="/space/erebus/1/users/data/preprocess/${s}/snr/${niftyName}2T1.lta"
			else	
				file="/space/erebus/1/users/data/preprocess/${s}/${niftyName}.nii.gz"
				reg="/space/erebus/1/users/data/preprocess/${s}/snr/${niftyName}2T1.lta"

			fi

			mri_vol2vol --mov /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/wmparc.mgz --targ $file --o /space/erebus/1/users/data/preprocess/${s}/snr/wmparc_2${niftyName}.nii.gz --lta-inv $reg --nearest
			mri_binarize --i /space/erebus/1/users/data/preprocess/${s}/snr/wmparc_2${niftyName}.nii.gz --o /space/erebus/1/users/data/preprocess/${s}/snr/WMROI4010_2${niftyName}.nii.gz  --match 4010 
			mri_binarize --i /space/erebus/1/users/data/preprocess/${s}/snr/wmparc_2${niftyName}.nii.gz --o /space/erebus/1/users/data/preprocess/${s}/snr/WMROI5001_2${niftyName}.nii.gz  --match 5001 5002

					
		fi


	done < dicom2nifty.csv
}
function pre_compute()
{
	s=$1
	setenv SUBJECTS_DIR /autofs/space/erebus_001/users/data/preprocess/FS/MGH_HCP
	cd /space/erebus/1/users/data/preprocess/${s}

	#mkdir motion
	mkdir snr	
	IFS=","
	while read scan skip niftyName protocol
        do
		echo $niftyName
		echo $skip
		echo $scan
		echo $protocol
		if [[ ${niftyName} != *SpinEcho* ]];
		then
			if [[ ${niftyName} == *fMRI* ]];
			then
				mri_concat --i /space/erebus/1/users/data/preprocess/$s/${niftyName}.nii.gz --mean --o /space/erebus/1/users/data/preprocess/$s/snr/mean${niftyName}.nii.gz
				mri_concat --i /space/erebus/1/users/data/preprocess/$s/${niftyName}.nii.gz --std --o /space/erebus/1/users/data/preprocess/$s/snr/std${niftyName}.nii.gz
				fscalc /space/erebus/1/users/data/preprocess/$s/snr/mean${niftyName}.nii.gz div /space/erebus/1/users/data/preprocess/$s/snr/std${niftyName}.nii.gz --o /space/erebus/1/users/data/preprocess/$s/snr/snr${niftyName}.nii.gz
			fi	
			if [[ ${niftyName} == *dMRI* ]];
			then
				#echo " grep -n ^5\. $/space/erebus/1/users/data/preprocess/$s/${niftyName}.bvals\ | awk -v FS=:'{print $1-1}'"		
				#lowblist = `grep -n ^5\. /space/erebus/1/users/data/preprocess/$s/${niftyName}.bvals\ | awk '{print $1-1}'` 
				#mri_convert --frame lowblist /space/erebus/1/users/data/preprocess/$s/${niftyName}.nii.gz /space/erebus/1/users/data/preprocess/$s/${niftyName}_lowb.nii.gz
				mri_concat --i /space/erebus/1/users/data/preprocess/$s/${niftyName}_lowb.nii.gz --mean --o /space/erebus/1/users/data/preprocess/$s/snr/mean${niftyName}.nii.gz
				mri_concat --i /space/erebus/1/users/data/preprocess/$s/${niftyName}_lowb.nii.gz --std --o /space/erebus/1/users/data/preprocess/$s/snr/std${niftyName}.nii.gz

				fscalc /space/erebus/1/users/data/preprocess/$s/snr/mean${niftyName}.nii.gz div /space/erebus/1/users/data/preprocess/$s/snr/std${niftyName}.nii.gz --o /space/erebus/1/users/data/preprocess/$s/snr/snr${niftyName}.nii.gz
			fi	


		fi

	done < dicom2nifty.csv
}
function motion_measures()
{
	s=$1 #BANDA001 

	cd /space/erebus/1/users/data/preprocess/${s}

	mkdir motion
	rm motion/*.nii.gz

	fslroi fMRI_rest1_AP.nii.gz motion/fmri_a.nii.gz 0 1 
	fslroi fMRI_rest2_PA.nii.gz motion/fmri_b.nii.gz 0 1 
	fslroi fMRI_rest3_AP.nii.gz motion/fmri_c.nii.gz 0 1 
	fslroi fMRI_rest4_PA.nii.gz motion/fmri_d.nii.gz 0 1 

	fslroi tfMRI_gambling1_AP.nii.gz motion/fmri_e.nii.gz 0 1 
	fslroi tfMRI_gambling2_PA.nii.gz motion/fmri_f.nii.gz 0 1 

	fslroi tfMRI_faceMatching1_AP.nii.gz motion/fmri_g.nii.gz 0 1 
	fslroi tfMRI_faceMatching2_PA.nii.gz motion/fmri_h.nii.gz 0 1 
	
	fslroi tfMRI_conflict1_AP.nii.gz motion/fmri_i.nii.gz 0 1 
	fslroi tfMRI_conflict2_PA.nii.gz motion/fmri_j.nii.gz 0 1 
	fslroi tfMRI_conflict3_AP.nii.gz motion/fmri_k.nii.gz 0 1 
	fslroi tfMRI_conflict4_PA.nii.gz motion/fmri_l.nii.gz 0 1 


	fslmerge -t motion/fmriFirsts.nii.gz  motion/fmri_*.nii.gz 
	mcflirt -in motion/fmriFirsts.nii.gz -reffile motion/fmri_a.nii -out motion/fmriFirsts_motion.nii.gz -spline_final -plots 

	
	fslmerge -t motion/structural.nii.gz T1.nii.gz  T2.nii.gz 
	mcflirt -in  motion/structural.nii.gz -out motion/structural_motion.nii.gz -spline_final -plots 

	T1=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt HCP_MGH_T1w_MPR_vNav 1`)
	#T1=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt HCP_MGH_T1w_MPR_vNav 4`)
	T2=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt HCP_MGH_T2w_SPC_vNav 1`)
	
	/autofs/space/topaz_001/users/ah221/dev_projects/dev1/mri_convert/mri_convert --nslices-override 32 --ncols-override 32   /space/erebus/1/users/data/dicoms/$s/$T1 T1_nav.nii.gz
	mcflirt -in  T1_nav.nii.gz -out motion/T1_motion.nii.gz -spline_final -plots 
	
	/autofs/space/topaz_001/users/ah221/dev_projects/dev1/mri_convert/mri_convert --nslices-override 32 --ncols-override 32   /space/erebus/1/users/data/dicoms/$s/$T2 T2_nav.nii.gz		
	mcflirt -in  T2_nav.nii.gz -out motion/T2_motion.nii.gz -spline_final -plots
}
$@


