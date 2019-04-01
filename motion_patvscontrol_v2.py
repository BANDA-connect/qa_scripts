#author: Viviana Siless - vsiless@mgh.harvard.edu   #/space/erebus/1/users/jwang/jon2/bin/python3.6
import sys
import math 
import glob
import numpy as np
import os.path
import matplotlib
print( matplotlib.get_cachedir())
import matplotlib.pyplot as plt
import dicom

from numpy import linalg as LA
from pyquaternion import Quaternion
import matplotlib.patches as mpatches
import csv
import utils

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

def test_vNavsScore(vals1, vals2):
	q1 = Quaternion(axis=[vals1[1],vals1[2],vals1[3]], angle=vals1[0])
	q2 = Quaternion(axis=[vals2[1],vals2[2],vals2[3]], angle=vals2[0])
	q3 =q1*q2.inverse
	angle = q3.angle
	axis = q3.axis

	t = vals1[4:] -vals2[4:]
	
	t_rotmax = 100 * np.sqrt(2-2*np.cos(angle))
	temp=t_rotmax*LA.norm(np.asarray(t-np.dot(t,axis)*axis))
	nav_score = np.sqrt(t_rotmax**2 + 2*temp + LA.norm(t)**2)
	print ("score",nav_score)
	
def getvNavScore(lista):
	vals1= lista[len(lista)-1]
	vals2= lista[len(lista)-2]
	q1 = Quaternion(axis=[vals1[1],vals1[2],vals1[3]], angle=vals1[0])
	q2 = Quaternion(axis=[vals2[1],vals2[2],vals2[3]], angle=vals2[0])
	q3 =q1*q2.inverse
	angle = q3.angle
	axis = q3.axis

	t = vals1[4:] -vals2[4:]

	t_rotmax = 100 * np.sqrt(2-2*np.cos(angle))
	temp=t_rotmax*LA.norm(np.asarray(t-np.dot(t,axis)*axis))
	nav_score = np.sqrt(t_rotmax**2 + 2*temp + LA.norm(t)**2)
	return nav_score
def vNavRead():
	f, axarr = plt.subplots(1,2)
	#subjects = ["BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060"]
	#subjects = ["BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015"]
	#subjects = ["BANDA092","BANDA093","BANDA094","BANDA095","BANDA096","BANDA097","BANDA098","BANDA099", "BANDA100","BANDA101","BANDA102","BANDA103","BANDA104","BANDA105","BANDA106","BANDA107","BANDA108","BANDA109", "BANDA110","BANDA111","BANDA112","BANDA113","BANDA114","BANDA115","BANDA116","BANDA117","BANDA118","BANDA119"] 
	#,"BANDA088","BANDA089","BANDA090","BANDA091",]
	subjects = ["BANDA138","BANDA139","BANDA140"] 
	#["BANDA126","BANDA127","BANDA128","BANDA129","BANDA130","BANDA132","BANDA133","BANDA135","BANDA136","BANDA137","BANDA138","BANDA139","BANDA140"] 

	#["BANDA083","BANDA084","BANDA085","BANDA086","BANDA087"]
	for s in subjects:

		dicoms = glob.glob('/space/erebus/1/users/data/dicoms/'+s+'/MR*')
		vnavsT1=[]
		vnavsT2=[]
		vnavsT1Score=[]
		vnavsT2Score=[]
		vnavsT1Comms=[]
		vnavsT2Comms=[]

		vNav=0
		vNav2=0
		for d in dicoms:
			dcm =dicom.read_file(d)
			if dcm.ProtocolName == 'HCP_MGH_T1w_MPR_vNav' and dcm.SequenceName=='ABCD3d1_32ns':
				quat=dcm.ImageComments.split()
				if vNav ==0 and len(vnavsT1Score)>1:
					vnavsT1Score=[]
				vnavsT1Comms.append(str(dcm.AcquisitionNumber)+ " " + dcm.ImageComments)
				if int(dcm.AcquisitionNumber) >1 :

					vnavsT1.append(np.array([float(quat[1]),float(quat[2]),float(quat[3]),float(quat[4]),float(quat[6]),float(quat[7]),float(quat[8])]))
					if len(vnavsT1)>1:
						vnavsT1Score.append(getvNavScore(vnavsT1))	
						print (vnavsT1Comms[len(vnavsT1Comms)-2] ,"vnav score:", vnavsT1Score[len(vnavsT1Score)-1])
					vNav+=1			

				else:
					vnavsT1.append(np.array([0.0,1.0,0.0,0.0,0.0,0.0,0.0]))
					vnavsT1Score.append(getvNavScore(vnavsT1))	
					print (vnavsT1Comms[len(vnavsT1Comms)-2], "vnav score:",vnavsT1Score[len(vnavsT1Score)-1])
					vNav=0				

			elif dcm.ProtocolName == 'HCP_MGH_T2w_SPC_vNav' and dcm.SequenceName=='ABCD3d1_32ns':
				quat=dcm.ImageComments.split()
				if vNav2 ==0 and len(vnavsT2Score)>1:
					vnavsT2Score=[]
				if int(dcm.AcquisitionNumber) >1 :
					vnavsT2.append(np.array([float(quat[1]),float(quat[2]),float(quat[3]),float(quat[4]),float(quat[6]),float(quat[7]),float(quat[8])]))
					if len(vnavsT2)>1:
						vnavsT2Score.append(getvNavScore(vnavsT2))	
					vNav2+=1			
				else:
					vnavsT2.append(np.array([0.0,1.0,0.0,0.0,0.0,0.0,0.0]))
					vnavsT2Score.append(getvNavScore(vnavsT2))	
					vNav2=0
					
		f = open("/space/erebus/1/users/data/preprocess/"+s+"/motion/vnavsT1Score.csv", 'w')
		f.write(str(vnavsT1Score).replace("[","").replace("]",""))
		f.close()
		f = open("/space/erebus/1/users/data/preprocess/"+s+"/motion/vnavsT2Score.csv", 'w')
		f.write(str(vnavsT2Score).replace("[","").replace("]",""))
		f.close()
	
		print (vnavsT1Score)
		print (vnavsT2Score)
		print(s, "T1", sum(np.array(vnavsT1Score)>0.5))				
		print(s, "T2", sum(np.array(vnavsT2Score)>0.5))

		axarr[0].plot(range(len(vnavsT1Score)),vnavsT1Score,label=s)
		axarr[0].set_xlabel('TR (T1)')
		axarr[0].set_ylabel('vnav score')

		axarr[1].plot(range(len(vnavsT2Score)),vnavsT2Score,label=s)
		axarr[1].set_xlabel('TR (T2)')
		axarr[1].set_ylabel('vnav score')
	axarr[0].legend(ncol=3)	
	axarr[1].legend(ncol=3)
		
	#plt.show()


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



def plotWithinScanMotion():
        output=csv.writer(open('/space/erebus/1/users/data/scores/new/motion_within_scan_output_subj1,140.csv','w+'))
        output.writerow(['subject','rot_trans','scan_type','score'])

        scans.append("T1 all vnavs - no reacq")
        scans.append("T2 all vnavs - no reacq")

        outliers=["BANDA141","BANDA142","BANDA143"]

        subjects, subjects_lbl = utils.getBandaDiagnosis(outliers)

        for m in metric:
                f, axarr = plt.subplots(4, 5)
                f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.28)
                num=0
                for name  in scans:
                        fileN = studies[name.split()[0]]
                        i=num%4
                        j=int(num/4)
			
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
				
                        axarr[i,j].set_title(name)
                        #for s in subjects:
                        for s_index,s in enumerate(subjects_lbl['allsubjects']):				
                                f = getFilePath(fileN,s)
                                if f != None : 
                                        print (name)
                                        if "T1" == name:
                                                ind = readVNavsScoreFiles(s, "T1")
                                        elif "T2" == name:
                                                ind = readVNavsScoreFiles(s, "T2")
                                                #print(s, ind)
                                        else:
                                                ind = range(index[0], index[1])
					
                                        t=  m(f,column,np.sort(ind),acq_time)
                                        #axarr[i,j].plot(subjects.index(s)+1, t, "o",c='C'+str(s_index%10))
                                        output.writerow([s,m,name,t])
                                        #color by subject type
                                        if s in subjects_lbl['control']:
                                                axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='r')
                                        elif s in subjects_lbl['anx']:
                                                axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='c')
                                        elif s in subjects_lbl['dep_anx']:
                                                axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='m')
                                        elif s in subjects_lbl['dep']:
                                                axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='y')

						

                        if j==0:
                                axarr[i,j].set_ylabel(metric_label[metric.index(m)])
                        if i==3:
                                axarr[i,j].set_xlabel('Subject')

                        if metric.index(m) >1 :
                                axarr[i,j].set_ylim((-.1,7))
                        else:
                                axarr[i,j].set_ylim((-.1,1))
                        axarr[i,j].axvline(14.5, color='k', linestyle='--')
                        axarr[i,j].set_xticks(range(1,len(subjects)+1),20)
                        num+=1

                        control_patch = mpatches.Patch(color='r', label='control')
                        anxious_patch = mpatches.Patch(color='c', label='anxious')
                        comorbid_patch = mpatches.Patch(color='m', label='comorbid')
                        depressed_patch = mpatches.Patch(color='y', label='depressed')

                        axarr[i,j].legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])


        plt.show()
def plotBetweenScanMotion():
	#output=csv.writer(open('/space/erebus/1/users/data/scores/motion_between_scan_output.csv','w+'))
	#output.writerow(['subject','rot_trans','scan_type','score'])

	output=csv.writer(open('/space/erebus/1/users/data/scores/new/motion_between_scan_output_subj1,140_091018.csv','w+'))
	output.writerow(['subject','rot_trans','scan_type','score'])

	scans.append("T1 all vnavs - no reacq")
	scans.append("T2 all vnavs - no reacq")

	outliers=["BANDA141","BANDA142","BANDA143"]

	subjects, subjects_lbl = utils.getBandaDiagnosis(outliers)


	for m in metric[0:2]:
		f, axarr = plt.subplots(3,4)
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.28)
		num=0
		#for name1, name2  in pairsOfStudies.items():
		for a in range(len(pairsOfStudies)):
			name1 , name2 = pairsOfStudies[a]
			print( name1, name2)
			i=num%3
			j=int(num/3)
			axarr[i,j].set_title(name1+"_"+name2)
			name="%s_%s" % (name1, name2)

			y_values = []

			for s_index,s in enumerate(subjects_lbl['allsubjects']):			
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
					t=  m(f1,column, ind1,acq_time,0,f2, ind2) #/acq_time
					y_values.append(t)
					#axarr[i,j].plot(subjects.index(s)+1, t, "o",c='C'+str(s_index%10))
					output.writerow([s,m,name,t])
					#color by subject type
					if s in subjects_lbl['control']:
						axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='r')
					elif s in subjects_lbl['anx']:
						axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='c')
					elif s in subjects_lbl['dep_anx']:
						axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='m')
					elif s in subjects_lbl['dep']:
						axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='y')

			if j==0:
				axarr[i,j].set_ylabel(metric_label[metric.index(m)])
			if i==2:
				axarr[i,j].set_xlabel('Subject')

			#axarr[i,j].axvline(14.5, color='k', linestyle='--')
			axarr[i,j].set_xticks(range(1,len(subjects)+1),20)
			#axarr[i,j].set_xticklabels(np.arange(1,len(subjects)+1,20))


			num+=1

			#if metric.index(m)==1 :
			if max(y_values)<10:
				axarr[i,j].set_ylim(-.1,max(y_values)+1)
			control_patch = mpatches.Patch(color='r', label='control')
			anxious_patch = mpatches.Patch(color='c', label='anxious')
			comorbid_patch = mpatches.Patch(color='m', label='comorbid')
			depressed_patch = mpatches.Patch(color='y', label='depressed')

			axarr[i,j].legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])


	plt.show()
	
def plotLTAMovement():
	f, axarr = plt.subplots(1,2)
	
	files=['dMRI_AP1_2_T1.lta_diff' ,'dMRI_PA1_2_dMRI_AP1.lta_diff', 		'fMRI_rest1_AP_2_dMRI_PA1.lta_diff','fMRI_rest2_PA_2_fMRI_rest1_AP.lta_diff' ,'dMRI_AP2_2_fMRI_rest2_PA.lta_diff','dMRI_PA2_2_dMRI_AP2.lta_diff','fMRI_rest3_AP_2_dMRI_PA2.lta_diff' ,
	'fMRI_rest4_PA_2_fMRI_rest3_AP.lta_diff', 'tfMRI_gambling1_AP_2_fMRI_rest4_PA.lta_diff','tfMRI_gambling2_PA_2_tfMRI_gambling1_AP.lta_diff','tfMRI_faceMatching1_AP_2_tfMRI_gambling2_PA.lta_diff',
	'tfMRI_faceMatching2_PA_2_tfMRI_faceMatching1_AP.lta_diff','tfMRI_conflict1_AP_2_tfMRI_faceMatching2_PA.lta_diff','tfMRI_conflict2_PA_2_tfMRI_conflict1_AP.lta_diff',
	'tfMRI_conflict3_AP_2_tfMRI_conflict2_PA.lta_diff','tfMRI_conflict4_PA_2_tfMRI_conflict3_AP.lta_diff' ,'T2_2_tfMRI_conflict4_PA.lta_diff']

	labels=['T1','dMRI1','dMRI2','fMRI1','fMR2','dMRI3','dMRI4','fMRI3','fMRI4','gambling1','gambling2','faceMatching1','faceMatchin2', 'conflict1', 'conflict2','conflict3', 'conflict4', 'T2']
	for s in subjects:
		angles=[]
		trans=[]
		for f in files:
			lta_diff= open("/space/erebus/1/users/data/preprocess/"+s+"/motion/"+f)
			for line in lta_diff:
				if "RotAngle" in line:
					angles.append((float(line.split()[2])*180/3.15)%180)

				if "AbsTrans" in line:
					trans.append(line.split()[2])
				
		axarr[0].plot(angles,label=s)
		axarr[0].set_xlabel('scans')
		axarr[0].set_ylabel('angle')
		#axarr[0].get_xticklabels().set_rotation(90)
		#plt.setp(axarr, xticks=range(len(labels)), xticklabels=labels)
		axarr[1].plot(trans,label=s)
		axarr[1].set_xlabel('scans')
		axarr[1].set_ylabel('translation (mm)')
	labels2=[]
	for i in range(1,len(labels)):
		labels2.append(labels[i]+"-"+labels[i-1])
	matplotlib.pyplot.sca(axarr[1])
	plt.xticks(rotation=90)
	#axarr[1].get_xticklabels().set_rotation(90)
	axarr[1].legend(ncol=3)
	#plt.setp(axarr, xticks=range(len(labels)), xticklabels=labels)
	plt.setp(axarr, xticks=range(len(labels)), xticklabels=labels2)
	matplotlib.pyplot.sca(axarr[0])
	plt.xticks(rotation=90)
	plt.show()


studies = {'Diffusion1': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion2': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion3': 'dMRI_topup_eddy.nii.gz.eddy_parameters','Diffusion4':
'dMRI_topup_eddy.nii.gz.eddy_parameters','Rest1': 'fMRI_rest1_AP_motion.nii.gz.par','Rest2': 'fMRI_rest2_PA_motion.nii.gz.par','Rest3': 'fMRI_rest3_AP_motion.nii.gz.par','Rest4':
'fMRI_rest4_PA_motion.nii.gz.par', 'Gambling1' : 'tfMRI_gambling1_AP_motion.nii.gz.par','Gambling2' : 'tfMRI_gambling2_PA_motion.nii.gz.par','FaceMatching1' :
'tfMRI_faceMatching1_AP_motion.nii.gz.par','FaceMatching2' :
'tfMRI_faceMatching2_PA_motion.nii.gz.par','Conflict1':'tfMRI_conflict1_AP_motion.nii.gz.par','Conflict2':'tfMRI_conflict2_PA_motion.nii.gz.par','Conflict3':'tfMRI_conflict3_AP_motion.nii.gz.par',
'Conflict4':'tfMRI_conflict4_PA_motion.nii.gz.par', 'T1':'motion/T1_motion.nii.gz.par','T2':'motion/T2_motion.nii.gz.par'}

scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4','Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1',
'T2']

diffusion=[ [0,98], [98,196],[196,295],[295,394]]

metric = [getTranslation, getRotation] #, getTranslationAbsolute, getRotationAbsolute]
metric_label=["Translation (mm/s)" , "Rotation ($\degree/s$)", "Absolute translation per second", "Absolute rotation per second"]

pairsOfStudies = {'Diffusion1':'Diffusion2','Diffusion2':'Diffusion3','Diffusion3':'Diffusion4',
'Rest1':'Rest2','Rest2':'Rest3','Rest3':'Rest4','Gambling1':'Gambling2','FaceMatching1':'FaceMatching2','Conflict1':'Conflict2','Conflict2':'Conflict3', 'Conflict3':'Conflict4'}
#pairsOfStudies = {'Diffusion2':'Diffusion3'}
pairsOfStudies=[('Diffusion1','Diffusion2'),('Diffusion2','Diffusion3'),('Diffusion3','Diffusion4'),('Rest1','Rest2'),('Rest2','Rest3'),('Rest3','Rest4'),('T1','T2'),('Gambling1','Gambling2'),(
'FaceMatching1', 'FaceMatching2'),('Conflict1','Conflict2'),('Conflict2','Conflict3'), ('Conflict3','Conflict4')]
indexPerDiffusion = {'Diffusion1':[0,98], 'Diffusion2':[98,196], 'Diffusion3':[196,295],'Diffusion4':[295,394]}
fmri_order = {'Rest1':0,'Rest2':1,'Rest3':2,'Rest4':3,'Gambling1':4,'Gambling2':5, 'FaceMatching1':6,'FaceMatching2':7, 'Conflict1':8,'Conflict2':9,'Conflict3':10,'Conflict4':11}

#vNavRead()
#plotLTAMovement()
#test_vNavsScore()
#plotWithinScanMotion()
plotBetweenScanMotion()
#readVNavsScoreFiles()

"""
vals0=np.array([0,1,0,0,0,0,0 ])
vals1=np.array([-0.0010, -0.7937, -0.3014, -0.5284, 0.00, -0.03, 0.05 ])
vals2=np.array([-0.0015 ,-0.7621 ,-0.5352, -0.3643 ,-0.02, -0.03, 0.07])
vals3=np.array([-0.0012, -0.8314, -0.5554 ,-0.0155, -0.04 ,0.03 ,0.05 ])
vals4=np.array([-0.0017 ,-0.5576 ,-0.6031, -0.5703,   0.00, 0.05 ,0.05])
vals5=np.array([-0.0011 ,-0.5080 ,-0.6793, -0.5297,  -0.11 ,0.08 ,-0.02 ])
vals6=np.array([-0.0018 ,-0.5374 ,-0.8238 ,-0.1806 , -0.04 ,0.05, -0.01])
vals7=np.array([-0.0017, -0.6927, -0.5028, -0.5171 ,-0.08, 0.02, 0.07 ])
vals8=np.array([-0.0022 ,-0.6882 ,-0.4416, -0.5756 , -0.09 ,-0.02 ,0.19])
vals9=np.array([-0.0019 ,-0.5490 ,-0.6501, -0.5254  ,-0.04 ,0.03 ,0.14 ])

test_vNavsScore(vals0,vals1)
test_vNavsScore(vals1,vals2)
test_vNavsScore(vals2,vals3)
test_vNavsScore(vals3,vals4)
test_vNavsScore(vals4,vals5)
test_vNavsScore(vals5,vals6)
test_vNavsScore(vals6,vals7)
test_vNavsScore(vals7,vals8)
test_vNavsScore(vals8,vals9)


vals1=np.array([-0.0066, -0.7290, 0.5318, 0.4309, 0.54 ,0.33 ,0.04])
vals2=np.array([-0.0079 ,-0.8237 ,0.2869, 0.4892 ,0.50, 0.23, 0.10]) 
vals3=np.array([ -0.0069 ,-0.8022, 0.3268, 0.4996,   0.52, 0.32 ,-0.06])
vals4=np.array([ -0.0086, -0.8320, 0.3709, 0.4126, 0.54 ,0.29 ,0.11])
vals5=np.array([-0.0073, -0.7824, 0.2467, 0.5718 , 0.46 ,0.34 ,-0.08])
vals6=np.array([-0.0071, -0.8861 ,0.2709 ,0.3762 , 0.57, 0.26, 0.10 ])
vals7=np.array([ -0.0078 ,-0.8110, 0.3998, 0.4272 , 0.50, 0.32, -0.06])
test_vNavsScore(vals1,vals2)
test_vNavsScore(vals2,vals3)
test_vNavsScore(vals3,vals4)
test_vNavsScore(vals4,vals5)
test_vNavsScore(vals5,vals6)
test_vNavsScore(vals6,vals7)
"""

