#!/bin/bash
# @Viviana Siless : vsiless@mgh.harvard.edu
folder=/space/erebus/1/users/data
scriptFolder=/space/erebus/1/users/data/code/scripts
subjects=( BANDA126 ) #BANDA105 ) #BANDA102 ) #BANDA098 BANDA099 BANDA100 ) #BANDA097 ) #BANDA092 BANDA093 BANDA094 ) #BANDA091 ) #BANDA089 BANDA090 ) #BANDA084 BANDA085 BANDA086 BANDA087) #BANDA088) #BANDA087 ) #BANDA085 BANDA086 ) #BANDA084 ) #BANDA083 ) #BANDA080 BANDA081 ) #BANDA082 ) #BANDA080 BANDA081 ) #BANDA066 ) #BANDA065 BANDA064 ) #BANDA063 ) #BANDA062) #BANDA061) #BANDA060 ) #BANDA058 BANDA059 BANDA057) #BANDA056 ) #BANDA057 ) #BANDA056_test ) #BANDA056 ) #BANDA044 BANDA045 BANDA046 BANDA048 BANDA047 BANDA048 BANDA049 BANDA050 BANDA051 BANDA052 BANDA053 BANDA054) #BANDA055 ) #BANDA053 BANDA054 ) #BANDA051 BANDA050_2 BANDA050) #BANDA050 ) #BANDA046 BANDA047 BANDA048 BANDA049 ) #BANDA046 ) #BANDA044 BANDA045 ) #BANDA042 BANDA043) #BANDA037 BANDA038 BANDA039 BANDA040 BANDA041 ) #BANDA043 BANDA042 ) #BANDA041 ) #BANDA040 ) #BANDA039) #BANDA037 BANDA038) #BANDA029 BANDA030 BANDA031 BANDA032 BANDA033 BANDA034 BANDA035 BANDA036 ) #BANDA034 ) #BANDA032 BANDA033 ) #BANDA031 ) #BANDA030 ) #BANDA018 ) #BANDA017 ) #BANDA013)
#PANDA033 PANDA029 ) #PANDA030 ) #PANDA029 ) #PANDA027_test #PANDA028_test #PANDA028 ) #PANDA027 PANDA025b ) #PANDA025 ) #PANDA004b PANDA026 ) #4 ) #PANDA002d )  #PANDA022 PANDA023 PANDA021 PANDA011 PANDA013 PANDA014 PANDA016 PANDA017 PANDA018 PANDA019 PANDA020) #PANDA011 ) #PANDA017) #PANDA013)) #PANDA024_2 )  
#subjects=( BANDA001 BANDA002 BANDA003 BANDA004 BANDA005 BANDA006 BANDA007 BANDA008 )
#subjects=( BANDA009  BANDA010 BANDA011 BANDA012  BANDA013 BANDA014 BANDA015 )

#subjects=( BANDA001 BANDA016 BANDA009 ) # BANDA017 BANDA018 BANDA019 BANDA020 BANDA021 )
#subjects=(BANDA001  BANDA002 BANDA003 BANDA004 BANDA005 BANDA006 BANDA007 BANDA008 BANDA009  BANDA010 BANDA011 BANDA012  BANDA013 BANDA014 BANDA015 BANDA016 BANDA017 BANDA018 BANDA019 BANDA020 BANDA021 BANDA022 BANDA023 BANDA024 BANDA025 BANDA026 BANDA027 BANDA028 BANDA029 BANDA030 )
#subjects=(BANDA001 BANDA005 BANDA010 BANDA015 BANDA020 BANDA025 BANDA030 BANDA035 BANDA040 BANDA045 BANDA050 BANDA054 BANDA058 BANDA063 BANDA001V BANDA006 BANDA011  BANDA016 BANDA021 BANDA026 BANDA031 BANDA036 BANDA041 BANDA046 BANDA055 BANDA059 BANDA064  BANDA002 BANDA007 BANDA012 BANDA017 BANDA022 BANDA027 BANDA032 BANDA037 BANDA042 BANDA047 BANDA051 BANDA056 BANDA060 BANDA003 BANDA008 BANDA013 BANDA018 BANDA023 BANDA028 BANDA033  BANDA038 BANDA043 BANDA048 BANDA052 BANDA061 BANDA004 BANDA009 BANDA014 BANDA019 BANDA024 BANDA029 BANDA034 BANDA039 BANDA044 BANDA049 BANDA053 BANDA057 BANDA062 )
#subjects=(BANDA061 BANDA063 BANDA064 BANDA065  BANDA066 BANDA031 BANDA005 BANDA054 BANDA058 BANDA045 BANDA067 BANDA068 BANDA069 BANDA070 BANDA071)
#subjects=( BANDA072 BANDA073 BANDA074 BANDA075 BANDA076 BANDA077 BANDA078 BANDA079 BANDA080 BANDA081 BANDA082 BANDA083 BANDA084 BANDA085 BANDA086 BANDA087 BANDA088 BANDA089 BANDA090 BANDA091 BANDA092 BANDA093 BANDA094 BANDA095 BANDA096 BANDA097 BANDA098 BANDA099 BANDA100 BANDA101 BANDA102 BANDA103 BANDA104 BANDA105 BANDA106)
#subjects=( BANDA070 BANDA071 BANDA072 BANDA073 BANDA074 BANDA075  )

#subjects=(BANDA061 )
dsistudio=/autofs/cluster/pubsw/2/pubsw/Linux2-2.3-x86_64/packages/DSI-Studio/1.0/bin/
dsistudio=/autofs/cluster/pubsw/2/pubsw/Linux2-2.3-x86_64/packages/DSI-Studio/20170822/bin/

#Step 1
#This function should be run after unpacksdcmdir on the BANDA subject's directory, generating a scan.txt file
#A file dicom2nifty.csv is needed mapping each scan name to the nifty output name. 
#TODO: if dicom2nifty.csv is not found on the subject's output preprocess directorty, we should use the dicom2nifty file on the preprocess level folder. Meaning that if everything is normal, we don't need to re-specify the dicom2nifty file. [if no retro-recons happened during the scan session, or error]
function dicomToNifty()
{


for s in ${subjects[@]};
do
	echo $s 
	fout=${folder}/preprocess/$s
	mkdir -p ${fout}
	IFS=","
	while read scan skip niftyName protocol 
        do
		echo $i
		echo python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} ${niftyName}
		dicom=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} `)
		echo ${dicom}
		#mri_convert ${folder}/$s/${dicom} ${output}/${niftyName}.nii.gz 
		#pbsubmit -n 1 -m rjj7 -c "mri_convert ${folder}/$s/${dicom} ${fout}/${niftyName}.nii.gz "
		#pbsubmit -n 1 -c "mri_convert ${folder}/dicoms/$s/${dicom} ${fout}/${niftyName}.nii.gz "
		mri_convert ${folder}/dicoms/$s/${dicom} ${fout}/${niftyName}.nii.gz 
	done < $fout/dicom2nifty.csv



:<<perm
	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}

	chgrp -R fiber  ${folder}/${s}
	chmod -R 770  ${folder}/${s}
perm
done

}
# Step 5	
# after running everything, remember to grant permission to the rest of the group
function grantPermissions()
{

for s in ${subjects[@]};
do
	fout=${folder}/preprocess/$s

	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}

	chgrp -R fiber  ${folder}/${s}
	chmod -R 770  ${folder}/${s}
done

}
# Step 2
# For diffusion we merge all the diffusion files into one for runnning eddy which takes care of motion correction. For fMRI is not necesary since we use mcflirt to align volumes to the distortion maps /spin echos.
function mergeDiffusion()
{
	for s in ${subjects[@]};
	do

		fout=${folder}/preprocess/$s/
		study=CMRR
		study=

		mv ${fout}/${study}//dMRI_AP1.voxel_space.bvecs ${fout}/${study}//dMRI_AP1.bvecs
		mv ${fout}/${study}//dMRI_AP2.voxel_space.bvecs ${fout}/${study}/dMRI_AP2.bvecs
		mv ${fout}/${study}//dMRI_PA1.voxel_space.bvecs ${fout}/${study}//dMRI_PA1.bvecs
		mv ${fout}/${study}//dMRI_PA2.voxel_space.bvecs ${fout}/${study}/dMRI_PA2.bvecs

		fslmerge -t  ${fout}/${study}/dMRI_PA.nii.gz ${fout}/${study}/dMRI_PA1.nii.gz ${fout}/${study}/dMRI_PA2.nii.gz
		fslmerge -t  ${fout}/${study}/dMRI_AP.nii.gz ${fout}/${study}/dMRI_AP1.nii.gz ${fout}/${study}/dMRI_AP2.nii.gz

		rm ${out_folder}/double.b*
		rm ${fout}/${study}/bvecs
		rm ${fout}/${study}/bvals
		cat ${fout}/${study}/dMRI_AP1.bvals ${fout}/${study}/dMRI_AP2.bvals  >> ${fout}/${study}/bvals
		cat ${fout}/${study}/dMRI_PA1.bvals ${fout}/${study}/dMRI_PA2.bvals  >> ${fout}/${study}/bvals

		cat ${fout}/${study}/dMRI_AP1.bvecs ${fout}/${study}/dMRI_AP2.bvecs  >> ${fout}/${study}/bvecs
		cat ${fout}/${study}/dMRI_PA1.bvecs ${fout}/${study}/dMRI_PA2.bvecs  >> ${fout}/${study}/bvecs

		fslmerge -t  ${fout}/${study}/dMRI.nii.gz ${fout}/${study}/dMRI_PA.nii.gz ${fout}/${study}/dMRI_AP.nii.gz
	done
}
#Step 3
# Run top up to correct for spin echo distortions AP PA.
function distortionCorrection()
{
	user="-m rjj7"
	#user="-m rjj7"
	#user="-m vsiless"
	#user=

	for s in ${subjects[@]};
	do


#:<<ALL_FUNCTIONAL
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz AP"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz PA"
	
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA"
	
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA"

		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA"

		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_gambling1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP"
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_gambling2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA"
#ALL_FUNCTIONAL

#DIFFUSION
		pbsubmit -n 1  ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI.nii.gz dMRI_AP.nii.gz dMRI_PA.nii.gz AP bvecs bvals"
	done
}

# Step 4:
# Obtain the tractography
function tractography()
{
	#study=CMRR
	#for s in ${subjects[@]};
	#do
	s=$1
		input=${folder}/preprocess/${s}/
		output=${folder}/preprocess/${s}/dsi_studio
		#input=${folder}/preprocess/${s}/${study}/
		#output=${folder}/preprocess/${s}/${study}/dsi_studio
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

	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}
}

#Step 5:
#Prepare tract and T1 
function T1andtract()
{
	#study=CMRR
	#for s in ${subjects[@]};
	#do
	s=$1
		setenv SUBJECTS_DIR /space/erebus/1/users/data/preprocess/FS/MGH_HCP
		export SUBJECTS_DIR=/space/erebus/1/users/data/preprocess/FS/MGH_HCP
		trkToolsBin=/space/rama/2/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/trk_tools
		
		input=${folder}/preprocess/${s}/
		output=${folder}/preprocess/${s}/dsi_studio	
		
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
	#done

	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}
}
function AnatomiCuts()
{
	#for s in ${subjects[@]};
	#do
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
	#done

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
	#done
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
function forAllSubjects()
{
	num=${#subjects[@]}
 	echo ${num}
	for (( i=0; i<${num}; i++ ));
	do	
		pbsubmit -n 2 -c "bash ${0} $1 ${subjects[i]}"
	done
}


function alignToVTK()
{
		track_info ${output}/whole_brain_5k.trk -vorder LPS LAS

		mri_convert $input/brain.mgz ${output}/brain.nii.gz
		mri_convert ${input}/aparc+aseg.mgz ${output}/aparc+aseg.nii.gz
		mri_convert ${input}/aparc.a2009s+aseg.mgz ${output}/aparc.a2009s+aseg.nii.gz
	
		/local_mount/space/namic/2/users/vsiless/programs/MedINRIA -gui 0 -mod imagefusion -f ${output}/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -m ${output}/brain.nii.gz -r null -o  ${output}/brain2dwi.nii.gz -ot ${output}/brain2dwi.mat 
		/local_mount/space/namic/2/users/vsiless/programs/MedINRIA -gui 0 -mod imagefusion -f ${output}/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -m ${output}/aparc+aseg.nii.gz  -t ${output}/brain2dwi.mat -o  ${output}/aparc+aseg2dwi.nii.gz -i nn
		/local_mount/space/namic/2/users/vsiless/programs/MedINRIA -gui 0 -mod imagefusion -f ${output}/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -m ${output}/aparc.a2009s+aseg.nii.gz -t ${output}/brain2dwi.mat -o  ${output}/aparc.a2009s+aseg2dwi.nii.gz  -i nn

		mri_convert --in_orientation LAS --out_orientation LPS ${output}/aparc.a2009s+aseg2dwi.nii.gz ${output}/aparc.a2009s+aseg2dwi_LPS.nii.gz
		python /local_mount/space/namic/2/users/vsiless/scripts/hcp_changeHeader.py  ${output}/aparc.a2009s+aseg2dwi_LPS.nii.gz ${output}/aparc.a2009s+aseg2dwi.nii.gz
		rm ${output}/aparc.a2009s+aseg2dwi_LPS.nii.gz

		mri_convert --in_orientation LAS --out_orientation LPS ${output}/aparc+aseg2dwi.nii.gz ${output}/aparc+aseg2dwi_LPS.nii.gz
		python /local_mount/space/namic/2/users/vsiless/scripts/hcp_changeHeader.py  ${output}/aparc+aseg2dwi_LPS.nii.gz ${output}/aparc+aseg2dwi.nii.gz
		rm ${output}/aparc+aseg2dwi_LPS.nii.gz

		mri_convert --in_orientation LAS --out_orientation LPS ${output}/brain2dwi.nii.gz ${output}/brain2dwi_LPS.nii.gz
		python /local_mount/space/namic/2/users/vsiless/scripts/hcp_changeHeader.py  ${output}/brain2dwi_LPS.nii.gz ${output}/brain2dwi.nii.gz
		rm ${output}/brain2dwi_LPS.nii.gz


		python /local_mount/space/namic/2/users/vsiless/scripts/trk2vtk.py ${output}/whole_brain_5k.trk ${output}/whole_brain_5k.vtk # ${out_folder}/${s}/wmparc2dwi_LPS.nii.gz ${out_folder}/${s}/tracts/wmparc2dwi.nii.gz

}

function distortionCorrection_old()
{
for s in ${subjects[@]};
do
#CMRR - run it on rest AP PA, conflict 1 2 3 4, and facematching 1 2
#	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP
#	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA

:<<NO_LAUNCHPAD
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz AP
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz PA
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA

	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_gambling1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_gambling2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA

	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP
	bash ${scriptFolder}/distortion_v2	.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA

	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA

	pbsubmit -n 1 -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz AP"
	pbsubmit -n 1 -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz PA"
	pbsubmit -n 1 -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz AP"
	pbsubmit -n 1 -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz PA"


	fout=${folder}/preprocess/$s/

	mv ${fout}/CMRR//dMRI_AP1.voxel_space.bvecs ${fout}/CMRR//dMRI_AP1.bvecs
	mv ${fout}/CMRR//dMRI_AP2.voxel_space.bvecs ${fout}/CMRR/dMRI_AP2.bvecs
	mv ${fout}/CMRR//dMRI_PA1.voxel_space.bvecs ${fout}/CMRR//dMRI_PA1.bvecs
	mv ${fout}/CMRR//dMRI_PA2.voxel_space.bvecs ${fout}/CMRR/dMRI_PA2.bvecs

	fslmerge -t  ${fout}/CMRR/dMRI_PA.nii.gz ${fout}/CMRR/dMRI_PA1.nii.gz ${fout}/CMRR/dMRI_PA2.nii.gz
	fslmerge -t  ${fout}/CMRR/dMRI_AP.nii.gz ${fout}/CMRR/dMRI_AP1.nii.gz ${fout}/CMRR/dMRI_AP2.nii.gz

	rm ${out_folder}/double.b*
	rm ${fout}/CMRR/bvecs
	rm ${fout}/CMRR/bvals
	cat ${fout}/CMRR/dMRI_AP1.bvals ${fout}/CMRR/dMRI_AP2.bvals  >> ${fout}/CMRR/bvals
	cat ${fout}/CMRR/dMRI_PA1.bvals ${fout}/CMRR/dMRI_PA2.bvals  >> ${fout}/CMRR/bvals

	cat ${fout}/CMRR/dMRI_AP1.bvecs ${fout}/CMRR/dMRI_AP2.bvecs  >> ${fout}/CMRR/bvecs
	cat ${fout}/CMRR/dMRI_PA1.bvecs ${fout}/CMRR/dMRI_PA2.bvecs  >> ${fout}/CMRR/bvecs

	fslmerge -t  ${fout}/CMRR/dMRI.nii.gz ${fout}/CMRR/dMRI_PA.nii.gz ${fout}/CMRR/dMRI_AP.nii.gz
	bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI.nii.gz dMRI_AP.nii.gz dMRI_PA.nii.gz AP bvecs bvals
NO_LAUNCHPAD

	user=rjj7
	user=vsiless

:<<BANDA_TASK
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz AP"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_1.nii.gz fMRI_SpinEchoFieldMap_AP_1.nii.gz PA"
	
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA"
	
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA"

	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz AP"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_3.nii.gz fMRI_SpinEchoFieldMap_AP_3.nii.gz PA"

	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_gambling1_AP.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz AP"
	pbsubmit -n 1 -m ${user} -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_gambling2_PA.nii.gz fMRI_SpinEchoFieldMap_PA_2.nii.gz fMRI_SpinEchoFieldMap_AP_2.nii.gz PA"
BANDA_TASK

	#pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI.nii.gz dMRI_AP.nii.gz dMRI_PA.nii.gz AP bvecs bvals"
#:<<DIFFUSION
	fout=${folder}/preprocess/$s/
	study=CMRR
	study=

	mv ${fout}/${study}//dMRI_AP1.voxel_space.bvecs ${fout}/${study}//dMRI_AP1.bvecs
	mv ${fout}/${study}//dMRI_AP2.voxel_space.bvecs ${fout}/${study}/dMRI_AP2.bvecs
	mv ${fout}/${study}//dMRI_PA1.voxel_space.bvecs ${fout}/${study}//dMRI_PA1.bvecs
	mv ${fout}/${study}//dMRI_PA2.voxel_space.bvecs ${fout}/${study}/dMRI_PA2.bvecs

	fslmerge -t  ${fout}/${study}/dMRI_PA.nii.gz ${fout}/${study}/dMRI_PA1.nii.gz ${fout}/${study}/dMRI_PA2.nii.gz
	fslmerge -t  ${fout}/${study}/dMRI_AP.nii.gz ${fout}/${study}/dMRI_AP1.nii.gz ${fout}/${study}/dMRI_AP2.nii.gz

	rm ${out_folder}/double.b*
	rm ${fout}/${study}/bvecs
	rm ${fout}/${study}/bvals
	cat ${fout}/${study}/dMRI_AP1.bvals ${fout}/${study}/dMRI_AP2.bvals  >> ${fout}/${study}/bvals
	cat ${fout}/${study}/dMRI_PA1.bvals ${fout}/${study}/dMRI_PA2.bvals  >> ${fout}/${study}/bvals

	cat ${fout}/${study}/dMRI_AP1.bvecs ${fout}/${study}/dMRI_AP2.bvecs  >> ${fout}/${study}/bvecs
	cat ${fout}/${study}/dMRI_PA1.bvecs ${fout}/${study}/dMRI_PA2.bvecs  >> ${fout}/${study}/bvecs

	fslmerge -t  ${fout}/${study}/dMRI.nii.gz ${fout}/${study}/dMRI_PA.nii.gz ${fout}/${study}/dMRI_AP.nii.gz
	pbsubmit -n 1  -m ${user} rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI.nii.gz dMRI_AP.nii.gz dMRI_PA.nii.gz AP bvecs bvals"
#DIFFUSION

:<<COM
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_PA1.nii.gz dMRI_AP1.nii.gz dMRI_PA1.nii.gz PA dMRI_PA1.bvecs dMRI_PA1.bvals"
	
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_AP2.nii.gz  dMRI_PA2.nii.gz dMRI_AP2.nii.gz AP dMRI_AP2.bvecs dMRI_AP2.bvals"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_PA2.nii.gz  dMRI_PA2.nii.gz dMRI_AP2.nii.gz PA dMRI_PA2.bvecs dMRI_PA2.bvals"


	mv ${fout}/CMRR//dMRI_AP1.voxel_space.bvecs ${fout}/CMRR//dMRI_AP1.bvecs
	mv ${fout}/CMRR//dMRI_AP2.voxel_space.bvecs ${fout}/CMRR/dMRI_AP2.bvecs
	mv ${fout}/CMRR//dMRI_PA1.voxel_space.bvecs ${fout}/CMRR//dMRI_PA1.bvecs
	mv ${fout}/CMRR//dMRI_PA2.voxel_space.bvecs ${fout}/CMRR/dMRI_PA2.bvecs

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_AP1.nii.gz dMRI_AP1.nii.gz dMRI_PA1.nii.gz AP dMRI_AP1.bvecs dMRI_AP1.bvals"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_PA1.nii.gz dMRI_AP1.nii.gz dMRI_PA1.nii.gz PA dMRI_PA1.bvecs dMRI_PA1.bvals"
	
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_AP2.nii.gz  dMRI_PA2.nii.gz dMRI_AP2.nii.gz AP dMRI_AP2.bvecs dMRI_AP2.bvals"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR dMRI $s dMRI_PA2.nii.gz  dMRI_PA2.nii.gz dMRI_AP2.nii.gz PA dMRI_PA2.bvecs dMRI_PA2.bvals"

	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA"

	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA"

	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 CMRR fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA"
COM

:<<MGH_HCP 

	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s fMRI_rest1_AP.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s fMRI_rest2_PA.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz PA"


	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz PA"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz PA"

	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz AP"
	pbsubmit -n 1  -m rjj7 -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 MGH_HCP fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz PA"
MGH_HCP

#ABCD
#	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest1.nii.gz
#	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest2.nii.gz

# 	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict1.nii.gz
#  	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict2.nii.gz
#	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict3.nii.gz
#	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict4.nii.gz

# 	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching1.nii.gz
# 	bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching2.nii.gz



chgrp -R fiber  ${folder}/preprocess/${s}
chmod -R 770  ${folder}/preprocess/${s}

chgrp -R fiber  ${folder}/${s}
chmod -R 770  ${folder}/${s}


done	
:<<COMMENT
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s fMRI_rest1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s fMRI_rest2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_faceMatching2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_conflict1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_conflict2_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_conflict3_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_conflict4_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s fMRI_SpinEchoFieldMap_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz PA "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_DistortionMap_PA.nii.gz "
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_DistortionMap_PA.nii.gz "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching1.nii.gz "
 	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching2.nii.gz "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict1.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict2.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict3.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict4.nii.gz "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest1.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest2.nii.gz "
COMMENT

	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}
}
function dicomToNifty2()
{

for s in ${subjects[@]};
do


	echo $s
	#unpacksdcmdir -src /space/erebus/1/users/data/dicoms/$s/ -targ /space/erebus/1/users/data/dicoms/$s/ -scanonly scan.txt
	fout=${folder}/preprocess/$s

!<<EDITS
	IFS ","
	while read scan skip niftyName protocol
      	do
		echo python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} ${niftyName}
		dicom=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} `)
		echo ${dicom}
		#mri_convert ${folder}/$s/${dicom} ${niftyName}.nii.gz 
		pbsubmit -n 1 -m rjj7 -c "mri_convert ${folder}/$s/${dicom} ${niftyName}.nii.gz "
	done < $fout/dicom2nifty.csv
	
	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}

	chgrp -R fiber  ${folder}/${s}
	chmod -R 770  ${folder}/${s}
EDITS

#!<<SUBDIRECTORIES
	
	mkdir -p ${fout}/ABCD/
	mkdir -p ${fout}/iPAT2/
	mkdir -p ${fout}/CMRR/
	mkdir -p ${fout}/MGH_HCP/ #

#	rm ${fout}/ABCD/*
#	rm ${fout}/iPAT2/*
#	rm ${fout}/CMRR/*
	IFS=","
	while read scan skip niftyName protocol
        do
		echo $i
		if [ -z "${scan##*iPAT2*}" ]; then
			output=${fout}/iPAT2
		elif [ -z "${scan##*ABCD*}" ]; then
			output=${fout}/ABCD
		elif [ -z "${scan##*CMRR*}" ] || [ -z "${scan##*HCP_CMRR*}" ]; then
			output=${fout}/CMRR
		elif [ -z "${scan##*MGH_HCP*}" ]  || [ -z "${scan##*mgh_for_AY*}" ] || [ -z "${scan##*HCP_MGH*}" ]; then
			output=${fout}/MGH_HCP
		else
			output=${fout}/weirdddd
		fi
		
		echo python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} ${niftyName}
		dicom=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scan} ${skip} `)
		echo ${dicom}
		#mri_convert ${folder}/$s/${dicom} ${output}/${niftyName}.nii.gz 
		pbsubmit -n 1 -m rjj7 -c "mri_convert ${folder}/$s/${dicom} ${output}/${niftyName}.nii.gz "
	done < $fout/dicom2nifty.csv

	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}

	chgrp -R fiber  ${folder}/${s}
	chmod -R 770  ${folder}/${s}
#SUBDIRECTORIES
done


}

function dicomToNifty_old()
{

scanNames=( "CMRR_SpinEchoFieldMap_AP" "CMRR_SpinEchoFieldMap_PA" "CMRR_fMRI_rest_AP 2" "CMRR_fMRI_rest_PA 2" "CMRR_fMRI_faceMatching_AP 2" "CMRR_fMRI_faceMatching_PA 2" "CMRR_fMRI_conflict_AP 2" "CMRR_fMRI_conflict_PA 2" "CMRR_fMRI_conflict_AP 4" "CMRR_fMRI_conflict_PA 4"  "ABCD_T1w_MPR_vNav" "T1w_MPR_CMRR"   "ABCD_dMRI_DistortionMap_PA" "ABCD_dMRI_DistortionMap_AP" "ABCD_dMRI" "ABCD_dMRI 2" "dMRI_dir99_AP_CMRR 2" "dMRI_dir99_PA_CMRR 2" "dMRI_dir98_AP_CMRR 2" "dMRI_dir98_PA_CMRR 2" "rfMRI_REST_AP_CMRR  4" "rfMRI_REST_PA_CMRR  2" "rfMRI_REST_AP_CMRR  6" "rfMRI_REST_PA_CMRR  4" "ABCD_fMRI_DistortionMap_PA 2" "ABCD_fMRI_DistortionMap_AP 2"  "ABCD_fMRI_DistortionMap_PA_shortTE 2" "ABCD_fMRI_DistortionMap_AP_shortTE 2"  "ABCD_fMRI_DistortionMap_PA_shortTE_asc 2" "ABCD_fMRI_DistortionMap_AP_shortTE_asc 2"  "ABCD_fMRI_rest 2" "ABCD_fMRI_rest 3" "ABCD_fMRI_rest 3" "ABCD_fMRI_rest 4" "ABCD_fMRI_rest 5" "ABCD_fMRI_gambling" "ABCD_fMRI_gambling 2" "ABCD_fMRI_faceMatching" "ABCD_fMRI_faceMatching 2" "ABCD_fMRI_conflict 2" "ABCD_fMRI_conflict 3" "ABCD_fMRI_conflict 4" "ABCD_fMRI_conflict 5"   "ABCD_T2w_SPC_vNav 3" "T2w_SPC_CMRR"  "tfMRI_conflict_AP_CMRR 2" "tfMRI_conflict_AP_CMRR 4" "tfMRI_conflict_PA_CMRR 2" "tfMRI_conflict_PA_CMRR 4" "tfMRI_gambling_AP_CMRR 2" "tfMRI_gambling_PA_CMRR 2" "tfMRI_faceMatching_AP_CMRR 2" "tfMRI_faceMatching_PA_CMRR 2" ) 

niftyNames=( "fMRI_SpinEchoFieldMap_AP" "fMRI_SpinEchoFieldMap_PA" "fMRI_rest1_AP" "fMRI_rest2_PA" "tfMRI_faceMatching_1_AP" "tfMRI_faceMatching2_PA" "tfMRI_conflict1_AP" "tfMRI_conflict2_PA" "tfMRI_conflict3_AP" "tfMRI_conflict4_PA"  "T1" "T1" "dMRI_DistortionMap_PA" "dMRI_DistortionMap_AP" "dMRI1" "dMRI2" "dMRI_AP1" "dMRI_PA1" "dMRI_AP2" "dMRI_PA2" "fMRI_rest_AP1" "fMRI_rest_PA1" "fMRI_rest_AP2" "fMRI_rest_PA2" "fMRI_DistortionMap_PA" "fMRI_DistortionMap_AP"  "fMRI_DistortionMap_PA_shortTE" "fMRI_DistortionMap_AP_shortTE"  "fMRI_DistortionMap_PA_shortTE_asc" "fMRI_DistortionMap_AP_shortTE_asc" "fMRI_rest1" "fMRI_rest2" "fMRI_rest3" "fMRI_rest4" "fMRI_rest5" "tfMRI_gambling1" "tfMRI_gambling2" "tfMRI_faceMatching1" "tfMRI_faceMatching2" "tfMRI_conflict1" "tfMRI_conflict2" "tfMRI_conflict3" "tfMRI_conflict4" "T2" "T2" "tfMRI_conflict_AP1" "tfMRI_conflict_AP2" "tfMRI_conflict_PA1" "tfMRI_conflict_PA2" "tfMRI_gambling_AP" "tfMRI_gambling_PA" "tfMRI_faceMatching_AP" "tfMRI_faceMatching_PA" )

echo ${#scanNames[@]}
echo $s
for s in ${subjects[@]};
do
	#unpacksdcmdir -src /space/erebus/1/users/data/dicoms/$s/ -targ /space/erebus/1/users/data/dicoms/$s/ -scanonly scan.txt
	fout=${folder}/preprocess/$s

	mkdir -p ${fout}/ABCD/
	mkdir -p ${fout}/iPAT2/
	mkdir -p ${fout}/CMRR/

#	rm ${fout}/ABCD/*
#	rm ${fout}/iPAT2/*
#	rm ${fout}/CMRR/*
	for i in `seq 0 ${#scanNames[@]}`;
        do
		echo $i
		scan=${scanNames[$i]}
		if [ -z "${scanNames[$i]##*iPAT2*}" ]; then
			output=${fout}/iPAT2
		elif [ -z "${scanNames[$i]##*ABCD*}" ]; then
			output=${fout}/ABCD
		elif [ -z "${scanNames[$i]##*CMRR*}" ]; then
			output=${fout}/CMRR
		else
			output=${fout}/weirdddd
		fi
		
		echo python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scanNames[$i]} ${niftyNames[$i]}
		scan=(`python /space/erebus/1/users/data/code/scripts/readScanFile.py /space/erebus/1/users/data/dicoms/$s/scan.txt ${scanNames[$i]}`)
		scan=${scan[7]}
		echo ${scan}
		#mri_convert ${folder}/$s/${scan} ${output}/${niftyNames[$i]}.nii.gz &
		pbsubmit -n 1   -m rjj7 -c "mri_convert ${folder}/$s/${scan} ${output}/${niftyNames[$i]}.nii.gz"
	done
	chgrp -R fiber  ${folder}/preprocess/${s}
	chmod -R 770  ${folder}/preprocess/${s}

	chgrp -R fiber  ${folder}/${s}
	chmod -R 770  ${folder}/${s}
done


}
function motion()
{
	for s in ${subjects[@]};
	do
		pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh motion_measures  $s"
		#pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh everything2T1Motion $s"
		#bash ${scriptFolder}/motion.sh ltaDiff $s
	done
}
function snr()
{
	for s in ${subjects[@]};
	do
		#pbsubmit -n 1 -c "bash ${scriptFolder}/motion.sh pre_compute $s"
		#pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh GetB0s $s"
		pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh T1aparc2all $s"

		#pbsubmit -n 1  -c "bash ${scriptFolder}/motion.sh everything2T1SNR $s"
		
	done
}
	
function copyToHui()
{
	for s in ${subjects[@]};
	do
		mkdir -p /cluster/octdata/users/Hui/short_tracts/${s}
		cp /space/erebus/1/users/data/preprocess/${s}/dsi_studio/wm2009parc2fa_LPS.nii.gz /cluster/octdata/users/Hui/short_tracts/${s}/
		cp /space/erebus/1/users/data/preprocess/${s}/dsi_studio/fa.nii.gz /cluster/octdata/users/Hui/short_tracts/${s}/
		cp /space/erebus/1/users/data/preprocess/${s}/dsi_studio/md.nii.gz /cluster/octdata/users/Hui/short_tracts/${s}/
		cp /space/erebus/1/users/data/preprocess/${s}/dsi_studio/rd.nii.gz /cluster/octdata/users/Hui/short_tracts/${s}/
		cp /space/erebus/1/users/data/preprocess/${s}/dsi_studio/ad.nii.gz /cluster/octdata/users/Hui/short_tracts/${s}/
		cp /autofs/space/erebus_001/users/data/preprocess/${s}/dsi_studio/streamlines_long55.trk /cluster/octdata/users/Hui/short_tracts/${s}/
	done
}
<<permissions
chgrp -R fiber  ${folder}/preprocess/${s}
chmod -R 770  ${folder}/preprocess/${s}

chgrp -R fiber  ${folder}/${s}
chmod -R 770  ${folder}/${s}

chgrp -R fiber  ${folder}/tfMRI_output
chmod -R 770  ${folder}/tfMRI_output

chgrp -R fiber  ${folder}/BIDS
chmod -R 770  ${folder}/BIDS
permissions


$@
