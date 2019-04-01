
dsistudio=/autofs/cluster/pubsw/2/pubsw/Linux2-2.3-x86_64/packages/DSI-Studio/1.0/bin/
folder=/space/erebus/1/users/data/preprocess/

target=PANDA011
call()
{
	echo "hello"
	subjects=(PANDA011 PANDA013 PANDA014 PANDA016 PANDA017 PANDA020 PANDA021 PANDA018 PANDA019) #PANDA011 ) #PANDA017) #PANDA013) PANDA013 ) #
	studies=( ABCD CMRR iPAT2 ) # ABCD )  #iPAT2 )
	for study in ${studies[@]};
	do

	echo  $study

	for s in ${subjects[@]};
	do	
	echo $s
		#output=${folder}/${s}/${study}/dsi_studio
		pbsubmit -n 1 -m vsiless -c "bash /space/erebus/1/users/data/code/scripts/fornix_atlas.sh register_fsl $s ${study}"
		echo "pbsubmit -n 1 -m vsiless -c bash /space/erebus/1/users/data/code/scripts/fornix_atlas.sh register_fsl $s ${study}"
		#bash /space/erebus/1/users/data/code/scripts/fornix_atlas.sh register_fsl $s ${study}
	done
	done 
}
call_average()
{
	studies=( ABCD CMRR iPAT2 ) # ABCD )  #iPAT2 )
	for study in ${studies[@]};
	do
		pbsubmit -n 1 -m vsiless -c "bash /space/erebus/1/users/data/code/scripts/fornix_atlas.sh average_fsl ${study}"
		
	done
}
:<<COMMENT

cd /space/erebus/1/users/data/preprocess/$s/${study}

mri_convert -f 0 dMRI_topup_eddy.nii.gz lowb_topup_eddy.nii.gz

bet lowb_topup_eddy.nii.gz lowb_topup_eddy_brain.nii.gz -m -f 0.2
if [ "${study}" = "CMRR"  ]; then

	dtifit -k dMRI_topup_eddy.nii.gz -m lowb_topup_eddy_brain_mask.nii.gz -r double.bvecs -b double.bvals -o dMRI_topup_eddy

else
	dtifit -k dMRI_topup_eddy.nii.gz -m lowb_topup_eddy_brain_mask.nii.gz -r bvecs -b bvals -o dMRI_topup_eddy
fi
mri_convert --in_orientation LAS --out_orientation LPS dMRI_topup_eddy_FA.nii.gz dMRI_topup_eddy_FA_LPS.nii.gz

fsl_reg dMRI_topup_eddy_FA_LPS.nii.gz $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz fa2fmrib -e -FA

applywarp -i dMRI_topup_eddy_FA_LPS.nii.gz -o dMRI_topup_eddy_FA_LPS_to_FMRIB58_FA_1mm.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w fa2fmrib_warp

applywarp -i dsi_studio/fornix.nii -o dsi_studio/fornix_to_FMRIB58_FA_1mm.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w fa2fmrib_warp

if [ "${study}" = "CMRR"  ]; then
	applywarp -i dsi_studio/fornix_PA.nii -o dsi_studio/fornix_PA_to_FMRIB58_FA_1mm.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w fa2fmrib_warp
fi



done


#mri_average /space/erebus/1/users/data/preprocess/${target}/${study}/dsi_studio/fornix.nii /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fornix2_${target}.nii.gz /space/erebus/1/users/data/preprocess/average_fornix_${study}.nii.gz

#mri_average /space/erebus/1/users/data/preprocess/${target}/${study}/dsi_studio/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fa2_${target}.nii.gz /space/erebus/1/users/data/preprocess/average_fa_${study}.nii.gz

mri_average /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fornix_to_FMRIB58_FA_1mm.nii.gz /space/erebus/1/users/data/preprocess/fornix_${study}_to_FMRIB58_FA_1mm.nii.gz

if [ "${study}" = "CMRR"  ]; then
#	mri_average /space/erebus/1/users/data/preprocess/${target}/${study}/dsi_studio/fornix_PA.nii /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fornix_PA2_${target}.nii.gz /space/erebus/1/users/data/preprocess/average_fornix_${study}_PA.nii.gz
	mri_average /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fornix_PA_to_FMRIB58_FA_1mm.nii.gz /space/erebus/1/users/data/preprocess/fornix_PA_${study}_to_FMRIB58_FA_1mm.nii.gz
fi

done
COMMENT
average_fsl()
{
study=$1
mri_average /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fornix_to_FMRIB58_FA_1mm.nii.gz /space/erebus/1/users/data/preprocess/fornix_${study}_to_FMRIB58_FA_1mm.nii.gz

if [ "${study}" = "CMRR"  ]; then
	mri_average /space/erebus/1/users/data/preprocess/*/${study}/dsi_studio/fornix_PA_to_FMRIB58_FA_1mm.nii.gz /space/erebus/1/users/data/preprocess/fornix_PA_${study}_to_FMRIB58_FA_1mm.nii.gz
fi

}
register_fsl() 
{
	s=$1 
	study=$2

	cd /space/erebus/1/users/data/preprocess/$s/${study}

	mri_convert -f 0 dMRI_topup_eddy.nii.gz lowb_topup_eddy.nii.gz

	bet lowb_topup_eddy.nii.gz lowb_topup_eddy_brain.nii.gz -m -f 0.2
	if [ "${study}" = "CMRR"  ]; then

		dtifit -k dMRI_topup_eddy.nii.gz -m lowb_topup_eddy_brain_mask.nii.gz -r double.bvecs -b double.bvals -o dMRI_topup_eddy

	else
		dtifit -k dMRI_topup_eddy.nii.gz -m lowb_topup_eddy_brain_mask.nii.gz -r bvecs -b bvals -o dMRI_topup_eddy
	fi
	mri_convert --in_orientation LAS --out_orientation LPS dMRI_topup_eddy_FA.nii.gz dMRI_topup_eddy_FA_LPS.nii.gz

	fsl_reg dMRI_topup_eddy_FA_LPS.nii.gz $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz fa2fmrib -e -FA

	applywarp -i dMRI_topup_eddy_FA_LPS.nii.gz -o dMRI_topup_eddy_FA_LPS_to_FMRIB58_FA_1mm.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w fa2fmrib_warp

	applywarp -i dsi_studio/fornix.nii -o dsi_studio/fornix_to_FMRIB58_FA_1mm.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w fa2fmrib_warp

	if [ "${study}" = "CMRR"  ]; then
		applywarp -i dsi_studio/fornix_PA.nii -o dsi_studio/fornix_PA_to_FMRIB58_FA_1mm.nii.gz -r $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz -w fa2fmrib_warp
	fi

}

register_medINRIA()
{
	echo "jh"
	#/local_mount/space/namic/2/users/vsiless/programs/MedINRIA -gui 0 -mod imagefusion -f /space/erebus/1/users/data/preprocess/${target}/${study}/dsi_studio/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -m /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -o /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fa2_${target}.nii.gz -r diffeomorphic -od /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fa2_${target}_def.nii.gz

	#/local_mount/space/namic/2/users/vsiless/programs/MedINRIA -gui 0 -mod imagefusion -f /space/erebus/1/users/data/preprocess/${target}/${study}/dsi_studio/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -m /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fornix.nii -o /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fornix2_${target}.nii.gz -d /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fa2_${target}_def.nii.gz

	#if [ "${study}" = "CMRR"  ]; then
	#/local_mount/space/namic/2/users/vsiless/programs/MedINRIA -gui 0 -mod imagefusion -f /space/erebus/1/users/data/preprocess/${target}/${study}/dsi_studio/dwi.src.nii.gz.odf4.f3.de7.gqi.0.5.fib.gz.fa0.nii.gz -m /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fornix_PA.nii -o /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fornix_PA2_${target}.nii.gz -d /space/erebus/1/users/data/preprocess/$s/${study}/dsi_studio/fa2_${target}_def.nii.gz
	#fi

}
$@

