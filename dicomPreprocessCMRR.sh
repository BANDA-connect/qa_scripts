#!/bin/bash
folder=/space/erebus/1/users/data
scriptFolder=/space/erebus/1/users/data/scripts
#scanNames=( "ABCD_T1w_MPR" "T1w_MPR_CMRR"   "ABCD_dMRI_DistortionMap_PA" "ABCD_dMRI_DistortionMap_AP" "ABCD_dMRI"  "ABCD_dMRI_DistortionMap_PA_iPAT2" "ABCD_dMRI_DistortionMap_AP_iPAT2" "ABCD_dMRI_iPAT2" "dMRI_dir99_AP_CMRR 2" "dMRI_dir99_PA_CMRR 2" "dMRI_dir98_AP_CMRR 2" "dMRI_dir98_PA_CMRR 2" "rfMRI_REST_AP_CMRR  4" "rfMRI_REST_PA_CMRR  2" "rfMRI_REST_AP_CMRR  6" "rfMRI_REST_PA_CMRR  4" "ABCD_fMRI_rest_DistortionMap_PA" "ABCD_fMRI_rest_DistortionMap_AP" "ABCD_fMRI_rest" "ABCD_fMRI_rest 2" " ABCD_fMRI_rest_DistortionMap_PA_iPAT2" "ABCD_fMRI_rest_DistortionMap_AP_iPAT2" "ABCD_fMRI_rest_iPAT2" "ABCD_fMRI_rest_iPAT2 2" "ABCD_T2w_SPC" "T2w_SPC_CMRR" "tfMRI_conflict_AP_CMRR 2" "tfMRI_conflict_AP_CMRR 4" "tfMRI_conflict_PA_CMRR 2" "tfMRI_conflict_PA_CMRR 4" "tfMRI_gambling_AP_CMRR 2" "tfMRI_gambling_PA_CMRR 2" "tfMRI_faceMatching_AP_CMRR 2" "tfMRI_faceMatching_PA_CMRR 2" ) 

#new ABCD
scanNames=( "CMRR_SpinEchoFieldMap_AP" "CMRR_SpinEchoFieldMap_PA" "CMRR_fMRI_rest_AP 2" "CMRR_fMRI_rest_PA 2" "CMRR_fMRI_faceMatching_AP 2" "CMRR_fMRI_faceMatching_PA 2" "CMRR_fMRI_conflict_AP 2" "CMRR_fMRI_conflict_PA 2" "CMRR_fMRI_conflict_AP 4" "CMRR_fMRI_conflict_PA 4"  "ABCD_T1w_MPR_vNav" "T1w_MPR_CMRR"   "ABCD_dMRI_DistortionMap_PA" "ABCD_dMRI_DistortionMap_AP" "ABCD_dMRI" "ABCD_dMRI 2" "dMRI_dir99_AP_CMRR 2" "dMRI_dir99_PA_CMRR 2" "dMRI_dir98_AP_CMRR 2" "dMRI_dir98_PA_CMRR 2" "rfMRI_REST_AP_CMRR  4" "rfMRI_REST_PA_CMRR  2" "rfMRI_REST_AP_CMRR  6" "rfMRI_REST_PA_CMRR  4" "ABCD_fMRI_DistortionMap_PA 2" "ABCD_fMRI_DistortionMap_AP 2"  "ABCD_fMRI_DistortionMap_PA_shortTE 2" "ABCD_fMRI_DistortionMap_AP_shortTE 2"  "ABCD_fMRI_DistortionMap_PA_shortTE_asc 2" "ABCD_fMRI_DistortionMap_AP_shortTE_asc 2"  "ABCD_fMRI_rest 2" "ABCD_fMRI_rest 3" "ABCD_fMRI_rest 3" "ABCD_fMRI_rest 4" "ABCD_fMRI_rest 5" "ABCD_fMRI_gambling" "ABCD_fMRI_gambling 2" "ABCD_fMRI_faceMatching" "ABCD_fMRI_faceMatching 2" "ABCD_fMRI_conflict 2" "ABCD_fMRI_conflict 3" "ABCD_fMRI_conflict 4" "ABCD_fMRI_conflict 5"   "ABCD_T2w_SPC_vNav 3" "T2w_SPC_CMRR"  "tfMRI_conflict_AP_CMRR 2" "tfMRI_conflict_AP_CMRR 4" "tfMRI_conflict_PA_CMRR 2" "tfMRI_conflict_PA_CMRR 4" "tfMRI_gambling_AP_CMRR 2" "tfMRI_gambling_PA_CMRR 2" "tfMRI_faceMatching_AP_CMRR 2" "tfMRI_faceMatching_PA_CMRR 2" ) 


niftyNames=( "fMRI_SpinEchoFieldMap_AP" "fMRI_SpinEchoFieldMap_PA" "fMRI_rest1_AP" "fMRI_rest2_PA" "tfMRI_faceMatching_1_AP" "tfMRI_faceMatching2_PA" "tfMRI_conflict1_AP" "tfMRI_conflict2_PA" "tfMRI_conflict3_AP" "tfMRI_conflict4_PA"  "T1" "T1" "dMRI_DistortionMap_PA" "dMRI_DistortionMap_AP" "dMRI1" "dMRI2" "dMRI_AP1" "dMRI_PA1" "dMRI_AP2" "dMRI_PA2" "fMRI_rest_AP1" "fMRI_rest_PA1" "fMRI_rest_AP2" "fMRI_rest_PA2" "fMRI_DistortionMap_PA" "fMRI_DistortionMap_AP"  "fMRI_DistortionMap_PA_shortTE" "fMRI_DistortionMap_AP_shortTE"  "fMRI_DistortionMap_PA_shortTE_asc" "fMRI_DistortionMap_AP_shortTE_asc" "fMRI_rest1" "fMRI_rest2" "fMRI_rest3" "fMRI_rest4" "fMRI_rest5" "tfMRI_gambling1" "tfMRI_gambling2" "tfMRI_faceMatching1" "tfMRI_faceMatching2" "tfMRI_conflict1" "tfMRI_conflict2" "tfMRI_conflict3" "tfMRI_conflict4" "T2" "T2" "tfMRI_conflict_AP1" "tfMRI_conflict_AP2" "tfMRI_conflict_PA1" "tfMRI_conflict_PA2" "tfMRI_gambling_AP" "tfMRI_gambling_PA" "tfMRI_faceMatching_AP" "tfMRI_faceMatching_PA" )


#scanNames=( "ABCD_fMRI_DistortionMap_PA 2"  "ABCD_fMRI_DistortionMap_AP 2" "ABCD_fMRI_gambling" "ABCD_fMRI_gambling 2"  "ABCD_fMRI_faceMatching" "ABCD_fMRI_faceMatching 2" "ABCD_fMRI_DistortionMap_PA_iPAT2 "  "ABCD_fMRI_DistortionMap_AP_iPAT2" "ABCD_fMRI_gambling_iPAT2" "ABCD_fMRI_gambling_iPAT2 2"  "ABCD_fMRI_faceMatching_iPAT2" "ABCD_fMRI_faceMatching_iPAT2 2" "CMRR_tfMRI_faceMatching_AP 2"  "CMRR_tfMRI_faceMatching_PA 2" "CMRR_tfMRI_gambling_AP 2" "CMRR_tfMRI_gambling_PA 2" ) 
#niftyNames=( "fMRI_DistortionMap_PA" "fMRI_DistortionMap_AP" "tfMRI_gambling1" "tfMRI_gambling2" "tfMRI_faceMatching1" "tfMRI_faceMatching2" "fMRI_DistortionMap_PA" "fMRI_DistortionMap_AP" "tfMRI_gambling1" "tfMRI_gambling2" "tfMRI_faceMatching1" "tfMRI_faceMatching2" "tfMRI_faceMatching_AP" "tfMRI_faceMatching_PA" "tfMRI_gambling_AP" "tfMRI_gambling_PA"  )

subjects=( PANDA028 ) #PANDA027 PANDA025b ) #PANDA025 ) #PANDA004b PANDA026 ) #4 ) #PANDA002d )  #PANDA022 PANDA023 PANDA021 PANDA011 PANDA013 PANDA014 PANDA016 PANDA017 PANDA018 PANDA019 PANDA020) #PANDA011 ) #PANDA017) #PANDA013)
echo ${#scanNames[@]}
#s=PANDA013
#s=$1
echo $s
for s in ${subjects[@]};
do
	#unpacksdcmdir -src /space/erebus/1/users/data/$s/ -targ /space/erebus/1/users/data/$s/ -scanonly scan.txt
	fout=${folder}/preprocess/$s

	mkdir -p ${fout}/ABCD/
	mkdir -p ${fout}/iPAT2/
	mkdir -p ${fout}/CMRR/
:<<hola2
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
		
		echo python /space/erebus/1/users/data/scripts/readScanFile.py /space/erebus/1/users/data/$s/scan.txt ${scanNames[$i]} ${niftyNames[$i]}
		scan=(`python /space/erebus/1/users/data/scripts/readScanFile.py /space/erebus/1/users/data/$s/scan.txt ${scanNames[$i]}`)
		scan=${scan[7]}
		echo ${scan}
		#mri_convert ${folder}/$s/${scan} ${output}/${niftyNames[$i]}.nii.gz &
		pbsubmit -n 1   -m vsiless -c "mri_convert ${folder}/$s/${scan} ${output}/${niftyNames[$i]}.nii.gz"
	done


	

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_gambling1.nii.gz no_bvec no_bval tfMRI_gambling1"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_gambling2.nii.gz no_bvec no_bval tfMRI_gambling2"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching1.nii.gz no_bvec no_bval tfMRI_faceMatching1"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching2.nii.gz no_bvec no_bval tfMRI_faceMatching2"

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict1.nii.gz no_bvec no_bval tfMRI_conflict1"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict2.nii.gz no_bvec no_bval tfMRI_conflict2"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict3.nii.gz no_bvec no_bval tfMRI_conflict3"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict4.nii.gz no_bvec no_bval tfMRI_conflict4"

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest1.nii.gz no_bvec no_bval fMRI_rest1"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest2.nii.gz no_bvec no_bval fMRI_rest2"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest3.nii.gz no_bvec no_bval fMRI_rest3"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest4.nii.gz no_bvec no_bval fMRI_rest4"
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest5.nii.gz no_bvec no_bval fMRI_rest5"




	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s fMRI_rest1_AP.nii.gz fMRI_rest2_PA.nii.gz hola que tal fMRI_rest1"
	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_faceMatching1_AP.nii.gz tfMRI_faceMatching2_PA.nii.gz hola que tal tfMRI_faceMatching"
	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_conflict1_AP.nii.gz tfMRI_conflict2_PA.nii.gz hola que tal tfMRI_conflict1"
	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_conflict3_AP.nii.gz tfMRI_conflict4_PA.nii.gz hola que tal tfMRI_conflict2"

	#lastest
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

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_DistortionMap_AP.nii.gz "
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_DistortionMap_PA.nii.gz "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching1.nii.gz "
 	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching2.nii.gz "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict1.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict2.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict3.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_conflict4.nii.gz "

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest1.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest2.nii.gz "
	output=${fout}/ABCD/
	cp  ${output}/fMRI_rest1.nii.gz ${output}/fMRI_rest1_shortTE.nii.gz
	cp  ${output}/fMRI_rest2.nii.gz ${output}/fMRI_rest2_shortTE.nii.gz
	cp  ${output}/fMRI_rest1.nii.gz ${output}/fMRI_rest1_shortTE_asc.nii.gz
	cp  ${output}/fMRI_rest2.nii.gz ${output}/fMRI_rest2_shortTE_asc.nii.gz

	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA_shortTE.nii.gz fMRI_DistortionMap_AP_shortTE.nii.gz fMRI_rest1_shortTE.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA_shortTE.nii.gz fMRI_DistortionMap_AP_shortTE.nii.gz fMRI_rest2_shortTE.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA_shortTE_asc.nii.gz fMRI_DistortionMap_AP_shortTE_asc.nii.gz fMRI_rest1_shortTE_asc.nii.gz "
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_ABCD_iPAT2 ABCD fMRI $s fMRI_DistortionMap_PA_shortTE_asc.nii.gz fMRI_DistortionMap_AP_shortTE_asc.nii.gz fMRI_rest2_shortTE_asc.nii.gz "
hola2
	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion_v2.sh distortion_CMRR_2 fMRI $s tfMRI_faceMatching1_AP.nii.gz fMRI_SpinEchoFieldMap_PA.nii.gz fMRI_SpinEchoFieldMap_AP.nii.gz AP "
<<hola4


hola4
#	mv ${fout}/CMRR//dMRI_AP1.voxel_space.bvecs ${fout}/CMRR//dMRI_AP1.bvecs
#	mv ${fout}/CMRR//dMRI_AP2.voxel_space.bvecs ${fout}/CMRR/dMRI_AP2.bvecs
#	mv ${fout}/CMRR//dMRI_PA1.voxel_space.bvecs ${fout}/CMRR//dMRI_PA1.bvecs
#	mv ${fout}/CMRR//dMRI_PA2.voxel_space.bvecs ${fout}/CMRR/dMRI_PA2.bvecs

#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR dMRI $s dMRI_PA1.nii.gz dMRI_AP1.nii.gz dMRI_AP1.nii.gz  dMRI_AP1.bvecs dMRI_AP1.bvals dMRI1"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR dMRI $s dMRI_PA2.nii.gz dMRI_AP2.nii.gz dMRI_AP2.nii.gz  dMRI_AP2.bvecs dMRI_AP2.bvals dMRI2"

#	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_conflict_PA1.nii.gz tfMRI_conflict_AP1.nii.gz hola que tal tfMRI_conflict1"
#	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_conflict_PA2.nii.gz tfMRI_conflict_AP2.nii.gz hola que tal tfMRI_conflict2"

#	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_gambling_PA.nii.gz tfMRI_gambling_AP.nii.gz hola que tal tfMRI_gambling"

#	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s tfMRI_faceMatching_PA.nii.gz tfMRI_faceMatching_AP.nii.gz hola que tal tfMRI_faceMatching"


:<<COMMENT


#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 tfMRI_gambling1 $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_gambling1.nii.gz"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 tfMRI_gambling2 $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_gambling2.nii.gz"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 tfMRI_faceMatching1 $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching1.nii.gz"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 tfMRI_faceMatching2 $s fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz tfMRI_faceMatching2.nii.gz"

#	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR tfMRI_gambling $s tfMRI_gambling_PA.nii.gz tfMRI_gambling_AP.nii.gz tfMRI_gambling.nii.gz"
#	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR tfMRI_faceMatching $s tfMRI_faceMatching_PA.nii.gz tfMRI_faceMatching_AP.nii.gz tfMRI_faceMatching.nii.gz"


	mv ${fout}/ABCD/dMRI.voxel_space.bvecs ${fout}/ABCD/dMRI.bvecs
	mv ${fout}/iPAT2/dMRI.voxel_space.bvecs ${fout}/iPAT2/dMRI.bvecs
	mv ${fout}/CMRR/dMRI_AP.voxel_space.bvecs ${fout}/CMRR/dMRI_AP.bvecs
	mv ${fout}/CMRR/dMRI_PA.voxel_space.bvecs ${fout}/CMRR/dMRI_PA.bvecs


#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD dMRI $s dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.bvecs dMRI.bvals"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI_rest1 $s fMRI_DistortionMap_PA_rest.nii.gz fMRI_DistortionMap_AP_rest.nii.gz fMRI_rest1.nii.gz"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD fMRI_rest2 $s fMRI_DistortionMap_PA_rest.nii.gz fMRI_DistortionMap_AP_rest.nii.gz fMRI_rest2.nii.gz"

#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 dMRI $s dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.bvecs dMRI.bvals"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 fMRI_rest1 $s fMRI_DistortionMap_PA_rest.nii.gz fMRI_DistortionMap_AP_rest.nii.gz fMRI_rest1.nii.gz"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 fMRI_rest2 $s fMRI_DistortionMap_PA_rest.nii.gz fMRI_DistortionMap_AP_rest.nii.gz fMRI_rest2.nii.gz"

	pbsubmit -n 2  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR fMRI $s fMRI_rest_PA.nii.gz fMRI_rest_AP.nii.gz fMRI_rest1.nii.gz"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh CMRR dMRI $s dMRI_PA.nii.gz dMRI_AP.nii.gz dMRI_AP.nii.gz  dMRI_AP.bvecs dMRI_AP.bvals"

#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh ABCD dMRI $s dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.bvecs dMRI.bvals"
#	pbsubmit -n 1  -m vsiless -c "bash ${scriptFolder}/distortion.sh iPAT2 dMRI $s dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.bvecs dMRI.bvals"



chgrp -R fiber  ${folder}/preprocess/${s}
chmod -R 770  ${folder}/preprocess/${s}

chgrp -R fiber  ${folder}/${s}
chmod -R 770  ${folder}/${s}

chgrp -R fiber  ${folder}/tfMRI_output
chmod -R 770  ${folder}/tfMRI_output

chgrp -R fiber  ${folder}/BIDS
chmod -R 770  ${folder}/BIDS

COMMENT
done


