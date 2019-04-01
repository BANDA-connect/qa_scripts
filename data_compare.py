#/space/erebus/1/users/jwang/jon2/bin/python3.6 /space/erebus/1/users/data/code/scripts/data_compare.py
'''
Functions:
Data cross referenced from:
/space/erebus/1/users/admin/participant_info/participant_contact info.csv
/space/erebus/1/users/admin/participant_info/participant_diagnosis.txt
REDCap Clinical Interview Data - KSADS assessment

control vs anx vs dep
1. aparc_compare (cortical thickness)
2. aseg_compare (subcortical structure volumes)
3. aseg_compare_bvolume

KSAD scores
not present vs probable vs definite
1. aparc_compare_KSADS
2. aseg_compare_KSADS



'''
import csv
import os
import math
import numpy as np
import nibabel as nib
import os.path
import matplotlib
print( matplotlib.get_cachedir())
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import glob
import fnmatch
import readClinical

subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015", "BANDA016", "BANDA017","BANDA018","BANDA019","BANDA020","BANDA021","BANDA022","BANDA023","BANDA024","BANDA025","BANDA026","BANDA027","BANDA028","BANDA029","BANDA030","BANDA031","BANDA032",
"BANDA033","BANDA034","BANDA035","BANDA036","BANDA037","BANDA038","BANDA039","BANDA040",
"BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049",
"BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060","BANDA061","BANDA062","BANDA063"]
control_subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014","BANDA016","BANDA018","BANDA027","BANDA033","BANDA034","BANDA038","BANDA043","BANDA046","BANDA050","BANDA051","BANDA054","BANDA058","BANDA059","BANDA061"]
dep_subjects = ["BANDA024","BANDA047"]
anx_subjects = ["BANDA017","BANDA021","BANDA022","BANDA023","BANDA025","BANDA026","BANDA030","BANDA031","BANDA032","BANDA035","BANDA036","BANDA039","BANDA040","BANDA041","BANDA042","BANDA048","BANDA049","BANDA052","BANDA055","BANDA056",
"BANDA057","BANDA060","BANDA063"]
dep_and_anx_subjects = ["BANDA006","BANDA015","BANDA019","BANDA020","BANDA028","BANDA029","BANDA037","BANDA044","BANDA045","BANDA053","BANDA062"]

'''
#TEST
subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA006"]
dep_subjects = ["BANDA001","BANDA002"]
anx_subjects = ["BANDA003"]
dep_and_anx_subjects = ["BANDA004"]
control_subjects = ["BANDA005", "BANDA006"]
'''

output="/space/erebus/1/users/jwang/comparisonPlots_1_63/"
output="/space/erebus/1/users/banda/plots"


structures = {
'Lateral Ventricle':[4,43], 
'Inferior Lateral Ventricle':[5,44], 
'Cerebellum - White Matter':[7,46], 
'Cerebellum - Cortex':[8,47],
'Thalamus':[10,49],
'Caudate':[11,50],
'Putamen':[12,51],
'Pallidum':[13,52],
'3rd Ventricle':[14],
'4th Ventricle':[15],
'Brain Stem':[16],
'Hippocampus':[17,53],
'Amygdala':[18,54],
#'Insula':[19,55],
'CSF':[24],
'Accumbens':[26,58],
'Ventral DC':[28,60],
'vessel':[30,62],
'Choroid plexus':[31,63],
'5th Ventricle':[72],
'Optic Chiasm':[85],
'CC_Posterior':[251],
'CC_Mid_Posterior':[252],
'CC_Central':[253],
'CC_Mid_Anterior':[254],
'CC_Anterior':[255],
'Pons':[174]
}


structures = {
'Lateral Ventricle':[4,43], 
'Inferior Lateral Ventricle':[5,44], 
'Thalamus':[10,49],
'Caudate':[11,50],
'Putamen':[12,51],
'Pallidum':[13,52],
'Brain Stem':[16],
'Hippocampus':[17,53],
'Amygdala':[18,54],
'Accumbens':[26,58],
'CC_Mid_Anterior':[254],
'CC_Anterior':[255],
'Pons':[174]
}

def aparc_compare_MFQ():
	'''
	Each dot is subject
	y-axis cortical thickness
	x-axis MFQ total score
	'''
	structures = {
'Lateral and Medial Orbitofrontal':[70, 72],
'Precuneus':[83],
'Insula':[93],
'Caudal and Rostral Anterior Cingulate': [61,84],
'Temporal Lobe':[67, 73, 88, 60, 65, 91, 64, 92, 74],
#Temporal Lobe: Superior, Middle, and Inferior Temporal, Banks of the Superior Temporal Sulcus, Fusiform, Transverse Temporal, Entorhinal, Temporal Pole, Parahippocampal 
'Parahippocampal':[74],
'Rostral Middle Frontal':[85],
'Superior Frontal':[86]
}

	#[control, anxious, comorbid, depressed]
	boxplot_data = [[],[],[],[]]
	right_boxplot_data = [[],[],[],[]]




	for structure in structures:
		f, (ax1,ax2) = plt.subplots(nrows=2,ncols=1,figsize=(23,14))
		f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)
		min_value = 0
		max_value = 0
		x_ticks = []
		for s_index,s in enumerate(subjects):	
			lh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/lh.aparc.stats')
			rh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/rh.aparc.stats')

			lh_thickness=0
			rh_thickness=0

			for i in structures[structure]:
				lh_list = open(lh_parc_file[0],'r').readlines()[i].split()
				rh_list = open(rh_parc_file[0],'r').readlines()[i].split()
	
				#StructName NumVert SurfArea GrayVol ThickAvg ThickStd MeanCurv GausCurv FoldInd CurvInd

				#Global Mean Cortical Thickness weighted by Surface Area
				#bh.thickness = ( (lh.thickness * lh.surfarea) + (rh.thickness * rh.surfarea) ) / (lh.surfarea + rh.surfarea) 
				#thickness += (  ( ( float(lh_list[4])*float(lh_list[2]) )+ ( float(rh_list[4])*float(rh_list[2]) ) ) / (float(lh_list[2]) + float(rh_list[2]) ) )/(structures[structure].index(i)+1)
				lh_thickness += float(lh_list[4])
				rh_thickness += float(rh_list[4])
				if structures[structure].index(i) == len(structures[structure])-1:
					lh_thickness == lh_thickness/ len(structures[structure])
					rh_thickness == rh_thickness/ len(structures[structure])
				


			#no current color assignment
			csvfile = open('/space/erebus/1/users/jwang/MFQ_i.csv')
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['banda_id']==s:
					print (s)
					print (row['mfq_i_total'])
					print (lh_thickness)
					print (rh_thickness)	
					ax1.plot(int(row['mfq_i_total']), lh_thickness, "-o",markersize=5,c='r')
					ax2.plot(int(row['mfq_i_total']), rh_thickness, "-o",markersize=5,c='r')
					if min_value == 0: min_value = lh_thickness
					min_value = min(min_value,lh_thickness,rh_thickness)					
					max_value = max(max_value,lh_thickness,rh_thickness)
					x_ticks.append(int(row['mfq_i_total']))

		
		ax1.set_ylabel("Global Mean Cortical Thickness")
		ax1.set_title("Left " + structure)
		ax1.set_xlabel("MFQ total score")

		ax2.set_ylabel("Global Mean Cortical Thickness")
		ax2.set_title("Right " + structure)
		ax2.set_xlabel("MFQ total score")

		ax1.set_xticks(x_ticks)
		ax2.set_xticks(x_ticks)
		#ax1.set_xticklabels(x_labels,rotation=45)
		#ax2.set_xticklabels(x_labels,rotation=45, ha="right")

		ax1.set_ylim(min_value-.15,max_value+.15)
		ax2.set_ylim(min_value-.15,max_value+.15)
		f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/MFQ/"+structure+"_i_thickness_compare",dpi=199)	

	'''
	control_patch = mpatches.Patch(color='r', label='not present')
	probable_patch = mpatches.Patch(color='c', label='probable')
	definite_patch = mpatches.Patch(color='m', label='definite')
	ax1.legend(handles=[control_patch,probable_patch,definite_patch])
	ax2.legend(handles=[control_patch,probable_patch,definite_patch])
	print(len(disorders))
	'''
		


	


aparc_compare_MFQ()

'''
#wrong
def aparc_compare_KSADS():
	structures = {
'Lateral and Medial Orbitofrontal':[70, 72],
'Precuneus':[83],
'Insula':[93],
'Caudal and Rostral Anterior Cingulate': [61,84],
'Temporal Lobe':[67, 73, 88, 60, 65, 91, 64, 92, 74],
#Temporal Lobe: Superior, Middle, and Inferior Temporal, Banks of the Superior Temporal Sulcus, Fusiform, Transverse Temporal, Entorhinal, Temporal Pole, Parahippocampal 
'Parahippocampal':[74],
'Rostral Middle Frontal':[85],
'Superior Frontal':[86]
}

	#[control, anxious, comorbid, depressed]
	boxplot_data = [[],[],[],[]]
	right_boxplot_data = [[],[],[],[]]

	controls = []
	definite_subjects = []
	probable_subjects = []
	
	Criteria for Probable Diagnosis
	1. Meets criteria for core symptoms of the disorder.
	2. Meets all but one, or a minimum of 75% of the remaining criteria required for the diagnosis,
	and
	3. Evidence of functional impairment
	
	f, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
	f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)


	csvfile = open('/space/erebus/1/users/jwang/KSADS.csv')
	reader = csv.DictReader(csvfile)
	disorders =[]
	#excluded_disorders = ['enuresis_current_i', 'encopresis_current_i', 'anorexia_current_i', 'bulimia_current_i', 'adhd_current_i','tourettes_current_i', 'tourettes_dsm5_current_i', 'chronic_tic_current_i', 'chronic_tic_dsm5_current_i', 'transient_tic_current_i', 'transient_tic_dsm5_current_i', 'alcohol_abuse_current_i', 'alcohol_depend_current_i', 'alcohol_use_dsm5_current_i', 'alcohol_unspec_dsm5_current_i', 'substance_abuse_current_i', 'substance_depend_current_i', 'substance_use_dsm5_current_i', 'mental_current_i', 'other_current_i', 'other_dx_current_i']

	for disorder in reader.fieldnames:
		if fnmatch.fnmatch(disorder,'*_current_i') and not fnmatch.fnmatch(disorder,'*_dsm5_current_i'):
			disorders.append(disorder)

	x_ticks = []
	x_labels = []
	min_value = 0
	max_value = 0
	for s_index,s in enumerate(subjects):	
		lh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/lh.aparc.stats')
		rh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/rh.aparc.stats')
		lh_thickness=0
		rh_thickness=0
		for structure in structures:
			for i in structures[structure]:
				lh_list = open(lh_parc_file[0],'r').readlines()[i].split()
				rh_list = open(rh_parc_file[0],'r').readlines()[i].split()
	
				#StructName NumVert SurfArea GrayVol ThickAvg ThickStd MeanCurv GausCurv FoldInd CurvInd

				#Global Mean Cortical Thickness weighted by Surface Area
				#bh.thickness = ( (lh.thickness * lh.surfarea) + (rh.thickness * rh.surfarea) ) / (lh.surfarea + rh.surfarea) 
				#thickness += (  ( ( float(lh_list[4])*float(lh_list[2]) )+ ( float(rh_list[4])*float(rh_list[2]) ) ) / (float(lh_list[2]) + float(rh_list[2]) ) )/(structures[structure].index(i)+1)
				lh_thickness += float(lh_list[4])
				rh_thickness += float(rh_list[4])
				if structures[structure].index(i) == len(structures[structure])-1:
					lh_thickness == lh_thickness/ len(structures[structure])
					rh_thickness == rh_thickness/ len(structures[structure])
				
			ax1.set_ylabel("Global Mean Cortical Thickness")
			ax1.set_title("Left " + structure)
			ax2.set_ylabel("Global Mean Cortical Thickness")
			ax2.set_title("Right " + structure)
		
			#color by diagnosis severity
			csvfile = open('/space/erebus/1/users/jwang/KSADS.csv')
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['banda_id']==s:
					print('hello')
					disorder_seperator = .1
					for disorder in disorders:
						x_ticks.append(disorder_seperator)
						x_labels.append(disorder.strip('_current_i'))
						print (disorder)
						print (row[disorder])
						print (row[disorder]=='1')
						if row[disorder]=='1':
							ax1.plot(disorder_seperator+random.uniform(-0.3,0.3), lh_thickness, "-o",markersize=5,c='r')
							ax2.plot(disorder_seperator+random.uniform(-0.3,0.3), rh_thickness, "-o",markersize=5,c='r')
						elif row[disorder]=='2':
							ax1.plot(disorder_seperator+random.uniform(-0.3,0.3), lh_thickness, "-o",markersize=5,c='c')
							ax2.plot(disorder_seperator+random.uniform(-0.3,0.3), rh_thickness, "-o",markersize=5,c='c')
						elif row[disorder]=='4':
							ax1.plot(disorder_seperator+random.uniform(-0.3,0.3), lh_thickness, "-o",markersize=5,c='m')
							ax2.plot(disorder_seperator+random.uniform(-0.3,0.3), rh_thickness, "-o",markersize=5,c='m')
						disorder_seperator+=2	
						if min_value == 0: min_value = lh_thickness
						min_value = min(min_value,lh_thickness,rh_thickness)					
						max_value = max(max_value,lh_thickness,rh_thickness)					

	#ax1.axes.get_xaxis().set_visible(False)
	#ax2.axes.get_xaxis().set_visible(False)
	ax1.set_xticks(x_ticks)
	ax2.set_xticks(x_ticks)
	ax1.set_xticklabels(x_labels,rotation=45)
	ax2.set_xticklabels(x_labels,rotation=45, ha="right")

	ax1.set_ylim(min_value-.15,max_value+.15)
	ax2.set_ylim(min_value-.15,max_value+.15)

	control_patch = mpatches.Patch(color='r', label='not present')
	probable_patch = mpatches.Patch(color='c', label='probable')
	definite_patch = mpatches.Patch(color='m', label='definite')
	ax1.legend(handles=[control_patch,probable_patch,definite_patch])
	ax2.legend(handles=[control_patch,probable_patch,definite_patch])
	print(len(disorders))
	f.savefig(output+"/aparc/"+structure+"_thickness_compare_KSADS",dpi=199)	
	plt.show()
'''


def aparc_compare(structure):
	structures = {
'Lateral and Medial Orbitofrontal':[70, 72],
'Precuneus':[83],
'Insula':[93],
'Caudal and Rostral Anterior Cingulate': [61,84],
'Temporal Lobe':[67, 73, 88, 60, 65, 91, 64, 92, 74],
#Temporal Lobe: Superior, Middle, and Inferior Temporal, Banks of the Superior Temporal Sulcus, Fusiform, Transverse Temporal, Entorhinal, Temporal Pole, Parahippocampal 
'Parahippocampal':[74],
'Rostral Middle Frontal':[85],
'Superior Frontal':[86]
}

	control_total = 0
	anxious_total = 0
	comorbid_total = 0
	depressed_total = 0

	right_control_total = 0
	right_anxious_total = 0
	right_comorbid_total = 0
	right_depressed_total = 0
	f, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,14))

	#[control, anxious, comorbid, depressed]
	boxplot_data = [[],[],[],[]]
	right_boxplot_data = [[],[],[],[]]

	for s_index,s in enumerate(subjects):	
		lh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/lh.aparc.stats')
		rh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/rh.aparc.stats')
		lh_thickness=0
		rh_thickness=0
		for i in structures[structure]:
			lh_list = open(lh_parc_file[0],'r').readlines()[i].split()
			rh_list = open(rh_parc_file[0],'r').readlines()[i].split()
	
			#StructName NumVert SurfArea GrayVol ThickAvg ThickStd MeanCurv GausCurv FoldInd CurvInd

			#Global Mean Cortical Thickness weighted by Surface Area
			#bh.thickness = ( (lh.thickness * lh.surfarea) + (rh.thickness * rh.surfarea) ) / (lh.surfarea + rh.surfarea) 
			#thickness += (  ( ( float(lh_list[4])*float(lh_list[2]) )+ ( float(rh_list[4])*float(rh_list[2]) ) ) / (float(lh_list[2]) + float(rh_list[2]) ) )/(structures[structure].index(i)+1)
			lh_thickness += float(lh_list[4])
			rh_thickness += float(rh_list[4])
			if structures[structure].index(i) == len(structures[structure])-1:
				print("Hi")
				lh_thickness == lh_thickness/ len(structures[structure])
				rh_thickness == rh_thickness/ len(structures[structure])
				
		ax1.set_ylabel("Global Mean Cortical Thickness")
		ax1.set_title("Left " + structure)
		ax2.set_ylabel("Global Mean Cortical Thickness")
		ax2.set_title("Right " + structure)
		#color by subject type
		if s in control_subjects:
			ax1.plot(1+random.uniform(0,0.3), lh_thickness, "-o",c='r')
			control_total += lh_thickness
			ax2.plot(1+random.uniform(0,0.3), rh_thickness, "-o",c='r')
			right_control_total += rh_thickness

			boxplot_data[0].append(lh_thickness)
			right_boxplot_data[0].append(rh_thickness)
		elif s in anx_subjects:
			ax1.plot(1.5+random.uniform(0,0.3), lh_thickness, "-o",c='c')
			anxious_total += lh_thickness
			ax2.plot(1.5+random.uniform(0,0.3), rh_thickness, "-o",c='c')
			right_anxious_total += rh_thickness

			boxplot_data[1].append(lh_thickness)
			right_boxplot_data[1].append(rh_thickness)
		elif s in dep_and_anx_subjects:
			ax1.plot(2+random.uniform(0,0.3), lh_thickness, "-o",c='m')
			comorbid_total += lh_thickness
			ax2.plot(2+random.uniform(0,0.3), rh_thickness, "-o",c='m')
			right_comorbid_total += rh_thickness

			boxplot_data[2].append(lh_thickness)
			right_boxplot_data[2].append(rh_thickness)			
		elif s in dep_subjects:
			ax1.plot(2.5+random.uniform(0,0.3), lh_thickness, "-o",c='y')
			depressed_total += lh_thickness
			ax2.plot(2.5+random.uniform(0,0.3), rh_thickness, "-o",c='y')
			right_depressed_total += rh_thickness

			boxplot_data[3].append(lh_thickness)
			right_boxplot_data[3].append(rh_thickness)



	ax1.axes.get_xaxis().set_visible(False)
	ax2.axes.get_xaxis().set_visible(False)

	max_list = [ max(a) for a in boxplot_data]
	min_list = [ min(a) for a in boxplot_data]
	#right_max_list = [ max(a) for a in right_boxplot_data]
	#right_min_list = [ min(a) for a in right_boxplot_data]

	ax1.set_ylim(min(min_list)-3,max(max_list)+3)
	ax2.set_ylim(min(min_list)-3,max(max_list)+3)

	control_patch = mpatches.Patch(color='r', label='control '+str(round(control_total/len(control_subjects),4)))
	anxious_patch = mpatches.Patch(color='c', label='anxious '+str(round(anxious_total/len(anx_subjects),4)))
	comorbid_patch = mpatches.Patch(color='m', label='comorbid '+str(round(comorbid_total/len(dep_and_anx_subjects),4)))
	depressed_patch = mpatches.Patch(color='y', label='depressed '+str(round(depressed_total/len(dep_subjects),4)))
	ax1.legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])

	right_control_patch = mpatches.Patch(color='r', label='control '+str(round(right_control_total/len(control_subjects),4)))
	right_anxious_patch = mpatches.Patch(color='c', label='anxious '+str(round(right_anxious_total/len(anx_subjects),4)))
	right_comorbid_patch = mpatches.Patch(color='m', label='comorbid '+str(round(right_comorbid_total/len(dep_and_anx_subjects),4)))
	right_depressed_patch = mpatches.Patch(color='y', label='depressed '+str(round(right_depressed_total/len(dep_subjects),4)))
	ax2.legend(handles=[right_control_patch,right_anxious_patch,right_comorbid_patch,right_depressed_patch])



	#box plot measures
	g, (boxes1,boxes2) = plt.subplots(nrows=1,ncols=2,figsize=(10,14))
	boxes1.set_title("Left " + structure)
	boxes2.set_title("Right "+structure)
	boxes1.set_ylim(min(min_list)-.25,max(max_list)+.25)
	boxes2.set_ylim(min(min_list)-.25,max(max_list)+.25)
	if structure == "Temporal Lobe":
		boxes1.set_ylim(min(min_list)-1.5,max(max_list)+1.5)
		boxes2.set_ylim(min(min_list)-1.5,max(max_list)+1.5)
		ax1.set_ylim(min(min_list)-6,max(max_list)+6)
		ax2.set_ylim(min(min_list)-6,max(max_list)+6)
	boxes1.boxplot(boxplot_data,labels=['control','anxious','comorbid','depressed'])
	boxes2.boxplot(right_boxplot_data,labels=['control','anxious','comorbid','depressed'])

	f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aparc/"+structure+"_thickness_compare",dpi=199)
	#plt.show()
	g.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aparc/"+structure+"_boxplot",dpi=199)



def plot_structures(structs):
	disordersWeights = readClinical.readKSADS()
	print(len(disordersWeights))
	colors=['red','blue','green','violet','cyan','black']
	for structure in structs:
		print("plotting ",structure)
		if structure in structures.keys(): 
			if len(structures[structure])>1:
				f, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,14))
			else:
				f, ax1 = plt.subplots(nrows=1,figsize=(15,14))
					
			anatomy_label_1 = str(structures[structure][0]) 
			if len(structures[structure])>1:		
				anatomy_label_2 = str(structures[structure][1])  #right side
			
			#left side if bilateral
			control_total = 0
			anxious_total = 0
			comorbid_total = 0
			depressed_total = 0

			right_control_total = 0
			right_anxious_total = 0
			right_comorbid_total = 0
			right_depressed_total = 0

			#[control, anxious, comorbid, depressed]
			boxplot_data = [[],[],[],[]]
			right_boxplot_data = [[],[],[],[]]

			for s_index,s in enumerate(subjects):			
				if s in disordersWeights:
					
					talairach="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/transforms/talairach.xfm"
					aseg ="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/aseg.mgz"
					
					if os.path.isfile(talairach) & os.path.isfile(aseg):
						vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" " +anatomy_label_1).read()
						side= str(vol.split("\n")[2])
						side_percent = str(side.split(" ")[7])
						ax1.set_ylabel("percentage of eTIV")
						ax1.set_xlabel('Subject Type')
						if len(structures[structure])>1:		
							vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" "+anatomy_label_2).read()
							right_side= str(vol.split("\n")[2])
							right_side_percent = str(right_side.split(" ")[7])
							ax2.set_ylabel("percentage of eTIV")
							ax2.set_xlabel('Subject Type')

				
						weights = disordersWeights[s]
						"""
						ax1.plot(sum(weights), float(side_percent.strip('%')), "-o",c=colors[5])
						if len(structures[structure])>1:		
							ax2.plot(sum(weights), float(right_side_percent.strip('%')), "-o",c=colors[5])
						"""
						for disorder in [0,2]:

							ax1.plot(weights[disorder]+weights[disorder+1], float(side_percent.strip('%')), "-o",c=colors[disorder])
							control_total += float(side_percent.strip('%'))

							if len(structures[structure])>1:		
								ax2.plot(weights[disorder]+weights[disorder+1], float(right_side_percent.strip('%')), "-o",c=colors[disorder])
								right_control_total += float(right_side_percent.strip('%'))
						

			#ax1.set_ylim((0,0.8))
			ax1.set_title(structure)
			ax1.axes.get_xaxis().set_visible(False)

			if len(structures[structure])>1:
				#ax2.set_ylim((0,.8))
				ax1.set_title("Left "+structure)
				ax2.set_title("Right "+structure)
				ax2.axes.get_xaxis().set_visible(False)
				
			affective_patch = mpatches.Patch(color=colors[0], label='Affective ')
			anxiety_patch = mpatches.Patch(color=colors[1], label='Anxiety ')
			psychotic_patch = mpatches.Patch(color=colors[2], label='Psychotic ')
			behavioral_patch = mpatches.Patch(color=colors[3], label='Behavioral ')
			substance_patch = mpatches.Patch(color=colors[4], label='Substance ')
			all_patch = mpatches.Patch(color=colors[5], label='all')
			ax1.legend(handles=[affective_patch,anxiety_patch,psychotic_patch,behavioral_patch,substance_patch,all_patch])

			if len(structures[structure])>1:	
				ax2.legend(handles=[affective_patch,anxiety_patch,psychotic_patch,behavioral_patch,substance_patch,all_patch])


			f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aseg/"+structure+"_compare",dpi=199)
		
		else:
			print('must input valid structure') 
			print(structures)
	plt.show()

def aseg_compare(structure):

	if structure in structures.keys(): 
		if len(structures[structure])>1:
			f, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,14))
		else:
			f, ax1 = plt.subplots(nrows=1,figsize=(15,14))
		#f.tight_layout()
		#f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
				
		anatomy_label_1 = str(structures[structure][0]) 
		if len(structures[structure])>1:		
			anatomy_label_2 = str(structures[structure][1])  #right side
		
		#left side if bilateral
		control_total = 0
		anxious_total = 0
		comorbid_total = 0
		depressed_total = 0

		right_control_total = 0
		right_anxious_total = 0
		right_comorbid_total = 0
		right_depressed_total = 0

		#[control, anxious, comorbid, depressed]
		boxplot_data = [[],[],[],[]]
		right_boxplot_data = [[],[],[],[]]

		for s_index,s in enumerate(subjects):			
			talairach="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/transforms/talairach.xfm"
			aseg ="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/aseg.mgz"
			#print (s)
			#print (s_index)
			if os.path.isfile(talairach) & os.path.isfile(aseg):
				vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" " +anatomy_label_1).read()
				side= str(vol.split("\n")[2])
				side_percent = str(side.split(" ")[7])
				ax1.set_ylabel("percentage of eTIV")
				ax1.set_xlabel('Subject Type')
				if len(structures[structure])>1:		
					vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" "+anatomy_label_2).read()
					right_side= str(vol.split("\n")[2])
					right_side_percent = str(right_side.split(" ")[7])
					ax2.set_ylabel("percentage of eTIV")
					ax2.set_xlabel('Subject Type')

				#color by subject type
				if s in control_subjects:
					ax1.plot(1+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='r')
					control_total += float(side_percent.strip('%'))

					boxplot_data[0].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:		
						ax2.plot(1+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='r')
						right_control_total += float(right_side_percent.strip('%'))
						right_boxplot_data[0].append(float(side_percent.strip('%')))
				elif s in anx_subjects:
					ax1.plot(1.5+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='c')
					anxious_total += float(side_percent.strip('%'))
					boxplot_data[1].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:
						ax2.plot(1.5+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='c')		
						right_anxious_total += float(right_side_percent.strip('%'))
						right_boxplot_data[1].append(float(side_percent.strip('%')))
				elif s in dep_and_anx_subjects:
					ax1.plot(2+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='m')
					comorbid_total += float(side_percent.strip('%'))
					boxplot_data[2].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:	
						ax2.plot(2+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='m')
						right_comorbid_total += float(right_side_percent.strip('%'))
						right_boxplot_data[2].append(float(side_percent.strip('%')))
				elif s in dep_subjects:
					ax1.plot(2.5+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='y')
					depressed_total += float(side_percent.strip('%'))
					boxplot_data[3].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:	
						ax2.plot(2.5+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='y')	
						right_depressed_total += float(right_side_percent.strip('%'))
						right_boxplot_data[3].append(float(side_percent.strip('%')))

		ax1.set_ylim((0,1.2))
		ax1.set_title(structure)
		ax1.axes.get_xaxis().set_visible(False)

		if len(structures[structure])>1:
			ax2.set_ylim((0,1.2))
			ax1.set_title("Left "+structure)
			ax2.set_title("Right "+structure)
			ax2.axes.get_xaxis().set_visible(False)
		control_patch = mpatches.Patch(color='r', label='control '+str(round(control_total/len(control_subjects),4))+'%')
		anxious_patch = mpatches.Patch(color='c', label='anxious '+str(round(anxious_total/len(anx_subjects),4))+'%')
		comorbid_patch = mpatches.Patch(color='m', label='comorbid '+str(round(comorbid_total/len(dep_and_anx_subjects),4))+'%')
		depressed_patch = mpatches.Patch(color='y', label='depressed '+str(round(depressed_total/len(dep_subjects),4))+'%')
		ax1.legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])

		if len(structures[structure])>1:	
			right_control_patch = mpatches.Patch(color='r', label='control '+str(round(right_control_total/len(control_subjects),4))+'%')
			right_anxious_patch = mpatches.Patch(color='c', label='anxious '+str(round(right_anxious_total/len(anx_subjects),4))+'%')
			right_comorbid_patch = mpatches.Patch(color='m', label='comorbid '+str(round(right_comorbid_total/len(dep_and_anx_subjects),4))+'%')
			right_depressed_patch = mpatches.Patch(color='y', label='depressed '+str(round(right_depressed_total/len(dep_subjects),4))+'%')
			ax2.legend(handles=[right_control_patch,right_anxious_patch,right_comorbid_patch,right_depressed_patch])


		f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aseg/"+structure+"_compare",dpi=199)

		#box plot measures
		if len(structures[structure])>1:
			g, (boxes1,boxes2) = plt.subplots(nrows=1,ncols=2,figsize=(10,14))
			boxes1.set_title("Left " + structure)
			boxes2.boxplot(right_boxplot_data,labels=['control','anxious','comorbid','depressed'])
			boxes2.set_title("Right "+structure)
		else:
			g, boxes1 = plt.subplots(nrows=1,figsize=(10,14))	
			boxes1.set_title(structure)
		boxes1.boxplot(boxplot_data,labels=['control','anxious','comorbid','depressed'])
		plt.show()

		g.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aseg/"+structure+"_boxplot",dpi=199)
	else:
		print('must input valid structure') 
		print(structures)

def aseg_compare_bvolume(structure):

	if structure in structures.keys(): 
		if len(structures[structure])>1:
			f, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,14))
		else:
			f, ax1 = plt.subplots(nrows=1,figsize=(15,14))
		#f.tight_layout()
		#f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
				
		anatomy_label_1 = str(structures[structure][0]) 
		if len(structures[structure])>1:		
			anatomy_label_2 = str(structures[structure][1])  #right side
		
		#left side if bilateral
		control_total = 0
		anxious_total = 0
		comorbid_total = 0
		depressed_total = 0

		right_control_total = 0
		right_anxious_total = 0
		right_comorbid_total = 0
		right_depressed_total = 0

		#[control, anxious, comorbid, depressed]
		boxplot_data = [[],[],[],[]]
		right_boxplot_data = [[],[],[],[]]

		for s_index,s in enumerate(subjects):			
			brain="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/brain.mgz"
			aseg ="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/aseg.mgz"
			#print (s)
			#print (s_index)
			if os.path.isfile(brain) & os.path.isfile(aseg):
				vol=os.popen("mri_label_volume -b \\"+brain+" \\"+aseg+" " +anatomy_label_1).read()
				side= str(vol.split("\n")[2])
				side_percent = str(side.split(" ")[7])
				ax1.set_ylabel("percentage of b")
				ax1.set_xlabel('Subject Type')
				if len(structures[structure])>1:		
					vol=os.popen("mri_label_volume -b \\"+brain+" \\"+aseg+" " +anatomy_label_2).read()
					right_side= str(vol.split("\n")[2])
					right_side_percent = str(right_side.split(" ")[7])
					ax2.set_ylabel("percentage of b")
					ax2.set_xlabel('Subject Type')

				#color by subject type
				if s in control_subjects:
					ax1.plot(1+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='r')
					control_total += float(side_percent.strip('%'))

					boxplot_data[0].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:		
						ax2.plot(1+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='r')
						right_control_total += float(right_side_percent.strip('%'))
						right_boxplot_data[0].append(float(side_percent.strip('%')))
				elif s in anx_subjects:
					ax1.plot(1.5+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='c')
					anxious_total += float(side_percent.strip('%'))
					boxplot_data[1].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:
						ax2.plot(1.5+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='c')		
						right_anxious_total += float(right_side_percent.strip('%'))
						right_boxplot_data[1].append(float(side_percent.strip('%')))
				elif s in dep_and_anx_subjects:
					ax1.plot(2+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='m')
					comorbid_total += float(side_percent.strip('%'))
					boxplot_data[2].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:	
						ax2.plot(2+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='m')
						right_comorbid_total += float(right_side_percent.strip('%'))
						right_boxplot_data[2].append(float(side_percent.strip('%')))
				elif s in dep_subjects:
					ax1.plot(2.5+random.uniform(0,0.3), float(side_percent.strip('%')), "-o",c='y')
					depressed_total += float(side_percent.strip('%'))
					boxplot_data[3].append(float(side_percent.strip('%')))
					if len(structures[structure])>1:	
						ax2.plot(2.5+random.uniform(0,0.3), float(right_side_percent.strip('%')), "-o",c='y')	
						right_depressed_total += float(right_side_percent.strip('%'))
						right_boxplot_data[3].append(float(side_percent.strip('%')))

		ax1.set_ylim((0,1.2))
		ax1.set_title(structure)
		ax1.axes.get_xaxis().set_visible(False)

		if len(structures[structure])>1:
			ax2.set_ylim((0,1.2))
			ax1.set_title("Left "+structure)
			ax2.set_title("Right "+structure)
			ax2.axes.get_xaxis().set_visible(False)
		control_patch = mpatches.Patch(color='r', label='control '+str(round(control_total/len(control_subjects),4))+'%')
		anxious_patch = mpatches.Patch(color='c', label='anxious '+str(round(anxious_total/len(anx_subjects),4))+'%')
		comorbid_patch = mpatches.Patch(color='m', label='comorbid '+str(round(comorbid_total/len(dep_and_anx_subjects),4))+'%')
		depressed_patch = mpatches.Patch(color='y', label='depressed '+str(round(depressed_total/len(dep_subjects),4))+'%')
		ax1.legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])

		if len(structures[structure])>1:	
			right_control_patch = mpatches.Patch(color='r', label='control '+str(round(right_control_total/len(control_subjects),4))+'%')
			right_anxious_patch = mpatches.Patch(color='c', label='anxious '+str(round(right_anxious_total/len(anx_subjects),4))+'%')
			right_comorbid_patch = mpatches.Patch(color='m', label='comorbid '+str(round(right_comorbid_total/len(dep_and_anx_subjects),4))+'%')
			right_depressed_patch = mpatches.Patch(color='y', label='depressed '+str(round(right_depressed_total/len(dep_subjects),4))+'%')
			ax2.legend(handles=[right_control_patch,right_anxious_patch,right_comorbid_patch,right_depressed_patch])


		f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aseg_bvolume/"+structure+"_compare_bvolume",dpi=199)

		#box plot measures
		if len(structures[structure])>1:
			g, (boxes1,boxes2) = plt.subplots(nrows=1,ncols=2,figsize=(10,14))
			boxes1.set_title("Left " + structure)
			boxes2.boxplot(right_boxplot_data,labels=['control','anxious','comorbid','depressed'])
			boxes2.set_title("Right "+structure)
		else:
			g, boxes1 = plt.subplots(nrows=1,figsize=(10,14))	
			boxes1.set_title(structure)
		boxes1.boxplot(boxplot_data,labels=['control','anxious','comorbid','depressed'])

		g.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/aseg_bvolume/"+structure+"_boxplot_bvolume",dpi=199)
		#plt.show()
	else:
		print('must input valid structure') 
		print(structures)
'''
aparc_compare('Lateral and Medial Orbitofrontal')
aparc_compare('Precuneus')
aparc_compare('Insula')
aparc_compare('Caudal and Rostral Anterior Cingulate')
aparc_compare('Temporal Lobe')
aparc_compare('Parahippocampal')
aparc_compare('Rostral Middle Frontal')
aparc_compare('Superior Frontal')
'''

'''
aparc_compare_KSADS('Lateral and Medial Orbitofrontal')
aparc_compare_KSADS('Precuneus')
aparc_compare_KSADS('Insula')
aparc_compare_KSADS('Caudal and Rostral Anterior Cingulate')
aparc_compare_KSADS('Temporal Lobe')
aparc_compare_KSADS('Parahippocampal')
aparc_compare_KSADS('Rostral Middle Frontal')
aparc_compare_KSADS('Superior Frontal')

'''
#plot_structures(['Amygdala','Thalamus'])
plot_structures(structures.keys()) #'Thalamus','Amygdala','Caudate','Putamen','Accumbens','CC_Anterior','CC_Mid_Anterior','CC_Central', 'CC_Mid_Posterior', 'CC_Posterior', 'Optic Chiasm', 'Pons','Pallidum',  'Ventral DC','Choroid plexus'])
'''
aseg_compare_bvolume('Amygdala')

aseg_compare('Cerebellum - Cortex')
aseg_compare('Cerebellum - White Matter')

aseg_compare('Caudate')
aseg_compare('Putamen')
aseg_compare('Accumbens')
aseg_compare('Ventral DC')
aseg_compare('Choroid plexus')
aseg_compare('CC_Anterior')
aseg_compare('CC_Mid_Anterior')
aseg_compare('CC_Central')
aseg_compare('CC_Mid_Posterior')
aseg_compare('CC_Posterior')
aseg_compare('Optic Chiasm')
aseg_compare('Pons')
aseg_compare('Pallidum')
'''


