#/space/erebus/1/users/jwang/jon2/bin/python3.6 motion_snr_plots_v3.py

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

from numpy import linalg as LA
from pyquaternion import Quaternion
import matplotlib.patches as mpatches
import csv
from nipy.modalities.fmri.glm import GeneralLinearModel

outliers=["BANDA051","BANDA104","BANDA131","BANDA134","BANDA129","BANDA137"]
output="/space/erebus/1/users/data/scores/new2"

matplotlib.rcParams.update({'font.size': 18})

def readVNavsScoreFiles(s,t):

	f = open("/space/erebus/1/users/data/preprocess/"+s+"/motion/vnavs"+t+"Score.csv", 'r')
	if t=="T1":
		num=166
	else:
		num=111

	a = map(float, f.read().split(",") )
	li=[]
	li.extend(a)
	scores = li[:num]
	#print (scores)
	indices = np.array(range(num))
	for i in range(num,len(li)) :
		#print (np.argmax(scores), max(scores))
		index= np.argmax(scores)
		val = max(scores)
		if scores[index] > li[i]:
			scores[index] = li[i]
			indices[index]=i

	#print(indices)
	#print(sum(indices>166))
	return indices

def getValues(inFile, xColumn,lineIndex, acq_time,ref):
	prevValues =[]
	volumes=1
	tra = [0,0,0]
	absol = [0,0,0]
	linei=0
	iind=0
	with open(inFile) as motionFile:
		for line in motionFile:
			if linei >= lineIndex[0] and linei <lineIndex[len(lineIndex)-1] :

				values =  line.split()
				if len(prevValues )>5:
					t=0
					for i in range(xColumn, xColumn+3):
						if linei == lineIndex[iind]:
							tra[i-xColumn] += math.fabs(float(values[i])-float(prevValues[i]))

					volumes +=1
				if linei==ref or ref<0:
					prevValues = values
				if linei==lineIndex[0]:
					for i in range(xColumn, xColumn+3):
						absol[i-xColumn]= float(values[i])
				iind+=1
			if len(lineIndex) == iind:
				break
			linei+=1
	return (tra, volumes*acq_time, absol)

def getTranslation(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None):

	tra = getValues( inFile,xColumn,lineIndex,acq_time,ref)
	tra2=[0,0,0]
	if not inFile2 ==None :
		tra2 = getValues( inFile2,xColumn,lineIndex2,acq_time,ref)
		res = np.array(tra[2]) - np.array(tra2[2])
	else:
		res= np.array(tra[0])/tra[1]



	return math.sqrt(sum(res**2)) #/tra[1]

def getRotation(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None):
	col= 0 if xColumn == 3 else 3

	rot =getValues(inFile,col,lineIndex,acq_time,ref)
	rot2=[0,0,0]
	if not inFile2 ==None :
		rot2 = getValues( inFile2,col,lineIndex2,acq_time,ref)
		res = np.absolute(np.array(rot[2]) - np.array(rot2[2]))
	else:
		res= np.array(rot[0])/rot[1]

	return (sum(res*180/3.15)%180) #/rot[1]

def getTranslationAbsolute(inFile, xColumn,lineIndex,acq_time,ref=0):
	return getTranslation( inFile,xColumn,lineIndex,acq_time,ref)

def getRotationAbsolute(inFile, xColumn,lineIndex,acq_time,ref=0):
	return getRotation(inFile,xColumn,lineIndex,acq_time,ref)

def getFileData(fileN):
	if "dMRI" in fileN:
		column =0
		acq_time=3.230
	else:
		column =3
		acq_time=.8
	return column, acq_time

def getFilePath(fileN,s):
	f = "/space/erebus/1/users/data/preprocess/"+s+"/"+fileN
	if not os.path.isfile(f):
		f = "/space/erebus/1/users/data/preprocess/"+s+"/CMRR/"+fileN

	if os.path.isfile(f):
		return f
	else:
		return None

def motionWithin_measures():
	studies = {'Diffusion1': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion2': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion3': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion4':
	'dMRI_topup_eddy.nii.gz.eddy_parameters','Rest1': 'fMRI_rest1_AP_motion.nii.gz.par','Rest2': 'fMRI_rest2_PA_motion.nii.gz.par','Rest3': 'fMRI_rest3_AP_motion.nii.gz.par','Rest4':
	'fMRI_rest4_PA_motion.nii.gz.par', 'Gambling1' : 'tfMRI_gambling1_AP_motion.nii.gz.par','Gambling2' : 'tfMRI_gambling2_PA_motion.nii.gz.par','FaceMatching1' :
	'tfMRI_faceMatching1_AP_motion.nii.gz.par','FaceMatching2' :
	'tfMRI_faceMatching2_PA_motion.nii.gz.par','Conflict1':'tfMRI_conflict1_AP_motion.nii.gz.par','Conflict2':'tfMRI_conflict2_PA_motion.nii.gz.par','Conflict3':'tfMRI_conflict3_AP_motion.nii.gz.par',
	'Conflict4':'tfMRI_conflict4_PA_motion.nii.gz.par', 'T1':'motion/T1_motion.nii.gz.par','T2':'motion/T2_motion.nii.gz.par'}

	scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4'] #,'Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1','T2']
	#scans.append("T1 all vnavs - no reacq")
	#scans.append("T2 all vnavs - no reacq")
	#scans=['T2']
	diffusion=[ [0,98], [98,196],[196,295],[295,394]]

	metric = [getTranslation, getRotation] #, getTranslationAbsolute, getRotationAbsolute]
	metric_label=["Translation (mm/s)" , "Rotation ($\degree/s$)", "Absolute translation per second", "Absolute rotation per second"]

	indexPerDiffusion = {'Diffusion1':[0,98], 'Diffusion2':[98,196], 'Diffusion3':[196,295],'Diffusion4':[295,394]}
	fmri_order = {'Rest1':0,'Rest2':1,'Rest3':2,'Rest4':3,'Gambling1':4,'Gambling2':5, 'FaceMatching1':6,'FaceMatching2':7, 'Conflict1':8,'Conflict2':9,'Conflict3':10,'Conflict4':11}

	subjects, sex, scores = utils.loadBANDA140(outliers)

	motionWithin_output=csv.writer(open('/space/erebus/1/users/data/scores/new2/motionWithin_avg_output_rjj020419.csv','w+'))
	motionWithin_output.writerow(['subject','rot_trans','avg_score','questionnaire','questionnaire_score'])

	for key, score in scores.items():

		print (scans)
		f, axarr = plt.subplots(1, 2,figsize=(23,14))
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.28)

		trans_boxplot_data = [[],[]]
		rotat_boxplot_data = [[],[]]

		anhedonia = 0
		anhedonia_no = 0

		#box plot measures
		g, (boxes1,boxes2) = plt.subplots(nrows=1,ncols=2,figsize=(15,14))

		for i,met in enumerate(metric):
			axarr[i].set_title(str(met)[13:18])
			if str(met)[13:18]=='Trans': boxes1.set_title(str(met)[13:18])
			elif str(met)[13:18]=='Rotat': boxes2.set_title(str(met)[13:18])
			#for calculating axis ranges
			ymin_value = 0
			ymax_value = 0
			xmin_value = 0
			xmax_value = 0

			x_values = []
			y_values = []
			#for s in subjects:
			for s_index,s in enumerate(subjects):
				t_accumulate = 0

				for name in scans:
					fileN = studies[name.split()[0]]

					column,acq_time = getFileData(fileN)
					if "no vnavs" in name:
						if "T1" in name :
							index=[0,166]
						else:
							index=[0,111]
					else:
						index=[0,1000]
					if "dMRI" in fileN:
						index =diffusion[i]
					filePath = getFilePath(fileN,s)

						#print(i,j)
						#print(name)
					if filePath != None :
						#print (name)
						if "T1" == name:
							ind = readVNavsScoreFiles(s, "T1")
						elif "T2" == name:
							ind = readVNavsScoreFiles(s, "T2")
							#print(s, ind)
						else:
							ind = range(index[0], index[1])

						t=  met(filePath,column,np.sort(ind),acq_time)
						t_accumulate += t

				avg_t = t_accumulate/len(scans)

				if s_index == 0: ymin_value = avg_t
				ymin_value = min(ymin_value,avg_t)
				ymax_value = max(ymax_value,avg_t)

				if s_index == 0: xmin_value = float(score[s_index])
				xmin_value = min(xmin_value,float(score[s_index]))
				xmax_value = max(xmax_value,float(score[s_index]))

				if str(str(key))=='Anhedonia':
					if str(met)[13:18]=='Trans':
						if float(score[s_index])<3:
							trans_boxplot_data[0].append(avg_t)
							anhedonia_no += 1
						else:
							trans_boxplot_data[1].append(avg_t)
							anhedonia += 1
					if str(met)[13:18]=='Rotat':

						if float(score[s_index])<3: rotat_boxplot_data[0].append(avg_t)
						else: rotat_boxplot_data[1].append(avg_t)

				motionWithin_output.writerow([s,metric_label[metric.index(met)],avg_t,key,float(score[s_index])])
				axarr[i].plot(float(score[s_index]),avg_t,"o",markersize=5, color='m')

				x_values.append(float(score[s_index]))
				y_values.append(avg_t)
			#regression lines
			(sl,b) = polyfit(x_values,y_values,1)
			yp = polyval([sl,b],x_values)
			axarr[i].plot(x_values,yp,'-',color='r')
			#GLM
			X=np.array([])
			if key != 'Anhedonia':
				X  = np.ones(len(x_values))
				X =np.stack((X, x_values), axis=-1)
				cval = np.hstack((0, -1))
			else:
				for x in x_values:
					if x>=3:
						X=np.append(X,[[1,0]])
					else:
						X=np.append(X,[[0,1]])
				cval = np.hstack((1, -1))
			X= np.array(X).reshape(len(y_values),2)
			Y=np.array(y_values )

			model = GeneralLinearModel(X)
			model.fit(Y)
			z_vals = model.contrast(cval).p_value() # z-transformed statistics
			print(key, z_vals)

			axarr[i].set_ylabel("Average" + str(metric_label[metric.index(met)]))
			axarr[i].set_xlabel(str(key))

			axarr[i].set_xlim(xmin_value-(np.median(x_values)*.30),xmax_value+(np.median(x_values)*.30))
			axarr[i].set_ylim(ymin_value-(np.median(y_values)*.30),ymax_value+(np.median(y_values)*.30))

			if str(key)=='Anhedonia':
				if i==0:
					trans_box_max_list = [ max(a) for a in trans_boxplot_data]
					trans_box_min_list = [ min(a) for a in trans_boxplot_data]
					boxes1.set_ylabel("Average " + str(metric_label[metric.index(met)]))
					boxes1.set_xlabel(str(key))
				elif i==1:
					rotat_box_max_list = [ max(a) for a in rotat_boxplot_data]
					rotat_box_min_list = [ min(a) for a in rotat_boxplot_data]
					boxes2.set_ylabel("Average " + str(metric_label[metric.index(met)]))
					boxes2.set_xlabel(str(key))
		#f.savefig("/space/erebus/1/users/data/comparisonPlots_1_88/plots/motion_snr/motionWithin_avg_"+str(key),dpi=199)
		f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/motion_Within_avg_"+str(key),dpi=199)

	if str(str(key))=='Anhedonia':
		boxes1.set_ylim(0,max(trans_box_max_list)+.25)
		boxes2.set_ylim(0,max(rotat_box_max_list)+.25)


		#print(trans_boxplot_data[0])
		#print(trans_boxplot_data[1])
		boxes1.boxplot(trans_boxplot_data,labels=['no anhedonia','anhedonia'])
		boxes2.boxplot(rotat_boxplot_data,labels=['no anhedonia','anhedonia'])
		g.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/motion_Within_avg_Anhedonia"+"_boxplot",dpi=199)
		#g.savefig("/space/erebus/1/users/vsiless/QA_plots//motion_Within_avg_Anhedonia"+"_boxplot",dpi=199)
		print(anhedonia)
		print(anhedonia_no)
		#plt.show()

def motionBetween_measures():

	studies = {'Diffusion1': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion2': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion3': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion4':
	'dMRI_topup_eddy.nii.gz.eddy_parameters','Rest1': 'fMRI_rest1_AP_motion.nii.gz.par','Rest2': 'fMRI_rest2_PA_motion.nii.gz.par','Rest3': 'fMRI_rest3_AP_motion.nii.gz.par','Rest4':
	'fMRI_rest4_PA_motion.nii.gz.par', 'Gambling1' : 'tfMRI_gambling1_AP_motion.nii.gz.par','Gambling2' : 'tfMRI_gambling2_PA_motion.nii.gz.par','FaceMatching1' :
	'tfMRI_faceMatching1_AP_motion.nii.gz.par','FaceMatching2' :
	'tfMRI_faceMatching2_PA_motion.nii.gz.par','Conflict1':'tfMRI_conflict1_AP_motion.nii.gz.par','Conflict2':'tfMRI_conflict2_PA_motion.nii.gz.par','Conflict3':'tfMRI_conflict3_AP_motion.nii.gz.par',
	'Conflict4':'tfMRI_conflict4_PA_motion.nii.gz.par', 'T1':'motion/T1_motion.nii.gz.par','T2':'motion/T2_motion.nii.gz.par'}

	scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4','Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1',
	'T2']

	metric = [getTranslation, getRotation] #, getTranslationAbsolute, getRotationAbsolute]
	metric_label=["Translation (mm/s)" , "Rotation ($\degree/s$)", "Absolute translation per second", "Absolute rotation per second"]

	pairsOfStudies = {'Diffusion1':'Diffusion2','Diffusion2':'Diffusion3','Diffusion3':'Diffusion4',
	'Rest1':'Rest2','Rest2':'Rest3','Rest3':'Rest4','Gambling1':'Gambling2','FaceMatching1':'FaceMatching2','Conflict1':'Conflict2','Conflict2':'Conflict3', 'Conflict3':'Conflict4'}
	pairsOfStudies=[('Diffusion1','Diffusion2'),('Diffusion2','Diffusion3'),('Diffusion3','Diffusion4'),('Rest1','Rest2'),('Rest2','Rest3'),('Rest3','Rest4'),('T1','T2'),('Gambling1','Gambling2'),(
	'FaceMatching1', 'FaceMatching2'),('Conflict1','Conflict2'),('Conflict2','Conflict3'), ('Conflict3','Conflict4')]

	diffusion=[ [0,98], [98,196],[196,295],[295,394]]
	indexPerDiffusion = {'Diffusion1':[0,98], 'Diffusion2':[98,196], 'Diffusion3':[196,295],'Diffusion4':[295,394]}
	fmri_order = {'Rest1':0,'Rest2':1,'Rest3':2,'Rest4':3,'Gambling1':4,'Gambling2':5, 'FaceMatching1':6,'FaceMatching2':7, 'Conflict1':8,'Conflict2':9,'Conflict3':10,'Conflict4':11}

	subjects, sex, scores = utils.loadBANDA140(outliers)

	motionBetween_output=csv.writer(open('/space/erebus/1/users/data/scores/new2/motionBetween_avg_output_rjj020419.csv','w+'))
	motionBetween_output.writerow(['subject','rot_trans','avg_score','questionnaire','questionnaire_score'])

	for key, score in scores.items():

		f, axarr = plt.subplots(1, 2,figsize=(23,14))
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.28)

		trans_boxplot_data = [[],[]]
		rotat_boxplot_data = [[],[]]

		#box plot measures
		g, (boxes1,boxes2) = plt.subplots(nrows=1,ncols=2,figsize=(10,14))

		for i,met in enumerate(metric):
			axarr[i].set_title(str(met)[13:18])
			if str(met)[13:18]=='Trans': boxes1.set_title(str(met)[13:18])
			elif str(met)[13:18]=='Rotat': boxes2.set_title(str(met)[13:18])
			#for calculating axis ranges
			ymin_value = 0
			ymax_value = 0
			xmin_value = 0
			xmax_value = 0

			x_values = []
			y_values = []

			#for s in subjects:
			for s_index,s in enumerate(subjects):
				t_accumulate = 0

				for a in range(len(pairsOfStudies)):
					name1 , name2 = pairsOfStudies[a]

					column,acq_time = getFileData(studies[name1])
					if "Diffusion" in name1:
						f1 = getFilePath(studies[name1],s)
						f2 = getFilePath(studies[name2],s)
						ind1=indexPerDiffusion[name1]
						ind2=indexPerDiffusion[name2]
						acq_time *= 99
					elif "T1" in name1:
						f1 = getFilePath("/motion/structural_motion.nii.gz.par",s)
						f2 = getFilePath("/motion/structural_motion.nii.gz.par",s)
						ind1=0,1
						ind2=1,2
					else:
						f1 = getFilePath("/motion/fmriFirsts_motion.nii.gz.par",s)
						f2 = getFilePath("/motion/fmriFirsts_motion.nii.gz.par",s)
						ind1=fmri_order[name1],	fmri_order[name1]+1
						ind2=fmri_order[name2],fmri_order[name2]+1

					if f1 != None and f2 != None :
						t=  met(f1,column, ind1,acq_time,0,f2, ind2)
						t_accumulate += t

				avg_t = t_accumulate/len(pairsOfStudies)
				if s_index == 0: ymin_value = avg_t
				ymin_value = min(ymin_value,avg_t)
				ymax_value = max(ymax_value,avg_t)

				if s_index == 0: xmin_value = float(score[s_index])
				xmin_value = min(xmin_value,float(score[s_index]))
				xmax_value = max(xmax_value,float(score[s_index]))

				if str(str(key))=='Anhedonia':
					if str(met)[13:18]=='Trans':
						if float(score[s_index])<3: trans_boxplot_data[0].append(avg_t)
						else: trans_boxplot_data[1].append(avg_t)
					if str(met)[13:18]=='Rotat':

						if float(score[s_index])<3: rotat_boxplot_data[0].append(avg_t)
						else: rotat_boxplot_data[1].append(avg_t)

				motionBetween_output.writerow([s,metric_label[metric.index(met)],avg_t,key,float(score[s_index])])
				axarr[i].plot(float(score[s_index]),avg_t,"o",markersize=5, color='m')

				x_values.append(float(score[s_index]))
				y_values.append(avg_t)
			#regression lines
			(sl,b) = polyfit(x_values,y_values,1)
			yp = polyval([sl,b],x_values)
			axarr[i].plot(x_values,yp,'-',color='r')

			axarr[i].set_ylabel("Average " + str(metric_label[metric.index(met)]))
			axarr[i].set_xlabel(str(key))

			axarr[i].set_xlim(xmin_value-(np.median(x_values)*.30),xmax_value+(np.median(x_values)*.30))
			axarr[i].set_ylim(ymin_value-(np.median(y_values)*.30),ymax_value+(np.median(y_values)*.30))

			if str(str(key))=='Anhedonia':
				if i==0:
					trans_box_max_list = [ max(a) for a in trans_boxplot_data]
					trans_box_min_list = [ min(a) for a in trans_boxplot_data]
					boxes1.set_ylabel("Average " + str(metric_label[metric.index(met)]))
					boxes1.set_xlabel(str(key))
				elif i==1:
					rotat_box_max_list = [ max(a) for a in rotat_boxplot_data]
					rotat_box_min_list = [ min(a) for a in rotat_boxplot_data]
					boxes2.set_ylabel("Average " + str(metric_label[metric.index(met)]))
					boxes2.set_xlabel(str(key))
		f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/motionBetween_avg_"+str(key),dpi=199)
		#f.savefig("/space/erebus/1/users/vsiless/QA_plots//motionBetween_avg_"+str(key),dpi=199)

	if str(str(key))=='Anhedonia':
		boxes1.set_ylim(min(trans_box_min_list)-.25,max(trans_box_max_list)+.25)
		boxes2.set_ylim(min(rotat_box_min_list)-.25,max(rotat_box_max_list)+.25)

		#print(trans_boxplot_data[0])
		#print(trans_boxplot_data[1])
		boxes1.boxplot(trans_boxplot_data,labels=['no anhedonia','anhedonia'])
		boxes2.boxplot(rotat_boxplot_data,labels=['no anhedonia','anhedonia'])
		#g.savefig("/space/erebus/1/users/vsiless/QA_plots//motion_Between_avg_Anhedonia"+"_boxplot",dpi=199)
		g.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/motion_Between_avg_Anhedonia"+"_boxplot",dpi=199)
		#plt.show()


def snr_measures(premade_output = None):
	studies = {'Diffusion1':'dMRI_AP1.nii.gz','Diffusion2':'dMRI_PA1.nii.gz','Diffusion3':'dMRI_AP2.nii.gz','Diffusion4':'dMRI_PA2.nii.gz','Rest1':'fMRI_rest1_AP.nii.gz', 'Rest2':'fMRI_rest2_PA.nii.gz', 'Rest3':'fMRI_rest3_AP.nii.gz', 'Rest4':'fMRI_rest4_PA.nii.gz', 'Gambling1':'tfMRI_gambling1_AP.nii.gz', 'Gambling2':'tfMRI_gambling2_PA.nii.gz','FaceMatching1':'tfMRI_faceMatching1_AP.nii.gz', 'FaceMatching2':'tfMRI_faceMatching2_PA.nii.gz', 'Conflict1':'tfMRI_conflict1_AP.nii.gz', 'Conflict2':'tfMRI_conflict2_PA.nii.gz', 'Conflict3':'tfMRI_conflict3_AP.nii.gz', 'Conflict4':'tfMRI_conflict4_PA.nii.gz', 'T2':'T2.nii.gz','T1':'T1.nii.gz'}
	scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4','Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1','T2']

	diffusion=[ [0,98], [98,196],[196,295],[295,394]]

	if premade_output == None:
		snr_output=csv.writer(open('/autofs/space/erebus_001/users/data/scores/new2/snr_avg_output_wComposites_rjj020419.csv','w+'))
		snr_output.writerow(['subject','avg_snr','questionnaire','questionnaire_score'])

	subjects, sex, scores = utils.loadBANDA140(outliers)
	#print(subjects)

	for key, score in scores.items():
		f, axarr = plt.subplots(1,1,figsize=(23,14))
		#f.tight_layout()
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

		axarr.set_title(str(key))
		#for calculating axis ranges
		ymin_value = 0
		ymax_value = 0
		xmin_value = 0
		xmax_value = 0
		x_values = []
		y_values = []

		#for s in subjects:
		for s_index,s in enumerate(subjects):
			print (s)
			if premade_output ==None:
				snr_accumulate = 0
				for scan in scans:
					roi="/space/erebus/1/users/data/preprocess/"+s+"/snr/WMROI5001_2"+studies[scan]
					image="/space/erebus/1/users/data/preprocess/"+s+"/"+studies[scan]
					mean2="/space/erebus/1/users/data/preprocess/"+s+"/snr/mean"+studies[scan]
					std2="/space/erebus/1/users/data/preprocess/"+s+"/snr/std"+studies[scan]
					snr2="/space/erebus/1/users/data/preprocess/"+s+"/snr/snr"+studies[scan]
					#ROI= nib.load("/space/erebus/1/users/data/preprocess/"+s+"/snr/WMROI4010_2"+studies[scan]).get_data()
					#image = nib.load("/space/erebus/1/users/data/preprocess/"+s+"/"+studies[scan]).get_data()
					snr=0
					if os.path.isfile(image) :
						#os.popen("mri_concat --i "+image+ " --mean --o "+mean2).read()
						#os.popen("mri_concat --i "+image+ " --std --o "+std2).read()
						if "T1" in scan or "T2" in scan:
							mean=os.popen("fslstats "+image+" -k "+roi+" -m").read()
							std=os.popen("fslstats "+image+" -k "+roi+" -s").read()

							snr = float(mean.split("\n")[0])/float(std.split("\n")[0])
							#print( snr)
						elif os.path.isfile(std2):
							#os.popen("fscalc "+mean2 +" div "+std2 +" --o " +snr2).read()
							res=os.popen("fslstats "+snr2+" -k "+roi+" -m").read()
							snr= float(res.split("\n")[0])
							snr_accumulate+= snr
				avg_snr = snr_accumulate/len(scans)
				x = float(score[s_index])
				y = avg_snr
				snr_output.writerow([s,y,key,x])

			else:
				snr_accumulate = 0
				for scan in scans:
					with open('/space/erebus/1/users/data/scores/snr_output_master.csv', 'r') as output:
						output_reader = csv.DictReader(output, delimiter = ",")
						for row in iter(output_reader):
							skip = 0
							if str(row['subject'])==s:
								print (row['subject'],s,key,scan)
								if str(row['questionnaire'])==key and str(row['scan'])==scan:
									print (key,scan)
									snr_accumulate += float(row['score'])
									if scans.index(scan) == 0: x = float(row['questionnaire_score'])
									break
								else:
									if skip > 0:skip+= 70
									else: skip+=69
									for i in range(skip):
										next(iter(output_reader))
				avg_snr = snr_accumulate/len(scans)
				y = avg_snr

			axarr.plot(x, y, "o",markersize=5, c='m')

			x_values.append(x)
			y_values.append(y)

			if s_index == 0: ymin_value = y
			ymin_value = min(ymin_value,y)
			ymax_value = max(ymax_value,y)

			if s_index == 0: xmin_value = x
			xmin_value = min(xmin_value,x)
			xmax_value = max(xmax_value,x)

		if key == 'Anhedonia':
			x_1 = [g for g in x_values if g>=3]
			x_2 = [g for g in x_values if g<3]
			#regression lines
			(sl,b) = polyfit(x_1,y_values[-len(x_1):], 1)
			yp = polyval([sl,b],x_1)
			axarr.plot(x_1,yp,'-',color='g')

			#regression lines
			(sl,b) = polyfit(x_2,y_values[:len(x_2)], 1)
			yp = polyval([sl,b],x_2)
			axarr.plot(x_2,yp,'-',color='b')

		else:
			#regression lines
			(sl,b) = polyfit(x_values,y_values, 1)
			yp = polyval([sl,b],x_values)
			axarr.plot(x_values,yp,'-',color='r')
		#GLM
		X=np.array([])
		if key != 'Anhedonia':
			X  = np.ones(len(x_values))
			X =np.stack((X, x_values), axis=-1)
			cval = np.hstack((0, -1))
		else:
			for x in x_values:
				if x>3:
					X=np.append(X,[[1,0]])
				else:
					X=np.append(X,[[0,1]])
			cval = np.hstack((1, -1))
		X= np.array(X).reshape(len(y_values),2)
		Y=np.array(y_values )

		model = GeneralLinearModel(X)
		model.fit(Y)
		z_vals = model.contrast(cval).p_value() # z-transformed statistics
		print(key, z_vals)

		axarr.set_ylabel("Average SNR")
		axarr.set_xlabel(str(key))

		axarr.set_xlim(xmin_value-(np.median(x_values)*.30),xmax_value+(np.median(x_values)*.30))
		axarr.set_ylim(ymin_value-(np.median(y_values)*.30),ymax_value+(np.median(y_values)*.30))

		f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/snr_avg_"+str(key),dpi=199)
		#f.savefig("/space/erebus/1/users/vsiless/QA_plots//snr_avg_"+str(key),dpi=199)


	#plt.show()

#motionWithin_measures()
#motionBetween_measures()
snr_measures()
