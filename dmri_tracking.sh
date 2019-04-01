dsistudio=/autofs/cluster/pubsw/2/pubsw/Linux2-2.3-x86_64/packages/DSI-Studio/1.0/bin/
folder=/space/erebus/1/users/data/preprocess/

subjects=(  PANDA021 PANDA018 PANDA019 PANDA011 PANDA013 PANDA014 PANDA016 PANDA017 PANDA018 PANDA019 PANDA013 PANDA020) #PANDA011 ) #PANDA017) #) PANDA013 ) #
studies=(  CMRR ABCD iPAT2 )
function oldTractography()
{
	for s in ${subjects[@]};
	do
	echo $s
	for study in ${studies[@]};
	do

	echo  $study

	output=${folder}/${s}/${study}/dsi_studio
	mkdir 	${output}
	:<<COMMENT

	if [ "${study}" = "CMRR"  ]; then
		echo "CMRR"
		cp ${folder}/${s}/${study}/double.bvals ${folder}/${s}/${study}/bvals
		cp ${folder}/${s}/${study}/double.bvecs ${folder}/${s}/${study}/bvecs

	#	python  /local_mount/space/namic/2/users/vsiless/scripts/flip_bvec.py ${folder}/${s}/${study}/bvecs ${folder}/${s}/${study}/bvecs_fy
	#	mv ${folder}/${s}/${study}/bvecs_fy ${folder}/${s}/${study}/bvecs
	else 
		cp ${folder}/${s}/${study}/dMRI.bvals ${folder}/${s}/${study}/bvals
		cp ${folder}/${s}/${study}/dMRI.bvecs ${folder}/${s}/${study}/bvecs
	fi
	#do this for bot ABCD and CMRR
	${dsistudio}/dsi_studio --action=src --source=${folder}/${s}/${study}/dMRI_topup_eddy.nii.gz  --output=${output}/dwi.src.nii.gz

		${dsistudio}/dsi_studio --action=rec --thread=8 --source=${output}/dwi.src.nii.gz --method=4 --param0=0.5 --odf_order=4 --num_fiber=3 --deconvolution=5 #--output=${output}/fib.gz # --r2_weighted=1  #--
		${dsistudio}/dsi_studio --action=exp  --source=${output}/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz --export=fa0,gfa 
		${dsistudio}/dsi_studio --action=trk --source=${output}/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz --method=0 --fiber_count=500000 --ref=${folder}/${s}/${study}/dMRI_AP_PA_topup.nii.gz --output=${output}/whole_brain_5k.trk

		track_info ${output}/whole_brain_5k.trk -vorder LPS LAS
	#for CMRR also only PA to compare same number of directions with ABCD
	if [ "${study}" = "CMRR"  ]; then
		echo "CMRR"
		cp ${folder}/${s}/${study}/dMRI_PA.bvals ${folder}/${s}/${study}/bvals
		cp ${folder}/${s}/${study}/dMRI_PA.bvecs ${folder}/${s}/${study}/bvecs

		${dsistudio}/dsi_studio --action=src --source=${folder}/${s}/${study}/dMRI_topup_eddy_PA.nii.gz  --output=${output}/dwi.src.PA.nii.gz

		${dsistudio}/dsi_studio --action=rec --thread=8 --source=${output}/dwi.src.PA.nii.gz --method=4 --param0=0.5 --odf_order=4 --num_fiber=3 --deconvolution=5 #--output=${output}/fib.gz # --r2_weighted=1  #--
		${dsistudio}/dsi_studio --action=exp  --source=${output}/dwi.src.PA.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz --export=fa0,gfa 
		${dsistudio}/dsi_studio --action=trk --source=${output}/dwi.src.PA.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz --method=0 --fiber_count=500000  --ref=${folder}/${s}/${study}/dMRI_AP_PA_topup.nii.gz --output=${output}/whole_brain_PA_5k.trk

		track_info ${output}/whole_brain_PA_5k.trk -vorder LPS LAS
	
	fi
	COMMENT
	#hola
		if [ "${study}" = "iPAT2"  ]; then
			input=/space/erebus/1/users/data/preprocess/FS/ABCD/$s/mri/
		else
			input=/space/erebus/1/users/data/preprocess/FS/$study/$s/mri/
		fi

	
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





	# python /local_mount/space/namic/2/users/vsiless/scripts/hcp_changeHeader.py ${folder}/${s}/${study}/dMRI_topup_eddy_PA.nii.gz ${output}/dMRI_topup_eddy_noheader.nii.gz

	#
	#mri_convert --in_orientation LAS --out_orientation PIL ${folder}/${s}/${study}/T1.nii.gz ${folder}/${s}/${study}/T1_LPS.nii.gz
	#python /local_mount/space/namic/2/users/vsiless/scripts/hcp_changeHeader.py  ${folder}/${s}/${study}/T1_LPS.nii.gz ${folder}/${s}/${study}/T1_LPS_noheader.nii.gz
	

	# python /local_mount/space/namic/2/users/vsiless/code/commons/tractconverter-master/scripts/TractConverter.py -i /local_mount/space/namic/2/users/vsiless/data/connectome-mgh/mgh_1001/whole_brain.trk -o /local_mount/space/namic/2/users/vsiless/data/connectome-mgh/mgh_1001/whole_brain.vtk -f

	done
	done
}
