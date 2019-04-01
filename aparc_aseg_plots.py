#/space/erebus/1/users/jwang/jon2/bin/python3.6 aparc_aseg_plots.py

'''
Functions:

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
import utils
from nipy.modalities.fmri.glm import GeneralLinearModel

#import readClinical
matplotlib.rcParams.update({'font.size': 18})
def aparc_measures():
	'''
	2 subplots (lh and rh_volume)
	Each dot is subject
	y-axis cortical thickness or volume
	x-axis MFQ total score
	color sorted by structure
	'''
	structures = {
'Medial Orbitofrontal':[72],
'Caudal Anterior Cingulate': [61],
'Rostral Anterior Cingulate': [84],
#'Temporal Lobe':[67, 73, 88, 60, 65, 91, 64, 92, 74],
#Temporal Lobe: Superior, Middle, and Inferior Temporal, Banks of the Superior Temporal Sulcus, Fusiform, Transverse Temporal, Entorhinal, Temporal Pole, Parahippocampal 
'Rostral Middle Frontal':[85],
'Caudal Middle Frontal': [62],
'Superior Frontal':[86],
'Parahippocampal':[74],
'Posterior Cingulate': [81],
'Precuneus':[83],
'Insula':[93],
'Fusiform': [65]
}
	outliers=["BANDA069","BANDA070", "BANDA071", "BANDA089","BANDA090"]#["BANDA071", "BANDA070","BANDA005","BANDA045"]
	subjects, sex, scores = utils.loadBANDA(outliers)


	for measurement in (['thickness','volume']):
		output=csv.writer(open('/space/erebus/1/users/data/scores/aparc_output_'+measurement+'.csv','w+'))
		output.writerow(['subject','structure','left_'+measurement,'right_'+measurement,'questionnaire','questionnaire_score'])
		for key, score in scores.items():
			f, axarr = plt.subplots(nrows=1,ncols=2,figsize=(23,14))
			f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)

			#for calculating axis ranges
			min_value = 0
			max_value = 0
			xmin_value = 0
			xmax_value = 0

			legends_patch_list = []
			GLM_x=np.array([])
			GLM_y=np.array([])
			print (key)
			print (score)
			for structure_index,structure in enumerate(structures):
			
				x_values = []
				lh_y_values = []
				rh_y_values = []
				for s_index,s in enumerate(subjects):	
					if structure_index==0:
						if key=='Anhedonia':
							if score[s_index]>=3:
								GLM_x=np.append(GLM_x,[[1,0]])	
							else:
								GLM_x=np.append(GLM_x,[[0,1]])	
						else:
							GLM_x=np.append(GLM_x,[[1,score[s_index]]])
					#print (s)
					lh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/lh.aparc.stats')
					rh_parc_file = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/stats/rh.aparc.stats')


					lh_measurement=0
					rh_measurement=0
					#print (key)
					#print (s)
					#print (structure)
					#print (rh_parc_file)
					for i in structures[structure]:
						lh_list = open(lh_parc_file[0],'r').readlines()[i].split()
						rh_list = open(rh_parc_file[0],'r').readlines()[i].split()
					
						#StructName NumVert SurfArea GrayVol ThickAvg ThickStd MeanCurv GausCurv FoldInd CurvInd

						#Global Mean Cortical Thickness weighted by Surface Area
						#bh.thickness = ( (lh.thickness * lh.surfarea) + (rh_volume.thickness * rh_volume.surfarea) ) / (lh.surfarea + rh_volume.surfarea) 
						#thickness += (  ( ( float(lh_list[4])*float(lh_list[2]) )+ ( float(rh_list[4])*float(rh_list[2]) ) ) / (float(lh_list[2]) + float(rh_list[2]) ) )/(structures[structure].index(i)+1)
						if measurement == 'thickness': 
							lh_measurement += float(lh_list[4])
							rh_measurement += float(rh_list[4])
						else: 
							lh_measurement += float(lh_list[3])
							rh_measurement += float(rh_list[3])
						if structures[structure].index(i) == len(structures[structure])-1:
							lh_measurement == lh_measurement/ len(structures[structure])
							rh_measurement == rh_measurement/ len(structures[structure])

					#color assigned by structure
					x_values.append(float(score[s_index]))
					lh_y_values.append(lh_measurement)
					rh_y_values.append(rh_measurement)
					output.writerow([s,structure,lh_measurement,rh_measurement,key,score[s_index]])
					axarr[0].plot(float(score[s_index]), lh_measurement, "-o",markersize=5, color='C'+str(structure_index%10))
					axarr[1].plot(float(score[s_index]), rh_measurement, "-o",markersize=5, color ='C'+str(structure_index%10))
					if s_index == 0: min_value = lh_measurement
					min_value = min(min_value,lh_measurement,rh_measurement)					
					max_value = max(max_value,lh_measurement,rh_measurement)

					if s_index == 0: xmin_value = float(score[s_index])
					xmin_value = min(xmin_value,float(score[s_index]))					
					xmax_value = max(xmax_value,float(score[s_index]))
				legends_patch_list.append(mpatches.Patch(color='C'+str(structure_index%10), label=structure))

				#regression lines
				(lh_m,lh_b) = polyfit(x_values,lh_y_values,1)
				lh_yp = polyval([lh_m,lh_b],x_values)
				axarr[0].plot(x_values,lh_yp,'-',color='C'+str(structure_index%10))		

				(rh_m,rh_b) = polyfit(x_values,rh_y_values,1)
				rh_yp = polyval([rh_m,rh_b],x_values)
				axarr[1].plot(x_values,rh_yp,'-',color='C'+str(structure_index%10))		
				if len(GLM_y)==0:
					GLM_y = lh_y_values
				else:
					GLM_y =np.vstack((GLM_y,[lh_y_values]))
		
				GLM_y =np.vstack((GLM_y,[rh_y_values]))

			GLM_y= GLM_y.transpose()
			print(np.shape(GLM_y))
			GLM_x= np.array(GLM_x).reshape(len(GLM_y),2)
			GLM_y=np.array(GLM_y)
		
			if key !='Anhedonia':     
				cval = np.hstack((0, -1))
			else:
				cval = np.hstack((1, -1))
	
			model = GeneralLinearModel(GLM_x)
			model.fit(GLM_y)
			p_vals = model.contrast(cval).p_value() # z-transformed statistics
			print(key, "+", p_vals)
		
			z_vals = model.contrast(cval*-1).p_value() # z-transformed statistics
			print(key,"-", p_vals)
		
			axarr[0].set_ylabel("Global Mean Cortical Thickness")
			axarr[0].set_title("Left structures")
			axarr[0].set_xlabel(key)

			axarr[1].set_ylabel("Global Mean Cortical Thickness")
			axarr[1].set_title("Right structures")
			axarr[1].set_xlabel(key)

			axarr[0].legend(handles=legends_patch_list)
			axarr[1].legend(handles=legends_patch_list)

			axarr[0].set_xlim(xmin_value-.30,xmax_value+.30)
			axarr[1].set_xlim(xmin_value-.30,xmax_value+.30)
			axarr[0].set_ylim(min_value-.30,max_value+.30)
			axarr[1].set_ylim(min_value-.30,max_value+.30)

			f.savefig("/space/erebus/1/users/data/comparisonPlots_1_114/aparc_"+measurement+"_"+str(key),dpi=199)	
		#plt.show()




	
def aseg_measures(premade_output = None):
	'''
	2 subplots (lh and rh_volume)
	Each dot is subject
	y-axis percent of eTV
	x-axis MFQ total score
	color sorted by structure
	'''
	structures = {
	'Thalamus':[10,49],
	'Caudate':[11,50],
	'Putamen':[12,51],
	'Pallidum':[13,52],
	'Amygdala':[18,54],
	'Hippocampus':[17,53],
	'Accumbens':[26,58],
	'Brain Stem':[16],
	'CC_Mid_Anterior':[254],
	'CC_Anterior':[255],
	'Pons':[174],
	'Lateral Ventricle':[4,43], 
	'Inferior Lateral Ventricle':[5,44]
	}

	f, axarr = plt.subplots(nrows=2,ncols=2,figsize=(23,14))
	f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)
	outliers=["BANDA069","BANDA070", "BANDA071", "BANDA089","BANDA090"]


#"BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015", "BANDA016", "BANDA017","BANDA018","BANDA019","BANDA020","BANDA021","BANDA022","BANDA023","BANDA024","BANDA025","BANDA026","BANDA027","BANDA028","BANDA029","BANDA030","BANDA031","BANDA032",
#"BANDA033","BANDA034","BANDA035","BANDA036","BANDA037","BANDA038","BANDA039","BANDA040",
#"BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049",
#"BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060", "BANDA061", "BANDA062", "BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA089","BANDA090"]
	subjects, sex, scores = utils.loadBANDA(outliers)
	if premade_output == None:
		output=csv.writer(open('/space/erebus/1/users/data/scores/aseg_output.csv','w+'))
		output.writerow(['subject','structure','left (or bilateral)','right','questionnaire','questionnaire_score'])	
	for key, score in scores.items():
		f, axarr = plt.subplots(nrows=2,ncols=2,figsize=(23,14))
		f.subplots_adjust(left=.03, bottom=.04, right=.98, top=.97, wspace=.18, hspace=.30)

		#for calculating axis ranges
		min_value = 0
		max_value = 0
		min_value2 = 0
		max_value2 = 0
		xmin_value = 0
		xmax_value = 0

		legends_patch_list = []
		legends_patch_list_2 = []
		GLM_x=np.array([])
		GLM_y=np.array([])
		

		for structure_index,structure in enumerate(structures):
		
			x_values = []
			lh_y_values = []
			rh_y_values = []
			x_values2 = []		
			y_values2 = []
			anatomy_label_1 = str(structures[structure][0]) 
			if len(structures[structure])>1:		
				anatomy_label_2 = str(structures[structure][1])  #right volume

			
			for s_index,s in enumerate(subjects):
				#print(structure_index)
				if structure_index==0:
					if key=='Anhedonia':
						if score[s_index]>=3:
							GLM_x=np.append(GLM_x,[[1,0]])	
						else:
							GLM_x=np.append(GLM_x,[[0,1]])	
					else:
						GLM_x=np.append(GLM_x,[[1,score[s_index]]])
				#print (key)
				#print (s)
				#print (structure)	
				
				current_y = 0
				current_rh_y = 0

				if premade_output == None:
					talairach="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/transforms/talairach.xfm"
					aseg ="/space/erebus/1/users/data/preprocess/FS/MGH_HCP/"+s+"/mri/aseg.mgz"

					if os.path.isfile(talairach) & os.path.isfile(aseg):
						vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" " +anatomy_label_1).read()
						volume= str(vol.split("\n")[2])
						percent = str(volume.split(" ")[7])
						current_y = float(percent.strip('%'))
						if len(structures[structure])>1:		
							vol=os.popen("mri_label_volume -eTIV \\"+talairach+" 1948 \\"+aseg+" "+anatomy_label_2).read()
							rh_volume= str(vol.split("\n")[2])
							rh_percent = str(rh_volume.split(" ")[7])
							current_rh_y = float(rh_percent.strip('%'))

				else:
					with open('/space/erebus/1/users/data/scores/aseg_output.csv', 'r') as output:
						output_reader = csv.DictReader(output, delimiter = ",")
						for row in output_reader:
							if row['structure']==structure and row['subject']== s:
								current_y = float(row['left (or bilateral)'])
								if len(structures[structure])>1: current_rh_y = float(row['right'])
								break

				#color assigned by structure
				if structure_index>=9:
					x_values2.append(float(score[s_index]))
					y_values2.append(current_y)
					
					if premade_output==None: 
							output.writerow([s,structure,current_y,key,float(score[s_index])])	
					axarr[1,0].plot(float(score[s_index]), current_y, "-o",markersize=5, color='C'+str(structure_index%10))
			
					if min_value2 == 0: min_value2 = current_y
					min_value2 = min(min_value,current_y)					
					max_value2 = max(max_value,current_y)

				else:
					x_values.append(float(score[s_index]))
					lh_y_values.append(current_y)
					if len(structures[structure])>1: rh_y_values.append(current_rh_y)

					if premade_output==None: 
						output.writerow([s,structure,current_y,current_rh_y,key,float(score[s_index])])	
					axarr[0,0].plot(float(score[s_index]), current_y, "-o",markersize=5, color='C'+str(structure_index%10))
					axarr[0,1].plot(float(score[s_index]), current_rh_y, "-o",markersize=5, color ='C'+str(structure_index%10))

					if s_index == 0: min_value = current_y
					min_value = min(min_value,current_y,current_rh_y)					
					max_value = max(max_value,current_y,current_rh_y)

				if s_index == 0: xmin_value = float(score[s_index])
				xmin_value = min(xmin_value,float(score[s_index]))					
				xmax_value = max(xmax_value,float(score[s_index]))

			#regression lines
			if structure_index>=9:
				(lh_m,lh_b) = polyfit(x_values2,y_values2,1)
				lh_yp = polyval([lh_m,lh_b],x_values2)
				axarr[1,0].plot(x_values2,lh_yp,'-',color='C'+str(structure_index%10))	
				legends_patch_list_2.append(mpatches.Patch(color='C'+str(structure_index%10), label=structure))
				
				GLM_y =np.vstack((GLM_y,[y_values2]))

			else:		
				(lh_m,lh_b) = polyfit(x_values,lh_y_values,1)
				lh_yp = polyval([lh_m,lh_b],x_values)
				axarr[0,0].plot(x_values,lh_yp,'-',color='C'+str(structure_index%10))		
				(rh_m,rh_b) = polyfit(x_values,rh_y_values,1)
				rh_yp = polyval([rh_m,rh_b],x_values)
				axarr[0,1].plot(x_values,rh_yp,'-',color='C'+str(structure_index%10))	
				legends_patch_list.append(mpatches.Patch(color='C'+str(structure_index%10), label=structure))	
				if len(GLM_y)==0:
					GLM_y = lh_y_values
				else:
					GLM_y =np.vstack((GLM_y,[lh_y_values]))
			
				GLM_y =np.vstack((GLM_y,[rh_y_values]))
			
		GLM_y= GLM_y.transpose()
		print(np.shape(GLM_y))
		GLM_x= np.array(GLM_x).reshape(len(GLM_y),2)
		GLM_y=np.array(GLM_y)
		
		if key !='Anhedonia':     
			cval = np.hstack((0, -1))
		else:
			cval = np.hstack((1, -1))
	
		model = GeneralLinearModel(GLM_x)
		model.fit(GLM_y)
		p_vals = model.contrast(cval).p_value() # z-transformed statistics
		print(key,"+", p_vals)
		
		
		p_vals = model.contrast(cval*-1).p_value() # z-transformed statistics
		print(key,"-", p_vals)
		
		axarr[0,0].set_ylabel("Percent of eTV")
		axarr[0,0].set_title("Left structures")
		axarr[0,0].set_xlabel(key)

		axarr[0,1].set_ylabel("Percent of eTV")
		axarr[0,1].set_title("Right structures")
		axarr[0,1].set_xlabel(key)

		axarr[0,0].legend(handles=legends_patch_list)
		axarr[0,1].legend(handles=legends_patch_list)
		axarr[1,0].legend(handles=legends_patch_list_2)
		axarr[1,0].set_title("Structures")
		axarr[1,0].set_xlabel(key)

		axarr[0,0].set_ylim(min_value-.30,max_value+.30)
		axarr[0,1].set_ylim(min_value-.30,max_value+.30)




	
		f.savefig("/space/erebus/1/users/data/comparisonPlots_1_114/aseg_"+key,dpi=199)	
	plt.show()
aparc_measures()
aseg_measures()

