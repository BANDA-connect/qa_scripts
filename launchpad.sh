<<COMMENT
string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD dMRI PANDA011 dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.voxel_space.bvecs dMRI.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD dMRI PANDA013 dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.voxel_space.bvecs dMRI.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh iPAT2 dMRI PANDA013 dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.voxel_space.bvecs dMRI.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "


string="bash /space/erebus/1/users/data/scripts/distortion.sh iPAT2 dMRI PANDA011 dMRI_DistortionMap_PA.nii.gz dMRI_DistortionMap_AP.nii.gz dMRI.nii.gz dMRI.voxel_space.bvecs dMRI.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD dMRI PANDA010 ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.bvecs ABCD_dMRI_pedi.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh iPAT2 dMRI PANDA010 ABCD_dMRI_DistortionMap_PA.nii.gz ABCD_dMRI_DistortionMap_AP.nii.gz ABCD_dMRI_pedi.nii.gz ABCD_dMRI_pedi.bvecs ABCD_dMRI_pedi.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "



string="bash /space/erebus/1/users/data/scripts/distortion.sh CMRR dMRI PANDA010 dMRI_dir99_PA.nii.gz dMRI_dir99_AP.nii.gz dMRI_dir99_AP.nii.gz dMRI_dir99_AP.bvecs dMRI_dir99_AP.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh CMRR dMRI PANDA011 dMRI_dir99_PA.nii.gz dMRI_dir99_AP.nii.gz dMRI_dir99_AP.nii.gz dMRI_dir99_AP.voxel_space.bvecs dMRI_dir99_AP.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh CMRR dMRI PANDA013 dMRI_dir99_PA.nii.gz dMRI_dir99_AP.nii.gz dMRI_dir99_AP.nii.gz dMRI_dir99_AP.voxel_space.bvecs dMRI_dir99_AP.bvals"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

COMMENT

string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD fMRI PANDA010 ABCD_fMRI_DistortionMap_PA.nii.gz ABCD_fMRI_DistortionMap_AP.nii.gz ABCD_fMRI_rest.nii.gz "
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD fMRI PANDA011 fMRI_DistortionMap_PA1.nii.gz fMRI_DistortionMap_AP1.nii.gz fMRI_rest1.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD fMRI PANDA011 fMRI_DistortionMap_PA1.nii.gz fMRI_DistortionMap_AP1.nii.gz fMRI_rest2.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "


string="bash /space/erebus/1/users/data/scripts/distortion.sh iPAT2 fMRI PANDA011 fMRI_DistortionMap_PA1.nii.gz fMRI_DistortionMap_AP1.nii.gz fMRI_rest1.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh iPAT2 fMRI PANDA011 fMRI_DistortionMap_PA1.nii.gz fMRI_DistortionMap_AP1.nii.gz fMRI_rest2.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh CMRR fMRI PANDA011 rfMRI_REST_PA.nii.gz rfMRI_REST_AP.nii.gz fMRI_rest2.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "


string="bash /space/erebus/1/users/data/scripts/distortion.sh ABCD fMRI PANDA013 fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI_rest.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh iPAT2 fMRI PANDA013 fMRI_DistortionMap_PA.nii.gz fMRI_DistortionMap_AP.nii.gz fMRI.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

string="bash /space/erebus/1/users/data/scripts/distortion.sh CMRR fMRI PANDA013 rfMRI_REST_PA.nii.gz rfMRI_REST_AP.nii.gz fMRI_rest2.nii.gz"
echo pbsubmit -m vsiless -c " ${string} "
pbsubmit -n 1  -m vsiless -c " ${string} "

