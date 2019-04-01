#/space/erebus/1/users/jwang/jon2/bin/python3.6 /space/erebus/1/users/jwang/plots_compare.py
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
from pylab import polyfit
from pylab import polyval
#import readClinical

subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015", "BANDA016", "BANDA017","BANDA018","BANDA019","BANDA020","BANDA021","BANDA022","BANDA023","BANDA024","BANDA025","BANDA026","BANDA027","BANDA028","BANDA029","BANDA030","BANDA031","BANDA032",
"BANDA033","BANDA034","BANDA035","BANDA036","BANDA037","BANDA038","BANDA039","BANDA040",
"BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049",
"BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060","BANDA061","BANDA062","BANDA063"]

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




def aparc_compare_MFQ():
	'''
	2 subplots (lh and rh)
	Each dot is subject
	y-axis cortical thickness
	x-axis MFQ total score
	color sorted by structure
	'''
	structures = {
'Lateral and Medial Orbitofrontal':[70, 72],
'Precuneus':[83],
'Insula':[93],
'Caudal and Rostral Anterior Cingulate': [61,84],
#'Temporal Lobe':[67, 73, 88, 60, 65, 91, 64, 92, 74],
#Temporal Lobe: Superior, Middle, and Inferior Temporal, Banks of the Superior Temporal Sulcus, Fusiform, Transverse Temporal, Entorhinal, Temporal Pole, Parahippocampal 
'Parahippocampal':[74],
'Rostral Middle Frontal':[85],
'Superior Frontal':[86]
}
	f, axarr = plt.subplots(nrows=1,ncols=2,figsize=(23,14))
	f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)

	#for calculating axis ranges
	min_value = 0
	max_value = 0
	xmin_value = 0
	xmax_value = 0


	x_ticks = []
	legends_patch_list = []
	for structure_index,structure in enumerate(structures):
			
		x_values = []
		lh_y_values = []
		rh_y_values = []
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

			#color assigned by structure
			csvfile = open('/space/erebus/1/users/jwang/MFQ_i.csv')
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['banda_id']==s:
					print (s)
					print (row['mfq_i_total'])
					print (lh_thickness)
					print (rh_thickness)
					print (rh_thickness)	
					print (str(structure_index%10))	
					x_values.append(int(row['mfq_i_total']))
					lh_y_values.append(lh_thickness)
					rh_y_values.append(rh_thickness)
					axarr[0].plot(int(row['mfq_i_total']), lh_thickness, "-o",markersize=5, color='C'+str(structure_index%10))
					axarr[1].plot(int(row['mfq_i_total']), rh_thickness, "-o",markersize=5, color ='C'+str(structure_index%10))
					if min_value == 0: min_value = lh_thickness
					min_value = min(min_value,lh_thickness,rh_thickness)					
					max_value = max(max_value,lh_thickness,rh_thickness)
					x_ticks.append(int(row['mfq_i_total']))
					if xmin_value == 0: xmin_value = int(row['mfq_i_total'])
					xmin_value = min(xmin_value,int(row['mfq_i_total']))					
					xmax_value = max(xmax_value,int(row['mfq_i_total']))
		legends_patch_list.append(mpatches.Patch(color='C'+str(structure_index%10), label=structure))
		(lh_m,lh_b) = polyfit(x_values,lh_y_values,1)
		lh_yp = polyval([lh_m,lh_b],x_values)
		axarr[0].plot(x_values,lh_yp,'-',color='C'+str(structure_index%10))		

		(rh_m,rh_b) = polyfit(x_values,rh_y_values,1)
		rh_yp = polyval([rh_m,rh_b],x_values)
		axarr[1].plot(x_values,rh_yp,'-',color='C'+str(structure_index%10))		

	axarr[0].set_ylabel("Global Mean Cortical Thickness")
	axarr[0].set_title("Left structures")
	axarr[0].set_xlabel("MFQ total score")

	axarr[1].set_ylabel("Global Mean Cortical Thickness")
	axarr[1].set_title("Right structures")
	axarr[1].set_xlabel("MFQ total score")

	#axarr[0].set_xticks(x_ticks)
	#axarr[1].set_xticks(x_ticks)
	#ax1.set_xticklabels(x_labels,rotation=45)
	#ax2.set_xticklabels(x_labels,rotation=45, ha="right")
	axarr[0].legend(handles=legends_patch_list)
	axarr[1].legend(handles=legends_patch_list)

	axarr[0].set_xlim(xmin_value-.30,xmax_value+.30)
	axarr[1].set_xlim(xmin_value-.30,xmax_value+.30)
	axarr[0].set_ylim(min_value-.30,max_value+.30)
	axarr[1].set_ylim(min_value-.30,max_value+.30)
	f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/MFQ_aparc_i_thickness_compare",dpi=199)	

	'''
	control_patch = mpatches.Patch(color='r', label='not present')
	probable_patch = mpatches.Patch(color='c', label='probable')
	definite_patch = mpatches.Patch(color='m', label='definite')
	ax1.legend(handles=[control_patch,probable_patch,definite_patch])
	ax2.legend(handles=[control_patch,probable_patch,definite_patch])
	print(len(disorders))
	'''



	
def aseg_compare_MFQ():
	'''
	2 subplots (lh and rh)
	Each dot is subject
	y-axis percent of eTV
	x-axis MFQ total score
	color sorted by structure
	'''
	structures = {
	'Lateral Ventricle':[4,43], 
	'Inferior Lateral Ventricle':[5,44], 
	'Thalamus':[10,49],
	'Caudate':[11,50],
	'Putamen':[12,51],
	'Pallidum':[13,52],
	'Hippocampus':[17,53],
	'Amygdala':[18,54],
	'Accumbens':[26,58],
	'Brain Stem':[16],
	'CC_Mid_Anterior':[254],
	'CC_Anterior':[255],
	'Pons':[174]
	}

	f, axarr = plt.subplots(nrows=2,ncols=2,figsize=(23,14))
	f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)


	#for calculating axis ranges
	min_value = 0
	max_value = 0
	min_value2 = 0
	max_value2 = 0
	xmin_value = 0
	xmax_value = 0


	x_ticks = []
	legends_patch_list = []
	legends_patch_list_2 = []
	for structure_index,structure in enumerate(structures):
			
		x_values = []
		lh_y_values = []
		rh_y_values = []
		x_values2 = []		
		y_values2 = []

		anatomy_label_1 = str(structures[structure][0]) 
		if len(structures[structure])>1:		
			anatomy_label_2 = str(structures[structure][1])  #right side


		for s_index,s in enumerate(subjects):	
			talairach="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/transforms/talairach.xfm"
			aseg ="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/aseg.mgz"
			print (s)
			print (s_index)
			if os.path.isfile(talairach) & os.path.isfile(aseg):
				vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" " +anatomy_label_1).read()
				side= str(vol.split("\n")[2])
				side_percent = str(side.split(" ")[7])
				if len(structures[structure])>1:		
					vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" "+anatomy_label_2).read()
					right_side= str(vol.split("\n")[2])
					right_side_percent = str(right_side.split(" ")[7])

			#color assigned by structure
			csvfile = open('/space/erebus/1/users/jwang/MFQ_i.csv')
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['banda_id']==s:


					if structure_index>=9:
						x_values2.append(int(row['mfq_i_total']))
						print(x_values2)
						y_values2.append(float(side_percent.strip('%')))
						axarr[1,0].plot(int(row['mfq_i_total']), float(side_percent.strip('%')), "-o",markersize=5, color='C'+str(structure_index%10))
						
						if min_value2 == 0: min_value2 = float(side_percent.strip('%'))
						min_value2 = min(min_value,float(side_percent.strip('%')))					
						max_value2 = max(max_value,float(side_percent.strip('%')))

					else:
						x_values.append(int(row['mfq_i_total']))
						lh_y_values.append(float(side_percent.strip('%')))
						if len(structures[structure])>1: rh_y_values.append(float(right_side_percent.strip('%')))
						axarr[0,0].plot(int(row['mfq_i_total']), float(side_percent.strip('%')), "-o",markersize=5, color='C'+str(structure_index%10))
						axarr[0,1].plot(int(row['mfq_i_total']), float(right_side_percent.strip('%')), "-o",markersize=5, color ='C'+str(structure_index%10))

						if min_value == 0: min_value = float(side_percent.strip('%'))
						min_value = min(min_value,float(side_percent.strip('%')),float(right_side_percent.strip('%')))					
						max_value = max(max_value,float(side_percent.strip('%')),float(right_side_percent.strip('%')))
					x_ticks.append(int(row['mfq_i_total']))
					if xmin_value == 0: xmin_value = int(row['mfq_i_total'])
					xmin_value = min(xmin_value,int(row['mfq_i_total']))					
					xmax_value = max(xmax_value,int(row['mfq_i_total']))

		
		if structure_index>=9:
			(lh_m,lh_b) = polyfit(x_values2,y_values2,1)
			lh_yp = polyval([lh_m,lh_b],x_values2)
			axarr[1,0].plot(x_values2,lh_yp,'-',color='C'+str(structure_index%10))	
			legends_patch_list_2.append(mpatches.Patch(color='C'+str(structure_index%10), label=structure))
		else:		
			(lh_m,lh_b) = polyfit(x_values,lh_y_values,1)
			lh_yp = polyval([lh_m,lh_b],x_values)
			axarr[0,0].plot(x_values,lh_yp,'-',color='C'+str(structure_index%10))		
			(rh_m,rh_b) = polyfit(x_values,rh_y_values,1)
			rh_yp = polyval([rh_m,rh_b],x_values)
			axarr[0,1].plot(x_values,rh_yp,'-',color='C'+str(structure_index%10))	
			legends_patch_list.append(mpatches.Patch(color='C'+str(structure_index%10), label=structure))	
		


	axarr[0,0].set_ylabel("Percent of eTV")
	axarr[0,0].set_title("Left structures")
	axarr[0,0].set_xlabel("MFQ total score")

	axarr[0,1].set_ylabel("Percent of eTV")
	axarr[0,1].set_title("Right structures")
	axarr[0,1].set_xlabel("MFQ total score")

	#axarr[0].set_xticks(x_ticks)
	#axarr[1].set_xticks(x_ticks)
	#ax1.set_xticklabels(x_labels,rotation=45)
	#ax2.set_xticklabels(x_labels,rotation=45, ha="right")
	axarr[0,0].legend(handles=legends_patch_list)
	axarr[0,1].legend(handles=legends_patch_list)
	axarr[1,0].legend(handles=legends_patch_list_2)
	axarr[1,0].set_title("Structures")
	axarr[1,0].set_xlabel("MFQ total score")

	#axarr[0].set_xlim(xmin_value-.30,xmax_value+.30)
	#axarr[1].set_xlim(xmin_value-.30,xmax_value+.30)
	axarr[0,0].set_ylim(min_value-.30,max_value+.30)
	axarr[0,1].set_ylim(min_value-.30,max_value+.30)
	
	f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/MFQ_aseg_i_thickness_compare",dpi=199)	
	plt.show()
	'''
	control_patch = mpatches.Patch(color='r', label='not present')
	probable_patch = mpatches.Patch(color='c', label='probable')
	definite_patch = mpatches.Patch(color='m', label='definite')
	ax1.legend(handles=[control_patch,probable_patch,definite_patch])
	ax2.legend(handles=[control_patch,probable_patch,definite_patch])
	print(len(disorders))
	'''

	


#aparc_compare_MFQ()
aseg_compare_MFQ()


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


#plot_structures(['Amygdala','Thalamus'])
#plot_structures(structures.keys()) #'Thalamus','Amygdala','Caudate','Putamen','Accumbens','CC_Anterior','CC_Mid_Anterior','CC_Central', 'CC_Mid_Posterior', 'CC_Posterior', 'Optic Chiasm', 'Pons','Pallidum',  'Ventral DC','Choroid plexus'])



