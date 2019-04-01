#author: Viviana Siless - vsiless@mgh.harvard.edu
import csv

import os
import math
import numpy as np
import nibabel as nib
import os.path
import matplotlib
print( matplotlib.get_cachedir())
import matplotlib.pyplot as plt

studies = {'Diffusion1':'dMRI_AP1.nii.gz','Diffusion2':'dMRI_PA1.nii.gz','Diffusion3':'dMRI_AP2.nii.gz','Diffusion4':'dMRI_PA2.nii.gz','Rest1':'fMRI_rest1_AP.nii.gz', 'Rest2':'fMRI_rest2_PA.nii.gz', 'Rest3':'fMRI_rest3_AP.nii.gz', 'Rest4':'fMRI_rest4_PA.nii.gz', 'Gambling1':'tfMRI_gambling1_AP.nii.gz', 'Gambling2':'tfMRI_gambling2_PA.nii.gz','FaceMatching1':'tfMRI_faceMatching1_AP.nii.gz', 'FaceMatching2':'tfMRI_faceMatching2_PA.nii.gz', 'Conflict1':'tfMRI_conflict1_AP.nii.gz', 'Conflict2':'tfMRI_conflict2_PA.nii.gz', 'Conflict3':'tfMRI_conflict3_AP.nii.gz', 'Conflict4':'tfMRI_conflict4_PA.nii.gz', 'T2':'T2.nii.gz','T1':'T1.nii.gz'}	
#studies = {,'T2':'T2.nii.gz','T1':'T1.nii.gz'}

#scans=['T1','T2']
#scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4'] #'Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4',]
scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4','Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1','T2']
diffusion=[ [0,98], [98,196],[196,295],[295,394]]
#subjects = ["BANDA028"]
subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008", "BANDA009", "BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015", "BANDA016", "BANDA017","BANDA018","BANDA019", "BANDA020","BANDA021","BANDA022","BANDA023","BANDA024","BANDA025","BANDA026","BANDA027","BANDA028","BANDA029","BANDA030","BANDA031","BANDA032","BANDA033","BANDA034","BANDA035","BANDA036",
"BANDA037","BANDA038","BANDA039","BANDA040","BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049"]

def snr():
	
	f, axarr = plt.subplots(4, 5,figsize=(23,14))
	#f.tight_layout()
	f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

	plotted=0
	for scan in scans:
		i=plotted%4
		j=int(plotted/4)
		print (scan)
		axarr[i,j].set_title(scan)
		print(i,j)
			
		#for s in subjects:
		for s_index,s in enumerate(subjects):			
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
					print( snr)
				elif os.path.isfile(std2):
					#os.popen("fscalc "+mean2 +" div "+std2 +" --o " +snr2).read()		
					res=os.popen("fslstats "+snr2+" -k "+roi+" -m").read()
					snr= float(res.split("\n")[0])		

			axarr[i,j].plot(subjects.index(s)+1, snr, "o",c='C'+str(s_index%10))

			if j==0:
				axarr[i,j].set_ylabel("SNR")
			if i==3:
				axarr[i,j].set_xlabel('Subject')

			axarr[i,j].set_xticks(range(1,len(subjects)+1,4))

			#axarr[i,j].set_xticklabels([])

			axarr[i,j].axvline(14.5, color='k', linestyle='--')
			axarr[i,j].set_ylim((0,30))
				
			"""if "T1" in scan or "T2" in scan or "Diffusion" in scan:
				axarr[i,j].set_yticks([0,1,2,3])
			else:
				axarr[i,j].set_yticks([0,0.1,0.2])
			"""
			f.savefig("/space/erebus/1/users/data/motion_and_snr_plots/snr_plots1",dpi=199)
		plotted+=1
	#mng = plt.get_current_fig_manager()
	#mng.full_screen_toggle()

	plt.show()
	#f.savefig("/space/erebus/1/users/vsiless/snr_20",dpi=199)
snr()
"""
#nonzeros=ROI.nonzero()
#amount=len(nonzeros[0])
#nonZV =  range(int(amount/2),int( amount/2+20))	
#nonZV =  range(amount)	
				
if "Diffusion" in scan:
	#num = int(scan.replace("Diffusion",""))-1
	#image = image [:,:,:,diffusion[num][0]: diffusion[num][1]]
	norm=0
	for w in range(2):
		masked = []	
		for k in nonZV:
			x = nonzeros[0][k]
			y = nonzeros[1][k]
			z = nonzeros[2][k]
			#if image[x,y,z,w] >1500:
			masked.append(image[x,y,z,w])
		#print(masked)
		print(s,np.mean(masked), np.std(masked))
		snr += np.mean(masked)/np.std(masked)
		norm+=1
	snr/=norm
	#snr= min(snr,3)
elif scan is "T1" or scan is "T2":
	masked = []	
	for k in nonZV:
		x = nonzeros[0][k]
		y = nonzeros[1][k]
		z = nonzeros[2][k]

		masked.append(image[x,y,z])
	print(s,np.mean(masked), np.std(masked))	
	snr = np.mean(masked)/np.std(masked)

else:
	snr=0
	hola=[]					
	for k in nonZV:
		x = nonzeros[0][k]
		y = nonzeros[1][k]
		z = nonzeros[2][k]
		#print(s,len(image[x,y,z,:]),np.mean(image[x,y,z,:]),np.std(image[x,y,z,:]))
		snr+=np.mean(image[x,y,z,:])/np.std(image[x,y,z,:])
		#hola=[]
		#hola.append(image[x,y,z,:])
	#snr=np.mean(hola)/np.std(hola)
	snr=snr/len(nonZV)
"""

