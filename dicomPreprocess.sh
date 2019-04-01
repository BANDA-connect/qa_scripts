
folder=/space/erebus/1/users/data
subjects=(PANDA003)

#for s in ${subjects[@]};
#do
#	mri_convert --in_type dicom --out_type nii ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016031820115086037455283 /space/erebus/1/users/data/preprocess/PANDA002/ABCD_dMRI_BW1700_4.nii.gz
#done



<<COMMENT
s=PANDA003
chgrp -R fiber  ${folder}/$s/
chmod -R 770  ${folder}/$s/
mkdir  ${folder}/preprocess/$s

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040113024619464563249  ${folder}/preprocess/$s/ABCD_T1w_MPR_vNav.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040113474215992365130  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PH_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040114062782821908680  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PH_PA_PAT2.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040113513532368466452  ${folder}/preprocess/$s/ABCD_dMRI_pedi_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040114075946636310001  ${folder}/preprocess/$s/ABCD_dMRI_pedi_AP2.nii.gz

chgrp -R fiber  ${folder}/preprocess/$s/
chmod -R 770  ${folder}/preprocess/$s/



s=PANDA004

chgrp -R fiber  ${folder}/$s/
chmod -R 770  ${folder}/$s/
mkdir  ${folder}/preprocess/$s

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040716503460837440797  ${folder}/preprocess/$s/ABCD_T1w_MPR_vNav.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040716543165084941739  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040716562251301641959  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040717002718955542288 ${folder}/preprocess/$s/ABCD_fMRI_rest.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.201604071729289119418637  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040717310071246819494  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.20160407173256914120791  ${folder}/preprocess/$s/ABCD_dMRI_pedi.nii.gz


s=PANDA005

chgrp -R fiber  ${folder}/$s/
chmod -R 770  ${folder}/$s/
mkdir  ${folder}/preprocess/$s

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040816380942644456060  ${folder}/preprocess/$s/ABCD_T1w_MPR_vNav.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.201604081639502607457019  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040816425358547257455  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040816445818840958000 ${folder}/preprocess/$s/ABCD_fMRI_rest.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040817080495141743653  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040817101295632944512  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016040817121029089345807  ${folder}/preprocess/$s/ABCD_dMRI_pedi.nii.gz

bash distortion.sh ABCD fmri PANDA005 ABCD_fMRI_DistortionMap_PA.nii.gz ABCD_fMRI_DistortionMap_AP.nii.gz ABCD_fMRI_rest.nii.gz
bash distortion.sh ABCD dmri PANDA005 ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.voxel_space.bvecs ABCD_dMRI_pedi.bvals
bet '/autofs/space/erebus_001/users/data/preprocess/PANDA005/ABCD_T1w_MPR_vNav.nii.gz' '/autofs/space/erebus_001/users/data/preprocess/PANDA005/ABCD/ABCD_T1w_MPR_vNav_brain.nii.gz'

mkdir /autofs/space/erebus_001/users/data/preprocess/PANDA005/FS
./hcp_pipelines/Pipelines/FreeSurfer/FreeSurferPipeline.sh --subject=PANDA005 --subjectDIR=/autofs/space/erebus_001/users/data/FS --t1=/autofs/space/erebus_001/users/data/preprocess/PANDA005/ABCD/ABCD_T1w_MPR_vNav.nii.gz --t1brain=/autofs/space/erebus_001/users/data/preprocess/PANDA005/ABCD/ABCD_T1w_MPR_vNav_brain.nii.gz 


s=PANDA005
#bash distortion.sh ABCD fmri $s ABCD_fMRI_DistortionMap_PA.nii.gz ABCD_fMRI_DistortionMap_AP.nii.gz ABCD_fMRI_rest.nii.gz
bash distortion.sh ABCD dMRI $s ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.voxel_space.bvecs ABCD_dMRI_pedi.bvals


s=PANDA007
chgrp -R fiber  ${folder}/$s/
chmod -R 770  ${folder}/$s/
mkdir  ${folder}/preprocess/$s

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041416222444472234118  ${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041416344065314937013  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041416362816918437845  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041416375645539165 ${folder}/preprocess/$s/ABCD_dMRI_pedi.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.201604141737132153151245  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041417371521597351679  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041417374340030452223  ${folder}/preprocess/$s/ABCD_fMRI_rest.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041417442975444458077  ${folder}/preprocess/$s/T2_ABCD.nii.gz

s=PANDA007
#bash distortion.sh ABCD fmri $s ABCD_fMRI_DistortionMap_PA.nii.gz ABCD_fMRI_DistortionMap_AP.nii.gz ABCD_fMRI_rest.nii.gz
bash distortion.sh ABCD dMRI $s ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.voxel_space.bvecs ABCD_dMRI_pedi.bvals



bet ${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz ${folder}/preprocess/$s/T1_mgh_epinav_ABCD_brain.nii.gz

./hcp_pipelines/Pipelines/FreeSurfer/FreeSurferPipeline.sh --subject=PANDA007 --subjectDIR=/autofs/space/erebus_001/users/data/FS/ABCD --t1=${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz --t1brain=${folder}/preprocess/$s/T1_mgh_epinav_ABCD_brain.nii.gz --t2=${folder}/preprocess/$s/T2_ABCD.nii.gz


COMMENT
s=PANDA008
mkdir  ${folder}/preprocess/$s

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041614583974227306960  ${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041615141820882901982  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041615161571471402837  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.201604161517489525504136 ${folder}/preprocess/$s/ABCD_dMRI_pedi.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041615294867951646270  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.201604161529518075646704  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041615301960061847247  ${folder}/preprocess/$s/ABCD_fMRI_rest.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041616001738626337716  ${folder}/preprocess/$s/T2_ABCD.nii.gz

#bash distortion.sh ABCD fmri $s ABCD_fMRI_DistortionMap_PA.nii.gz ABCD_fMRI_DistortionMap_AP.nii.gz ABCD_fMRI_rest.nii.gz
bash distortion.sh ABCD dMRI $s ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.voxel_space.bvecs ABCD_dMRI_pedi.bvals

bet ${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz ${folder}/preprocess/$s/T1_mgh_epinav_ABCD_brain.nii.gz

./hcp_pipelines/Pipelines/FreeSurfer/FreeSurferPipeline.sh --subject=$s --subjectDIR=/autofs/space/erebus_001/users/data/FS/ABCD --t1=${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz --t1brain=${folder}/preprocess/$s/T1_mgh_epinav_ABCD_brain.nii.gz --t2=${folder}/preprocess/$s/T2_ABCD.nii.gz

chgrp -R fiber  ${folder}/preprocess
chmod -R 770  ${folder}/preprocess

chgrp -R fiber  ${folder}/FS
chmod -R 770  ${folder}/FS


<<COMMENT
s=PANDA009
mkdir  ${folder}/preprocess/$s

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041915240310292054946  ${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041915490869202151074  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041915501849111451910  ${folder}/preprocess/$s/ABCD_dMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041915514812209553213 ${folder}/preprocess/$s/ABCD_dMRI_pedi.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041916033264759895347  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_PA.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.201604191603351472895781  ${folder}/preprocess/$s/ABCD_fMRI_DistortionMap_AP.nii.gz
mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041916040477014496324  ${folder}/preprocess/$s/ABCD_fMRI_rest.nii.gz

mri_convert ${folder}/$s/MR.1.3.12.2.1107.5.2.43.67026.2016041916330073332486791  ${folder}/preprocess/$s/T2_ABCD.nii.gz

#bash distortion.sh ABCD fmri $s ABCD_fMRI_DistortionMap_PA.nii.gz ABCD_fMRI_DistortionMap_AP.nii.gz ABCD_fMRI_rest.nii.gz


bash distortion.sh ABCD dMRI $s ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.voxel_space.bvecs ABCD_dMRI_pedi.bvals

bet ${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz ${folder}/preprocess/$s/T1_mgh_epinav_ABCD_brain.nii.gz

./hcp_pipelines/Pipelines/FreeSurfer/FreeSurferPipeline.sh --subject=$s --subjectDIR=/autofs/space/erebus_001/users/data/FS/ABCD --t1=${folder}/preprocess/$s/T1_mgh_epinav_ABCD.nii.gz --t1brain=${folder}/preprocess/$s/T1_mgh_epinav_ABCD_brain.nii.gz --t2=${folder}/preprocess/$s/T2_ABCD.nii.gz


chgrp -R fiber  ${folder}/preprocess
chmod -R 770  ${folder}/preprocess

chgrp -R fiber  ${folder}/FS
chmod -R 770  ${folder}/FS

