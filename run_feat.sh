 #!/bin/bash 
function first_level()
{
studies=(  CMRR ) #  iPAT2 ABCD )
subjects=(PANDA002d)
run=(1 2)
skip=8

for s in ${subjects[@]};
do
for study in ${studies[@]};
do
for r in ${run[@]};
do

	#run 1 PA for CMRR
	file_design=/space/erebus/1/users/data/preprocess/feat/$s/faceMatching_${study}_${r}_FT.fsf
	cp /space/erebus/1/users/data/preprocess/feat/faceMatching_template.fsf ${file_design}
	sed -i -- 's/SUBJECT_VIVI/'${s}'/g'  ${file_design}
	sed -i -- 's/STUDY_VIVI/'${study}'/g'  ${file_design}
	sed -i -- 's/RUN_VIVI/faceMatching_'$r'_skip'${skip}'_FT/g'  ${file_design}
	sed -i -- 's/TIME_RUN_TASK_VIVI/task003_run00'$r'/g'  ${file_design}
	if [ "${study}" = "CMRR"  ]; then
		if [ "${r}" = "1"  ]; then
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_faceMatching_PA.nii.gz/g'  ${file_design}
		else
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_faceMatching_AP.nii.gz/g'  ${file_design}
		fi
		sed -i -- 's/NUMBER_OF_VOLS_VIVI/346/g'  ${file_design}
		sed -i -- 's/NUMBER_VOLS_DELETE_VIVI/'${skip}'/g'  ${file_design}
		sed -i -- 's/SEQ_VIVI/3/g'  ${file_design}
	else
		if [ "${r}" = "1"  ]; then
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_faceMatching1.nii.gz/g'  ${file_design}
		else
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_faceMatching2.nii.gz/g'  ${file_design}
		fi

		sed -i -- 's/NUMBER_OF_VOLS_VIVI/338/g'  ${file_design}
		sed -i -- 's/NUMBER_VOLS_DELETE_VIVI/0/g'  ${file_design}
		if [ "${study}" = "ABCD"  ]; then
			sed -i -- 's/SEQ_VIVI/1/g'  ${file_design}
		else
			sed -i -- 's/SEQ_VIVI/2/g'  ${file_design}
		fi
	
	fi
	
	pbsubmit -n 1  -m vsiless -c "feat ${file_design} "
		
	
	#run 1 PA for CMRR
	file_design=/space/erebus/1/users/data/preprocess/feat/$s/gambling_${study}_${r}_FT.fsf
	cp /space/erebus/1/users/data/preprocess/feat/gambling_template.fsf ${file_design}
	sed -i -- 's/SUBJECT_VIVI/'${s}'/g'  ${file_design}
	sed -i -- 's/STUDY_VIVI/'${study}'/g'  ${file_design}
	sed -i -- 's/RUN_VIVI/gambling_'$r'_skip'${skip}'_FT/g'  ${file_design}
	sed -i -- 's/TIME_RUN_TASK_VIVI/task002_run00'$r'/g'  ${file_design}
	if [ "${study}" = "CMRR"  ]; then
		if [ "${r}" = "1"  ]; then
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_gambling_PA.nii.gz/g'  ${file_design}
		else
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_gambling_AP.nii.gz/g'  ${file_design}
		fi
		sed -i -- 's/NUMBER_OF_VOLS_VIVI/223/g'  ${file_design}
		sed -i -- 's/NUMBER_VOLS_DELETE_VIVI/'${skip}'/g'  ${file_design}
		sed -i -- 's/SEQ_VIVI/3/g'  ${file_design}
	else
		if [ "${r}" = "1"  ]; then
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_gambling1.nii.gz/g'  ${file_design}
		else
			sed -i -- 's/TASK_FILE_VIVI/tfMRI_gambling2.nii.gz/g'  ${file_design}
		fi
		sed -i -- 's/NUMBER_OF_VOLS_VIVI/215/g'  ${file_design}
		sed -i -- 's/NUMBER_VOLS_DELETE_VIVI/0/g'  ${file_design}
		if [ "${study}" = "ABCD"  ]; then
			sed -i -- 's/SEQ_VIVI/1/g'  ${file_design}
		else
			sed -i -- 's/SEQ_VIVI/2/g'  ${file_design}
		fi	
	fi


#	feat ${file_design} &
	pbsubmit -n 1  -m vsiless -c "feat ${file_design} "

	
done
done
done
}

#:<<hola
function second_level()
{
echo "hi"
studies=(  CMRR) #iPAT2 ABCD )
subjects=(PANDA002d)
skip=3
for s in ${subjects[@]};
do
for study in ${studies[@]};
do
	file_design=/space/erebus/1/users/data/preprocess/feat/$s/second_faceMatching_${study}.fsf
	cp /space/erebus/1/users/data/preprocess/feat/second_faceMatching_template.fsf ${file_design}
	sed -i -- 's/SUBJECT_VIVI/'${s}'/g'  ${file_design}
	sed -i -- 's/STUDY_VIVI/'${study}'/g'  ${file_design}
	sed -i -- 's/RUN_VIVI/faceMatching_1and2_skip'${skip}'_FT/g'  ${file_design}
	sed -i -- 's/RUN_1_VIVI/faceMatching_1_skip'${skip}'_FT.feat/g'  ${file_design}
	sed -i -- 's/RUN_2_VIVI/faceMatching_2_skip'${skip}'_FT.feat/g'  ${file_design}
	feat ${file_design} &
	

	
	#second level analysis
	file_design=/space/erebus/1/users/data/preprocess/feat/$s/second_gambling_${study}.fsf
	cp /space/erebus/1/users/data/preprocess/feat/second_gambling_template.fsf ${file_design}
	sed -i -- 's/SUBJECT_VIVI/'${s}'/g'  ${file_design}
	sed -i -- 's/STUDY_VIVI/'${study}'/g'  ${file_design}
	sed -i -- 's/RUN_VIVI/gambling_1and2_skip'${skip}'_FT/g'  ${file_design}
	sed -i -- 's/RUN_1_VIVI/gambling_1_skip'${skip}'_FT.feat/g'  ${file_design}
	sed -i -- 's/RUN_2_VIVI/gambling_2_skip'${skip}'_FT.feat/g'  ${file_design}
	feat ${file_design} &
done
done

}

function copy_things()
{
studies=(  CMRR ) #iPAT2 ABCD )
subjects=(PANDA002d)
skip=8

for s in ${subjects[@]};
do
for study in ${studies[@]};
do
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/faceMatching_1and2_skip${skip}_FT+.gfeat/cope1.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Happy_gt_Neutral_${study}_${skip}.png
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/faceMatching_1and2_skip${skip}_FT+.gfeat/cope2.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Neutral_gt_Happy_${study}_${skip}.png
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/faceMatching_1and2_skip${skip}_FT+.gfeat/cope3.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Happy_gt_Fear_${study}_${skip}.png
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/faceMatching_1and2_skip${skip}_FT+.gfeat/cope4.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Fear_gt_Happy_${study}_${skip}.png
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/faceMatching_1and2_skip${skip}_FT+.gfeat/cope5.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Fear_gt_Neutral_${study}_${skip}.png
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/faceMatching_1and2_skip${skip}_FT+.gfeat/cope6.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Neutral_gt_Fear_${study}_${skip}.png

	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/gambling_1and2_skip${skip}_FT+.gfeat/cope1.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Reward_gt_Loss_${study}_${skip}.png
	cp /space/erebus/1/users/data/preprocess/feat/$s/${study}/gambling_1and2_skip${skip}_FT+.gfeat/cope2.feat/rendered_thresh_zstat1.png  /space/erebus/1/users/data/preprocess/feat/$s/pngs/Loss_gt_Reward_${study}_${skip}.png

done
done
}


$@




