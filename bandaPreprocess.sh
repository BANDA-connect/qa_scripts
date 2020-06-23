#!/bin/bash
# @Viviana Siless : vsiless@mgh.harvard.edu


dsistudio=/autofs/cluster/pubsw/2/pubsw/Linux2-2.3-x86_64/packages/DSI-Studio/1.0/bin/
dsistudio=/autofs/cluster/pubsw/2/pubsw/Linux2-2.3-x86_64/packages/DSI-Studio/20170822/bin/


if [[ ! ${SUBJECTS_DIR} ]]; then
	SUBJECTS_DIR=/space/erebus/1/users/data/preprocess
fi

#scriptFolder=/space/erebus/1/users/data/code/scripts
scriptFolder=/autofs/space/erebus_002/users/vsiless/code/banda/CRHD_BANDA

scriptFolder=`dirname $0`
echo ${scriptFolder}
function forAllInFile()
{
	function=$1
	file=$2
	numberNodes=$3
	queue=$4
	extraParams=$5
	for s in `cat ${file}`;
	do

                subject=${s/^M/}                                                                                                     
		echo   ${s}
		echo ${PREPROCESS_DIR}
		echo ${extraParams}
		if [[  "${extraParams}" == "HCPD" ]]; then
			#setenv SUBJECTS_DIR /space/erebus/1/users/HCPD/preprocessed_viv/FS_STRUCTURE/
			pbsubmit -n ${numberNodes} -q ${queue} -c "bash ${0} $1 ${s}_V1_MR ${extraParams}"
		else
			#setenv SUBJECTS_DIR /space/erebus/1/users/data/preprocess/FS/MGH_HCP
			#setenv PREPROCESS_DIR /space/erebus/1/users/HCPD/preprocessed_viv/
			pbsubmit -n ${numberNodes} -q ${queue} -c "bash ${0} $1 ${s} ${extraParams}"
		fi
	done
}
function forAllSubjects()
{
	if [[  ${PREPROCESS_DIR} ]]; then
		echo ${PREPROCESS_DIR}
		cd ${PREPROCESS_DIR}
	else
		cd ${SUBJECTS_DIR}
	fi 

        function=$1 #i.e. tractography                                                                                                  
        for s in HCD1*/;                                                                                                                    
        do                                                                                                                              
                subject=${s//[\/]/}                                                                                                     
                echo ${subject}                                                                                                         
                                                                                                                                        
		pbsubmit -n ${2} -q ${3} -c "bash ${0} $1 ${subject} $4"
	done
}
#Step 1
#This function should be run after unpacksdcmdir on the BANDA subject's directory, generating a scan.txt file
#A file dicom2nifty.csv is needed mapping each scan name to the nifty output name. 
#TODO: if dicom2nifty.csv is not found on the subject's output preprocess directorty, we should use the dicom2nifty file on the preprocess level folder. Meaning that if everything is normal, we don't need to re-specify the dicom2nifty file. [if no retro-recons happened during the scan session, or error]
function dicomToNifty()
{


	echo $s 
	fout=${SUBJECTS_DIR}/$s
	mkdir -p ${fout}
	IFS=","
	while read scan skip niftyName protocol 
        do
		echo $i
		echo python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} ${niftyName}
		dicom=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} `)
		echo ${dicom}
		#mri_convert ${SUBJECTS_DIR}/$s/${dicom} ${output}/${niftyName}.nii.gz 
		#pbsubmit -n 1 -m rjj7 -c "mri_convert ${SUBJECTS_DIR}/$s/${dicom} ${fout}/${niftyName}.nii.gz "
		#pbsubmit -n 1 -c "mri_convert ${SUBJECTS_DIR}/dicoms/$s/${dicom} ${fout}/${niftyName}.nii.gz "
		mri_convert ${SUBJECTS_DIR}/dicoms/$s/${dicom} ${fout}/${niftyName}.nii.gz 
	done < $fout/dicom2nifty.csv

}
# Step 5	
# after running everything, remember to grant permission to the rest of the group
function grantPermissions()
{
	s=$1
	fout=${SUBJECTS_DIR}/$s

	chgrp -R fiber  ${SUBJECTS_DIR}/${s}
	chmod -R 770  ${SUBJECTS_DIR}/${s}

	chgrp -R fiber  ${SUBJECTS_DIR}/${s}
	chmod -R 770  ${SUBJECTS_DIR}/${s}

}


# Step 2
# For diffusion we merge all the diffusion files into one for runnning eddy which takes care of motion correction. For fMRI is not necesary since we use mcflirt to align volumes to the distortion maps /spin echos.
function mergeDiffusion()
{
	s=$1

	fout=${SUBJECTS_DIR}/$s/

:<<com	mv ${fout}/dMRI_AP1.voxel_space.bvecs ${fout}/dMRI_AP1.bvecs
	mv ${fout}/dMRI_AP2.voxel_space.bvecs ${fout}/dMRI_AP2.bvecs
	mv ${fout}/dMRI_PA1.voxel_space.bvecs ${fout}/dMRI_PA1.bvecs
	mv ${fout}/dMRI_PA2.voxel_space.bvecs ${fout}/dMRI_PA2.bvecs
com

	fslmerge -t  ${fout}/dMRI_PA.nii.gz ${fout}/dMRI_PA1.nii.gz ${fout}/dMRI_PA2.nii.gz
	fslmerge -t  ${fout}/dMRI_AP.nii.gz ${fout}/dMRI_AP1.nii.gz ${fout}/dMRI_AP2.nii.gz
:<<com
	rm ${out_folder}/double.b*
	rm ${fout}/bvecs
	rm ${fout}/bvals
	cat ${fout}/dMRI_AP1.bvals ${fout}/dMRI_AP2.bvals  >> ${fout}/bvals
	cat ${fout}/dMRI_PA1.bvals ${fout}/dMRI_PA2.bvals  >> ${fout}/bvals

	cat ${fout}/dMRI_AP1.bvecs ${fout}/dMRI_AP2.bvecs  >> ${fout}/bvecs
	cat ${fout}/dMRI_PA1.bvecs ${fout}/dMRI_PA2.bvecs  >> ${fout}/bvecs
com

	fslmerge -t  ${fout}/dMRI.nii.gz ${fout}/dMRI_PA.nii.gz ${fout}/dMRI_AP.nii.gz
}
function fixBVecsBValsFormat()
{
	s=$1
	fout=${SUBJECTS_DIR}/$s/
	subject=$1
	input=/space/erebus/1/users/HCPD/HCPDUnprocessed/
	output=/space/erebus/1/users/HCPD/preprocessed_viv/

	:<<hola cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir98_AP.bval ${output}/${subject}/dMRI_AP1N3.bvals 
	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir98_AP.bvec ${output}/${subject}/dMRI_AP1N3.bvecs

	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir99_AP.bval ${output}/${subject}/dMRI_AP2N3.bvals 

	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir99_AP.bvec ${output}/${subject}/dMRI_AP2N3.bvecs

	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir98_PA.bval ${output}/${subject}/dMRI_PA1N3.bvals 
	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir98_PA.bvec ${output}/${subject}/dMRI_PA1N3.bvecs

	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir99_PA.bval ${output}/${subject}/dMRI_PA2N3.bvals 
	cp ${input}/${subject}/unprocessed/Diffusion/${subject}_dMRI_dir99_PA.bvec ${output}/${subject}/dMRI_PA2N3.bvecs
hola

	cp ${output}/${subject}/dMRI_AP1.bvecs 	${output}/${subject}/dMRI_AP1N3.bvecs
	cp ${output}/${subject}/dMRI_AP2.bvecs 	${output}/${subject}/dMRI_AP2N3.bvecs
	cp ${output}/${subject}/dMRI_PA1.bvecs 	${output}/${subject}/dMRI_PA1N3.bvecs
	cp ${output}/${subject}/dMRI_PA2.bvecs 	${output}/${subject}/dMRI_PA2N3.bvecs

	cp ${output}/${subject}/dMRI_AP1.bvals 	${output}/${subject}/dMRI_AP1N3.bvals
	cp ${output}/${subject}/dMRI_AP2.bvals 	${output}/${subject}/dMRI_AP2N3.bvals
	cp ${output}/${subject}/dMRI_PA1.bvals 	${output}/${subject}/dMRI_PA1N3.bvals
	cp ${output}/${subject}/dMRI_PA2.bvals 	${output}/${subject}/dMRI_PA2N3.bvals

	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_AP1N3.bvecs ${fout}/dMRI_AP1.bvecs
	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_AP2N3.bvecs ${fout}/dMRI_AP2.bvecs
	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_PA1N3.bvecs ${fout}/dMRI_PA1.bvecs
	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_PA2N3.bvecs ${fout}/dMRI_PA2.bvecs

	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_AP1N3.bvals ${fout}/dMRI_AP1.bvals
	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_AP2N3.bvals ${fout}/dMRI_AP2.bvals
	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_PA1N3.bvals ${fout}/dMRI_PA1.bvals
	python3 /space/erebus/2/users/vsiless/code/freesurfer/anatomicuts/format_bvec.py ${fout}/dMRI_PA2N3.bvals ${fout}/dMRI_PA2.bvals

	rm ${out_folder}/double.b*
	rm ${fout}/bvecs
	rm ${fout}/bvals
	cat ${fout}/dMRI_AP1.bvals ${fout}/dMRI_AP2.bvals  >> ${fout}/bvals
	cat ${fout}/dMRI_PA1.bvals ${fout}/dMRI_PA2.bvals  >> ${fout}/bvals

	cat ${fout}/dMRI_AP1.bvecs ${fout}/dMRI_AP2.bvecs  >> ${fout}/bvecs
	cat ${fout}/dMRI_PA1.bvecs ${fout}/dMRI_PA2.bvecs  >> ${fout}/bvecs

}
#Step 3
# Run top up to correct for spin echo distortions AP PA.
function distortionCorrection()
{
	s=$1
	HCPD=$2
	cluster=$3 #"pubsubmit -n 1  "

	if [[ ${HCPD} ]]; then
		numRef=1
		numRefDiff=2
	else
		numRef=3
		numRefDiff=3
	fi	

#DIFFUSION
${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR dMRI $s dMRI.nii.gz dMRI_AP.nii.gz dMRI_PA.nii.gz AP bvecs bvals ${numRefDiff}
:<<ALL_FUNCTIONAL	
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz AP ${numRef}
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz PA ${numRef}

	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s fMRI_rest3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP ${numRef}
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s fMRI_rest4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA ${numRef}
	
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP ${numRef}
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA ${numRef}
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP ${numRef}
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA ${numRef}

	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP ${numRef}
	${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA ${numRef}
	
	if [[ ! ${HCPD} ]];
	then		
		${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_gambling1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP ${numRef}
		${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_gambling2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA ${numRef}
	else
		${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_gambling1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP ${numRef}
		${cluster} bash ${scriptFolder}/distortion.sh distortion_CMRR CMRR fMRI $s tfMRI_gambling2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA ${numRef}

	fi
ALL_FUNCTIONAL

}

# Step 4:
# Obtain the tractography
function tractography()
{
	s=$1
	input=${SUBJECTS_DIR}/preprocess/${s}/
	output=${SUBJECTS_DIR}/preprocess/${s}/dsi_studio
	#input=${SUBJECTS_DIR}/preprocess/${s}/${study}/
	#output=${SUBJECTS_DIR}/preprocess/${s}/${study}/dsi_studio
	mkdir 	${output}

	#source
	${dsistudio}/dsi_studio --action=src --source=${input}/dMRI_topup_eddy.nii.gz  --output=${output}/dwi.src.nii.gz

	#gqi reconstruction
	${dsistudio}/dsi_studio --action=rec --thread=8 --source=${output}/dwi.src.nii.gz --method=4 --param0=0.75 --odf_order=4 --num_fiber=3 # --deconvolution=5 #--output=${output}/fib.gz # --r2_weighted=1  #--
	${dsistudio}/dsi_studio --action=exp  --source=${output}/dwi.src.nii.gz.odf4.f3.de7.rdi.gqi.0.75.fib.gz --export=fa0,gfa 
	${dsistudio}/dsi_studio --action=trk --source=${output}/dwi.src.nii.gz.odf4.f3.de7.rdi.gqi.0.75.fib.gz --method=0 --fiber_count=500000 --output=${output}/whole_brain_5k.trk
	gunzip ${output}/whole_brain_5k.trk
	#dti reconstruction
	${dsistudio}/dsi_studio --action=rec --thread=8 --source=${output}/dwi.src.nii.gz --method=1  #--output=${output}/fib.gz # --r2_weighted=1  #--
	${dsistudio}/dsi_studio --action=exp  --source=${output}/dwi.src.nii.gz.dti.fib.gz --export=fa0,md,rd,ad,
	python3 /space/rama/2/users/vsiless/scripts/imageUtils.py ${output}/dwi.src.nii.gz.dti.fib.gz.ad.nii.gz ${output}/ad.nii.gz
	python3 /space/rama/2/users/vsiless/scripts/imageUtils.py ${output}/dwi.src.nii.gz.dti.fib.gz.rd.nii.gz ${output}/rd.nii.gz
	python3 /space/rama/2/users/vsiless/scripts/imageUtils.py ${output}/dwi.src.nii.gz.dti.fib.gz.fa0.nii.gz ${output}/fa0.nii.gz
	python3 /space/rama/2/users/vsiless/scripts/imageUtils.py ${output}/dwi.src.nii.gz.dti.fib.gz.md.nii.gz ${output}/md.nii.gz
			
		
	#done

	chgrp -R fiber  ${SUBJECTS_DIR}/preprocess/${s}
	chmod -R 770  ${SUBJECTS_DIR}/preprocess/${s}
}

#Step 5:
#Prepare tract and T1 
function T1andtract()
{
	s=$1
	setenv SUBJECTS_DIR /space/erebus/1/users/data/preprocess/FS/MGH_HCP
	export SUBJECTS_DIR=/space/erebus/1/users/data/preprocess/FS/MGH_HCP
	trkToolsBin=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/trk_tools
		
	input=${SUBJECTS_DIR}/preprocess/${s}/
	output=${SUBJECTS_DIR}/preprocess/${s}/dsi_studio	
		
	#bbregister --s ${s} --mov ${input}/dMRI_topup_eddy.nii.gz --reg ${input}/dsi_studio/b02T1.dat --fslmat ${input}/dsi_studio/b02T1.mat --dti
	#dmri_trk2trk --in ${output}/whole_brain_5k.trk --out ${output}/streamlines2T1.trk --inref ${input}/dMRI_topup_eddy.nii.gz --outref /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/T1.mgz --reg b02T1.mat --fill
	gunzip ${output}/whole_brain_5k.trk
	python3 /space/rama/2/users/vsiless/scripts/imageUtils.py ${output}/dwi.src.nii.gz.odf4.f3.de7.rdi.gqi.0.5.fib.gz.fa0.nii.gz ${output}/fa.nii.gz
	${trkToolsBin} -i ${output}/fa.nii.gz -f ${output}/whole_brain_5k.trk -o ${output}/whole_brain_5k_u.trk -u

	python3 /space/rama/2/users/vsiless/scripts/imageUtils.py ${output}/dwi.src.nii.gz.odf4.f3.de7.rdi.gqi.0.5.fib.gz.fa0.nii.gz ${output}/gfa.nii.gz
	${trkToolsBin} -i ${output}/gfa.nii.gz -f ${output}/whole_brain_5k.trk -o ${output}/whole_brain_5k_u.trk -u


	bbregister --s ${s} --mov ${output}/fa.nii.gz --reg ${input}/dsi_studio/fa2T1.dat --fslmat ${input}/dsi_studio/fa2T1.mat --t1 --o ${input}/dsi_studio/fa2T1.nii.gz
	mri_vol2vol --targ ${output}/T1.nii.gz --mov ${output}/fa.nii.gz --o ${output}/T12fa.nii.gz --reg ${input}/dsi_studio/fa2T1.dat --inv
	mri_vol2vol --targ ${output}/wm2009parc.nii.gz --mov ${output}/fa.nii.gz --o ${output}/wm2009parc2fa.nii.gz --reg ${input}/dsi_studio/fa2T1.dat --inv --nearest
	#dmri_trk2trk --in ${output}/whole_brain_5k_u.trk --out ${output}/streamlines2T1_u.trk --inref ${output}/fa.nii.gz --outref /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/T1.mgz --reg ${input}/dsi_studio/fa2T1.mat --fill
	#dmri_trk2trk --in ${output}/streamlines2T1_u.trk --out ${output}/streamlines2T1_u.trk --inref ${output}/fa.nii.gz --outref /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/T1.mgz --reg /autofs/space/erebus_001/users/data/preprocess/anteriorPosterior.mat --fill
		
	mri_convert --in_type mgz --out_type nii --input_volume /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/T1.mgz --output_volume ${output}/T1.nii.gz
	/usr/pubsw/packages/dtk/current/track_info streamlines2T1.trk -vorder LPS LPS

	mri_aparc2aseg --s ${s} --labelwm --hypo-as-wm --rip-unknown --volmask --o /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/wm2009parc.mgz --ctxseg aparc.a2009s+aseg.mgz
	mri_convert --in_type mgz --out_type nii --input_volume /space/erebus/1/users/data/preprocess/FS/MGH_HCP/${s}/mri/wm2009parc.mgz --output_volume /space/erebus/1/users/data/preprocess/${s}/dsi_studio/wm2009parc.nii.gz
	mri_vol2vol --targ ${output}/wm2009parc.nii.gz --mov ${output}/fa.nii.gz --o ${output}/wm2009parc2fa.nii.gz --reg ${input}/dsi_studio/fa2T1.dat --inv --nearest

	chgrp -R fiber  ${SUBJECTS_DIR}/preprocess/${s}
	chmod -R 770  ${SUBJECTS_DIR}/preprocess/${s}
}
function AnatomiCuts()
{
	s=$1
	anatomiCutsBin=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/AnatomiCuts
	filtershortFibers=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/filterShortFibers
	input=/space/erebus/1/users/data/preprocess/${s}/dsi_studio
	output=/space/erebus/1/users/data/preprocess/${s}/AnatomiCuts_long55_dwi/
	mkdir ${output}
	mri_convert --in_orientation LAS --out_orientation LPS ${input}/wm2009parc2fa.nii.gz ${input}/wm2009parc2fa_LPS.nii.gz

	echo ${filtershortFibers} -s ${input}/wm2009parc2fa_LPS.nii.gz -i  ${input}//whole_brain_5k_u.trk -o  ${input}/streamlines_long55.trk -t 55
	${filtershortFibers} -s ${input}/wm2009parc2fa_LPS.nii.gz -i  ${input}//whole_brain_5k_u.trk -o  ${input}/streamlines_long55.trk -t 55
	#rm ${output}/*
	string="${anatomiCutsBin} -s ${input}/wm2009parc2fa_LPS.nii.gz -f ${input}/streamlines_long55.trk -nc -l a -w -c 200 -n 20 -e 500 -labels -o ${output}"
	echo $string
	#pbsubmit -n 1  -c "${string}"
	#${string}

}

function AnatomiCutsCorrespondencesToAll()
{
	hungarianBin=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin//FindCorrespondingClusters
	metrics=(labels)
	clusters=(50 75 100 150 200)
	num=${#subjects[@]}
 	echo ${num}
	launched=0

	for (( i=0; i<1; i++ ));
	do	
		ci=/space/erebus/1/users/data/preprocess/${subjects[i]}/AnatomiCuts_long55_dwi/
		segi=/space/erebus/1/users/data/preprocess/${subjects[i]}/dsi_studio/wm2009parc2fa_LPS.nii.gz				
		for (( j=1; j<${num}; j++ ));
		do
			echo ${subjects[i]}" and "${subjects[j]}				
			
			cj=/space/erebus/1/users/data/preprocess/${subjects[j]}/AnatomiCuts_long55_dwi/
			segj=/space/erebus/1/users/data/preprocess/${subjects[j]}/dsi_studio/wm2009parc2fa_LPS.nii.gz
			output=/space/erebus/1/users/data/preprocess/${subjects[j]}/Hungarian_AnatomiCuts_long55_dwi/
			mkdir -p ${output}
			for c in ${clusters[@]};
			do
				
				string="${hungarianBin} -s1 ${segi} -s2 ${segj} -h1 ${ci} -h2 ${cj} -o ${output}/${subjects[i]}_${subjects[j]}_c${c}_labels_hungarian.csv  -labels -hungarian -c ${c}"
				pbsubmit -n 1 -c "${string}"
				
:<<COMMENT
				binary=FindCorrespondingClusters
				running=`ps aux | grep $binary | wc -l`
				while [[ "$running" -ge 50 ]];
				do
					echo $running running - sleeping...
					sleep 15 
					running=`ps aux | grep $binary | wc -l`
				done
				${string}&
				sleep 5	
COMMENT
				
			done
			
		done

	done
}
function AnatomiCutsCorrespondences()
{
	hungarianBin=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin//FindCorrespondingClusters
	clusters=(50 75 100 150 200)
	s=$1
	to=BANDA001
	ci=/space/erebus/1/users/data/preprocess/${to}/AnatomiCuts_long55_dwi/
	segi=/space/erebus/1/users/data/preprocess/${to}/dsi_studio/wm2009parc2fa_LPS.nii.gz				

	cj=/space/erebus/1/users/data/preprocess/${s}/AnatomiCuts_long55_dwi/
	segj=/space/erebus/1/users/data/preprocess/${s}/dsi_studio/wm2009parc2fa_LPS.nii.gz
	output=/space/erebus/1/users/data/preprocess/${s}/Hungarian_AnatomiCuts_long55_dwi/
	mkdir -p ${output}
	for c in ${clusters[@]};
	do
		
		string="${hungarianBin} -s1 ${segi} -s2 ${segj} -h1 ${ci} -h2 ${cj} -o ${output}/${to}_${s}_c${c}_labels_hungarian.csv  -labels -hungarian -c ${c}"
		pbsubmit -n 1 -c "${string}"
		

	done
}
function AnatomiPop()
{
	s=$1
	echo ${s}
		
	trkToImageBin=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/itkMeshToImageFilterTest
	ci=/space/erebus/1/users/data/preprocess/${s}/AnatomiCuts_long55_dwi/
	base=/space/erebus/1/users/data/preprocess/${s}/dsi_studio/
	#mri_convert --in_orientation RAS --out_orientation RPS ${base}/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz  ${base}/fa2t1.nii.gz
	#mri_vol2vol --mov ${base}/fa2t1.nii.gz --targ ${base}/wm2009parc.nii.gz --o ${base}/fa2t1.nii.gz --reg ${base}/b02T1.dat #--no-resample 
	#mri_convert --in_orientation LIA --out_orientation LPS ${base}//fa2t1.nii.gz ${base}//fa2t1_LPS.nii.gz
	#flirt -in ${base}//fa2t1_LPS.nii.gz -ref ${FSL_DIR}/data/standard/FMRIB58_FA_1mm.nii.gz -out ${base}//fa2t12FMRIB58_l.nii.gz -omat ${base}//fa2t12FMRIB58.mat
	#fnirt --in=${base}//fa2t12FMRIB58_l.nii.gz --ref=${FSL_DIR}/data/standard/FMRIB58_FA_1mm.nii.gz --iout=${base}//fa2t12FMRIB58.nii.gz --fout=${base}//fa2t12FMRIB58_field.nii.gz
	
	#flirt -in ${base}/fa.nii.gz -ref ${FSL_DIR}/data/standard/FMRIB58_FA_1mm.nii.gz -out ${base}//fa2FMRIB58_l.nii.gz -omat ${base}//fa2FMRIB58.mat
	#fnirt --in=${base}//fa2FMRIB58_l.nii.gz --ref=${FSL_DIR}/data/standard/FMRIB58_FA_1mm.nii.gz --iout=${base}//fa2FMRIB58.nii.gz --fout=${base}//fa2FMRIB58_field.nii.gz
		
	#fsl_reg ${base}/fa.nii.gz $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz ${base}/fa2fmrib -e -FA
	#applywarp -i ${base}/fa.nii.gz -o ${base}/fa2FMRIB58.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w ${base}/fa2fmrib_warp


	cd  ${ci}
	mkdir ${ci}/images
	mkdir ${ci}/MNIimages
	#rm ${ci}/images/*
	#rm ${ci}/MNIimages/*
	for f in *trk 
	do
		${trkToImageBin} ${ci}/${f} ${base}/fa.nii.gz  ${ci}/images/${f%.trk}.nii.gz
		mri_convert --in_orientation LAS --out_orientation LPS  ${ci}/images/${f%.trk}.nii.gz  ${ci}/images/${f%.trk}.nii.gz
		#mri_convert --in_orientation LIA --out_orientation LPS ${ci}/images/${f%.trk}.nii.gz ${ci}/images/${f%.trk}.nii.gz
		#applywarp -i ${ci}/images/${f%.trk}.nii.gz  --premat=${base}//fa2FMRIB58.mat -r ${base}//fa2FMRIB58.nii.gz -o ${ci}/MNIimages/${f%.trk}.nii.gz
		#mri_vol2vol --mov  ${ci}/images/${f%.trk}.nii.gz  --targ ${base}//fa2FMRIB58.nii.gz --o ${ci}/MNIimages/${f%.trk}.nii.gz --fsl ${base}//fa2FMRIB58.mat --inv
		#applywarp -i ${ci}/MNIimages/${f%.trk}.nii.gz --warp=${base}/fa2FMRIB58_field.nii.gz  -r ${base}//fa2FMRIB58.nii.gz -o ${ci}/MNIimages/${f%.trk}.nii.gz
		#applywarp -i ${ci}/images/${f%.trk}.nii.gz --warp=${base}/fa2fmrib_warp.nii.gz  -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -o ${ci}/MNIimages/${f%.trk}.nii.gz
	done 
}

function AnatomiMeasures()
{
	files=( fa0.nii.gz md.nii.gz rd.nii.gz ad.nii.gz )
	names=( FA MD RD AD )
	s=$1

	output=/space/erebus/1/users/data/preprocess/${s}/AnatomiCuts_long55_dwi/measures
	mkdir ${output}
	input=/space/erebus/1/users/data/preprocess/${s}/AnatomiCuts_long55_dwi/images
	clusters=/space/erebus/1/users/data/preprocess/${s}/AnatomiCuts_long55_dwi/
	cd  ${input}
	mkdir ${input}/bin

	rm ${output}/*.csv
	for (( i=0; i< ${#files[@]};i++))
	do
		echo "Cluster,${names[i]}">${output}/${names[i]}.csv
	done
	for f in 1*nii.gz 
	do
		mri_binarize --i ${f} --min 1 --o ${input}/bin/${f}
	
		for (( i=0; i< ${#files[@]};i++))
		do
			a=`fslstats /space/erebus/1/users/data/preprocess/${s}/dsi_studio/${files[i]} -k ${input}/bin/${f} -m`
			echo "${input}/${f%.nii.gz}.trk,$a" >> ${output}/${names[i]}.csv
		done
	done
}

function motion()
{
	s=$1
	pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh motion_measures  $s"
	#pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh everything2T1Motion $s"
	#bash ${scriptFolder}/motion.sh ltaDiff $s
}
function snr()
{
        s=$1	
	/space/erebus/1/users/data/preprocess/BANDA100/dicom2nifty.csv ${PREPROCESS_DIR}/${s}/	
	bash ${scriptFolder}/motion.sh GetB0s $s
	bash ${scriptFolder}/motion.sh pre_compute $s
	bash ${scriptFolder}/motion.sh T1aparc2all $s

	bash ${scriptFolder}/motion.sh everything2T1SNR $s
}
function FS()
{
	s=$1
	if [[ ${SUBJECTS_DIR} ]]  && [[ ${PREPROCESS_DIR} ]]; then
		recon-all -subject ${s} -i ${PREPROCESS_DIR}/${s}/T1.nii.gz -T2 ${PREPROCESS_DIR}/${s}/T2.nii.gz -T2pial -all
		#recon-all -subject ${s} -T2 ${PREPROCESS_DIR}/${s}/T2.nii.gz -T2pial -all  -no-isrunning
	else
		echo "missing SUBJECTS_DIR or PREPROCESS_DIR"
	fi

}	

function prepFSFast()
{

	cd ${SUBJECTS_DIR}/
	fcseed-config -segid 2010 -fcname lh.isthmuscingulate.dat -fsd rest -mean -cfg mean.lh.isthmuscingulate.config -overwrite	
	fcseed-config -segid 1010 -fcname rh.isthmuscingulate.dat -fsd rest -mean -cfg mean.rh.isthmuscingulate.config -overwrite	
	fcseed-config -segid 1010 -segid 2010 -fcname mni.isthmuscingulate.dat -fsd rest -mean -cfg mean.isthmuscingulate.config -overwrite	

	fcseed-config -wm -fcname wm.dat -fsd rest -pca -cfg wm.config -overwrite
	fcseed-config -vcsf -fcname vcsf.dat -fsd rest -pca -cfg vcsf.config -overwrite
	
	mkanalysis-sess -analysis fc.isthmcseed.surf.lh -surface fsaverage lh -fwhm 5 -notask -taskreg lh.isthmuscingulate.dat 1 -nuisreg vcsf.dat 5 -nuisreg wm.dat 5  -mcextreg -polyfit 5 -nskip 4 -fsd rest -TR 0.8 -per-run -overwrite
	mkanalysis-sess -analysis fc.isthmcseed.surf.rh -surface fsaverage rh -fwhm 5 -notask -taskreg rh.isthmuscingulate.dat 1 -nuisreg vcsf.dat 5 -nuisreg wm.dat 5  -mcextreg -polyfit 5 -nskip 4 -fsd rest -TR 0.8 -per-run -overwrite

	mkanalysis-sess -analysis fc.isthmcseed.mni305 -mni305 2 -fwhm 5 -notask -taskreg mni.isthmuscingulate.dat 1 -nuisreg vcsf.dat 5 -nuisreg wm.dat 5  -mcextreg -polyfit 5 -nskip 4 -fsd rest -TR 0.8 -per-run -overwrite
}
function runFSFast()
{
	s=$1
	cd ${SUBJECTS_DIR}/
	echo ${SUBJECTS_DIR}
	echo ${s}

	preproc-sess -s ${s} -fsd rest -stc up -surface fsaverage lhrh -mni305 -fwhm 5 -per-run
	fcseed-sess  -s ${s} -cfg mean.lh.isthmuscingulate.config  -overwrite 
	fcseed-sess  -s ${s} -cfg mean.rh.isthmuscingulate.config  -overwrite 
	fcseed-sess  -s ${s} -cfg mean.isthmuscingulate.config  -overwrite 

	fcseed-sess -s ${s} -cfg wm.config  -overwrite
	fcseed-sess -s ${s} -cfg vcsf.config  -overwrite
	
	selxavg3-sess -s ${s} -a fc.isthmcseed.surf.lh  #-per-run
	selxavg3-sess -s ${s} -a fc.isthmcseed.surf.rh  #-per-run
	selxavg3-sess -s ${s} -a fc.isthmcseed.mni305  #-per-run
	
	#mkanalysis-sess -analysis ${conf}/fc.rhrccseed.surf.rh -surface fsaverage rh -fwhm 5 -notask -taskreg ${conf}/rh.rostalcingulate.dat 1 -nuisreg ${conf}/vcsf.dat 5 -nuisreg ${conf}/wm.dat 5  -mcextreg -polyfit 5 -nskip 4 -fsd rest -TR 0.8 -per-run -overwrite 
	#fcseed-sess  -s ${s} -cfg rh.rostalcingulate.config  -overwrite
	#mkanalysis-sess -analysis fc.lhrccseed.surf.lh -surface fsaverage lh -fwhm 5 -notask -taskreg lh.rostalcingulate.dat 1 -nuisreg vcsf.dat 5 -nuisreg wm.dat 5  -mcextreg -polyfit 5 -nskip 4 -fsd rest -TR 0.8 -per-run -overwrite
	#selxavg3-sess -s ${s} -a ${comf}/fc.rhrccseed.surf.rh -per-run
	#fcseed-config -segid 2026 -fcname rh.rostalcingulate.dat -fsd rest -mean -cfg ${conf}/mean.rh.rostalcingulate.config -overwrite
}

function FSFastGA()
{
	fileName=$1
	
	#isxconcat-sess
	string="-s HCD0026119_V1_MR -s HCD0114419_V1_MR -s HCD0128935_V1_MR -s HCD0182941_V1_MR -s HCD0504735_V1_MR -s HCD0514738_V1_MR -s HCD0541539_V1_MR -s HCD0643345_V1_MR -s HCD0848060_V1_MR -s HCD1039032_V1_MR -s HCD1106728_V1_MR -s HCD1205326_V1_MR -s HCD1227134_V1_MR -s HCD1411935_V1_MR -s HCD1435646_V1_MR -s HCD1441540_V1_MR -s HCD1452848_V1_MR -s HCD1464451_V1_MR -s HCD1504437_V1_MR -s HCD1527045_V1_MR -s HCD1560851_V1_MR -s HCD1630139_V1_MR -s HCD1681257_V1_MR -s HCD1783366_V1_MR -s HCD1871969_V1_MR -s HCD1872971_V1_MR -s HCD1881164_V1_MR -s HCD1886477_V1_MR -s HCD1900142_V1_MR"
	isxconcat-sess ${string} -analysis fc.isthmcseed.surf.lh -all-contrasts -o control_group_29

	isxconcat-sess ${string} -analysis fc.isthmcseed.mni305 -all-contrasts -o control_group_29

	isxconcat-sess ${string} -analysis fc.isthmcseed.surf.rh -all-contrasts -o control_group_29

<<hola
 -d . -analysis fc.lhrccseed.surf.lh -all-contrasts -o controls
	isxconcat-sess -s HCD0026119_V1_MR -s HCD0114419_V1_MR -s HCD0128935_V1_MR -s HCD0182941_V1_MR -s HCD0504735_V1_MR -s HCD0514738_V1_MR -s HCD0541539_V1_MR -s HCD0643345_V1_MR -s HCD0848060_V1_MR -s HCD1039032_V1_MR -s HCD1106728_V1_MR -s HCD1205326_V1_MR -s HCD1227134_V1_MR -s HCD1411935_V1_MR -s HCD1435646_V1_MR -s HCD1441540_V1_MR -s HCD1452848_V1_MR -s HCD1464451_V1_MR -s HCD1504437_V1_MR -s HCD1527045_V1_MR -s HCD1560851_V1_MR -s HCD1630139_V1_MR -s HCD1681257_V1_MR -s HCD1783366_V1_MR -s HCD1871969_V1_MR -s HCD1872971_V1_MR -s HCD1881164_V1_MR -s HCD1886477_V1_MR -s HCD1900142_V1_MR  -s HCD1957171_V1_MR -s HCD1978987_V1_MR -s HCD2046943_V1_MR -s HCD2063034_V1_MR -s HCD2064440_V1_MR -s HCD2109638_V1_MR -s HCD2140127_V1_MR -s HCD2335344_V1_MR -s HCD2340640_V1_MR -s HCD2400026_V1_MR -s HCD2400632_V1_MR -s HCD2748672_V1_MR -s HCD2754061_V1_MR -s HCD2768981_V1_MR -s HCD2901654_V1_MR -analysis fc.isthmcseed.surf.lh -all-contrasts -o control_group_44

hola

}

function FSFastGABANDA()
{

	string="-s HCD0026119_V1_MR -s HCD0114419_V1_MR -s HCD0128935_V1_MR -s HCD0182941_V1_MR -s HCD0504735_V1_MR -s HCD0514738_V1_MR -s HCD0541539_V1_MR -s HCD0643345_V1_MR -s HCD0848060_V1_MR -s HCD1039032_V1_MR -s HCD1106728_V1_MR -s HCD1205326_V1_MR -s HCD1227134_V1_MR -s HCD1411935_V1_MR -s HCD1435646_V1_MR -s HCD1441540_V1_MR -s HCD1452848_V1_MR -s HCD1464451_V1_MR -s HCD1504437_V1_MR -s HCD1527045_V1_MR -s HCD1560851_V1_MR -s HCD1630139_V1_MR -s HCD1681257_V1_MR -s HCD1783366_V1_MR -s HCD1871969_V1_MR -s HCD1872971_V1_MR -s HCD1881164_V1_MR -s HCD1886477_V1_MR -s HCD1900142_V1_MR -s BANDA002  -s BANDA050 -s BANDA003  -s BANDA058 -s BANDA004  -s BANDA061 -s BANDA008  -s BANDA071 -s BANDA009  -s BANDA078 -s BANDA010  -s BANDA087 -s BANDA011  -s BANDA105 -s BANDA012  -s BANDA107 -s BANDA013  -s BANDA117  -s BANDA014  -s BANDA122 -s BANDA016  -s BANDA124 -s BANDA018  -s BANDA128 -s BANDA033  -s BANDA136 -s BANDA043  -s BANDA140 -s BANDA046"


	isxconcat-sess ${string} -analysis fc.isthmcseed.surf.lh -all-contrasts -o HCD_BANDA

	isxconcat-sess ${string} -analysis fc.isthmcseed.mni305 -all-contrasts -o HCD_BANDA

	isxconcat-sess ${string} -analysis fc.isthmcseed.surf.rh -all-contrasts -o HCD_BANDA

}
function FSFastcpBANDAtoHCD()
{
	
	#HCDs=( HCD0026119_V1_MR HCD0114419_V1_MR HCD0128935_V1_MR HCD0182941_V1_MR HCD0504735_V1_MR HCD0514738_V1_MR HCD0541539_V1_MR HCD0643345_V1_MR HCD0848060_V1_MR HCD1039032_V1_MR HCD1106728_V1_MR HCD1205326_V1_MR HCD1227134_V1_MR HCD1411935_V1_MR HCD1435646_V1_MR HCD1441540_V1_MR HCD1452848_V1_MR HCD1464451_V1_MR HCD1504437_V1_MR HCD1527045_V1_MR HCD1560851_V1_MR HCD1630139_V1_MR HCD1681257_V1_MR HCD1783366_V1_MR HCD1871969_V1_MR HCD1872971_V1_MR HCD1881164_V1_MR HCD1886477_V1_MR HCD1900142_V1_MR )

	BANDAs=(BANDA002  BANDA050 BANDA003 BANDA058 BANDA004 BANDA061 BANDA008 BANDA071 BANDA009 BANDA078 BANDA010 BANDA087 BANDA011 BANDA105 BANDA012 BANDA107 BANDA013 BANDA117 BANDA014 BANDA122 BANDA016 BANDA124 BANDA018 BANDA128 BANDA033 BANDA136 BANDA043 BANDA140 BANDA046)

	HCDdir=/space/erebus/1/users/HCPD/preprocessed_viv/FS_STRUCTURE/
	BANDAdir=/space/erebus/1/users/data/preprocess/FS/MGH_HCP/


	for s in ${BANDAs[@]}; 
	do
		echo ${s}
		mkdir ${HCDdir}/${s}
		#cp -R ${BANDAdir}/${s}/mri ${HCDdir}/${s}/
		#cp -R ${BANDAdir}/${s}/surf ${HCDdir}/${s}/
		#cp -R ${BANDAdir}/${s}/rest ${HCDdir}/${s}/
		cp  ${BANDAdir}/${s}/subjectname ${HCDdir}/${s}/

	done
}
function runBedpostx()
{
	s=$1
	rm  ${PREPROCESS_DIR}/${s}/bedpostx/data_* 
	rm -r  ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX/* 

	bedpostx ${PREPROCESS_DIR}/${s}/bedpostx -n 3 
}
function runBedpostx_mgh()
{
	file=$1
	extraParams=$2
	for si in `cat ${file}`;
	do

                subject=${si/^M/}                                                                                                     
		echo ${PREPROCESS_DIR}
		echo ${extraParams}
		if [[  "${extraParams}" == "HCPD" ]]; then
			s=${subject}_V1_MR
		else
			s=${subject}
		fi
		
		echo   ${s}
		running=`qstat | grep vsiless | wc -l`
		while [[ "$running" -ge 800 ]];
		do
			echo $running running - sleeping...
			sleep 10m 
			running=`qstat | grep vsiless | wc -l`
		done
		rm  ${PREPROCESS_DIR}/${s}/bedpostx/data_* 
		mv -r  ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX/  ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX.old/  

		bedpostx_mgh ${PREPROCESS_DIR}/${s}/bedpostx -n 3 
			
		sleep 10 
	done
}
function T12diff()
{
	s=$1	

	files=(dyads1_dispersion mean_fsumsamples mean_f1samples mean_f2samples mean_f3samples)
	bbregister --s ${s} --mov ${PREPROCESS_DIR}/${s}/dMRI_AP_b0.nii.gz --reg ${PREPROCESS_DIR}/${s}/b02T1.lta  --o ${PREPROCESS_DIR}/${s}/b02T1.nii.gz --t2
	mri_vol2vol --targ ${PREPROCESS_DIR}/${s}/dMRI_AP_b0.nii.gz --mov ${SUBJECTS_DIR}/${s}/mri/wmparc.mgz --o ${PREPROCESS_DIR}/${s}/wmparc2diff.nii.gz --lta-inv ${PREPROCESS_DIR}/${s}/b02T1.lta  --nearest 
	for f in ${files[@]};
	do
 mri_copy_params ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX/${f}.nii.gz ${PREPROCESS_DIR}/${s}/dMRI_AP_b0.nii.gz ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX/${f}_u.nii.gz --size
flirt -in ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX/${f}_u.nii.gz ${PREPROCESS_DIR}/${s}/dMRI_AP_b0.nii.gz ${PREPROCESS_DIR}/${s}/bedpostx.bedpostX/${f}_u.nii.gz
	done
}
<<permissions
chgrp -R fiber  ${SUBJECTS_DIR}/preprocess/${s}
chmod -R 770  ${SUBJECTS_DIR}/preprocess/${s}

chgrp -R fiber  ${SUBJECTS_DIR}/${s}
chmod -R 770  ${SUBJECTS_DIR}/${s}

chgrp -R fiber  ${SUBJECTS_DIR}/tfMRI_output
chmod -R 770  ${SUBJECTS_DIR}/tfMRI_output

chgrp -R fiber  ${SUBJECTS_DIR}/BIDS
chmod -R 770  ${SUBJECTS_DIR}/BIDS
permissions


$@
