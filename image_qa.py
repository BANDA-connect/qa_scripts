#author: Viviana Siless - vsiless@mgh.harvard.edu
import sys
import math 
import glob
import numpy as np
import os.path
import matplotlib
print matplotlib.get_cachedir()
import matplotlib.pyplot as plt
import nibabel as nib
from scipy import stats

def getSNR(data):
	brain = stats.threshold(data, threshmin=1000, threshmax=1000000, newval=0)

	black = stats.threshold(data, threshmin=-1000000, threshmax=500, newval=0)


	return (np.mean(brain)/(np.std(black)**2), np.mean(brain)/(np.std(black)))

def generateFiles():
	for s in subjects:
		print "subject"+s
		metrics = open("/space/erebus/1/users/data/preprocess/"+s+"/qa.csv", 'w')
		for f in files:
			metrics.write(f+",")	
		metrics.write("\n")
		for f in files:
			img = nib.load("/space/erebus/1/users/data/preprocess/"+s+"/"+f)

			snr =  getSNR(img.get_data())
			metrics.write(str(snr[0])+",")
		metrics.write("\n")
		for f in files:
			img = nib.load("/space/erebus/1/users/data/preprocess/"+s+"/"+f)

			snr =  getSNR(img.get_data())
			metrics.write(str(snr[1])+",")
		metrics.write("\n")
		metrics.close()

def plotQA():
	metrics_labels = ["SNR $\sigma^2$","SNR $\sigma$"]	
	metrics_values =[[],[]]
	header = []
	for s in subjects:
		metrics = open("/space/erebus/1/users/data/preprocess/"+s+"/qa.csv", 'r')
		print "/space/erebus/1/users/data/preprocess/"+s+"/qa.csv"
		i=0
		for line in metrics:
			qa_val = line.split(",")	
			
			if len(header)==0 and i==0:
				header = qa_val[0:len(qa_val)-1]
			if i==1:
				metrics_values[0].append(qa_val[0:len(qa_val)-1])
			elif i==2:
				metrics_values[1].append(qa_val[0:len(qa_val)-1])
			i+=1
							
		
	print header	
        print metrics_values	
	for m in metrics_values:
		f, axarr = plt.subplots( 4,3)
		f.canvas.set_window_title(metrics_labels[metrics_values.index(m)])	
		s=0
		for qa_vals in m:
			i=0			
			for qa in qa_vals:
				y=i/4
				x=i%4
				axarr[x,y].set_title(header[i])
				axarr[x,y].plot(m.index(qa_vals),qa, "o")
				print qa
				i+=1
			s+=1

	plt.show()			

subjects = [ "BANDA001","BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012"] #,"BANDA013"]
files = ["fMRI_rest1_AP_topup.nii.gz","fMRI_rest2_PA_topup.nii.gz","fMRI_rest3_AP_topup.nii.gz","fMRI_rest4_PA_topup.nii.gz",
"tfMRI_gambling1_AP_topup.nii.gz","tfMRI_gambling2_PA_topup.nii.gz","tfMRI_faceMatching1_AP_topup.nii.gz","tfMRI_faceMatching2_PA_topup.nii.gz","tfMRI_conflict1_AP_topup.nii.gz","tfMRI_conflict2_PA_topup.nii.gz","tfMRI_conflict3_AP_topup.nii.gz","tfMRI_conflict4_PA_topup.nii.gz"]

		
#generateFiles()
plotQA()
