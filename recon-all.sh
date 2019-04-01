subjects=( PANDA023 PANDA021 PANDA011 PANDA013 PANDA014 PANDA016 PANDA017 PANDA018 PANDA019 PANDA020  PANDA022)
protocols=( ABCD CMRR ) #iPAT2 ) #ABCD
for s in ${subjects[@]};
do
	for p in ${protocols[@]};
	do
#		pbsubmit -n 1 -m vsiless -c "recon-all -subject $s -all -aparc2aseg -i /space/erebus/1/users/data/preprocess/$s/$p/T1.nii.gz -sd /space/erebus/1/users/data/preprocess/FS/$p"
		pbsubmit -n 1 -m vsiless -c "recon-all -subject $s -all -sd /space/erebus/1/users/data/preprocess/FS/$p"
	done
done
