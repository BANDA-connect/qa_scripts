#!/bin/bash
# Robert Jones/rjj7 - 2.1.19

folder=/space/erebus/1/users/data
scriptFolder=/space/erebus/1/users/data/code/scripts
subjectBase=BANDA
currSubjNumbs=(5 6 7)
#currSubjNumbs+=`seq 51 1 150`


for subj in ${currSubjNumbs[@]};
do
	subjPad=`printf "%03d" $subj`
	s=${subjectBase}${subjPad}
	
	source /autofs/space/erebus_001/users/data/hcp_pipelines/HCPpipelines/Examples/Scripts/SetUpHCPPipeline.sh
	procdir=/autofs/space/erebus_001/users/data/preprocess
	subj_procdir=$procdir/$s
	gd_coeff_file=/autofs/space/erebus_001/users/data/hcp_pipelines/HCPpipelines/global/config/coeff.grad
	cmd=/space/erebus/1/users/data/hcp_pipelines/HCPpipelines/DiffusionPreprocessing/DiffPreprocPipeline_PostEddy.sh
	cmd+=" --path=${procdir}"
	cmd+=" --subject=${s}"
	cmd+=" --gdcoeffs=${gd_coeff_file}"
	cmd+=" --combine-data-flag=2"
	#echo $cmd >> ${subj_procdir}/Gradient_Unwarping_cmd.txt
	
	running=`qstat | grep rjj7 | wc -l`
	while [[ "$running" -ge 25 ]];
	do
		echo "$running jobs running... waiting..."
		echo ""
		sleep 30s
		echo "......."
		sleep 30s
		running=`qstat | grep rjj7 | wc -l`
	done
	
	pbsubmit -n 2 -m rjj7 -c "$cmd"
done



	

