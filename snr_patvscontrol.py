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
import matplotlib.patches as mpatches
import csv



studies = {'Diffusion1':'dMRI_AP1.nii.gz','Diffusion2':'dMRI_PA1.nii.gz','Diffusion3':'dMRI_AP2.nii.gz','Diffusion4':'dMRI_PA2.nii.gz','Rest1':'fMRI_rest1_AP.nii.gz', 'Rest2':'fMRI_rest2_PA.nii.gz', 'Rest3':'fMRI_rest3_AP.nii.gz', 'Rest4':'fMRI_rest4_PA.nii.gz', 'Gambling1':'tfMRI_gambling1_AP.nii.gz', 'Gambling2':'tfMRI_gambling2_PA.nii.gz','FaceMatching1':'tfMRI_faceMatching1_AP.nii.gz', 'FaceMatching2':'tfMRI_faceMatching2_PA.nii.gz', 'Conflict1':'tfMRI_conflict1_AP.nii.gz', 'Conflict2':'tfMRI_conflict2_PA.nii.gz', 'Conflict3':'tfMRI_conflict3_AP.nii.gz', 'Conflict4':'tfMRI_conflict4_PA.nii.gz', 'T2':'T2.nii.gz','T1':'T1.nii.gz'}	
#studies = {,'T2':'T2.nii.gz','T1':'T1.nii.gz'}

#scans=['T1','T2']
#scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4'] #'Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4',]
scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4','Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1','T2']
diffusion=[ [0,98], [98,196],[196,295],[295,394]]
#subjects = ["BANDA028"]
subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015", "BANDA016", "BANDA017","BANDA018","BANDA019","BANDA020","BANDA021","BANDA022","BANDA023","BANDA024","BANDA025","BANDA026","BANDA027","BANDA028","BANDA029","BANDA030","BANDA031","BANDA032",
"BANDA033","BANDA034","BANDA035","BANDA036","BANDA037","BANDA038","BANDA039","BANDA040",
"BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049",
"BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060", "BANDA061", "BANDA062", "BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA072","BANDA073","BANDA074","BANDA075","BANDA076","BANDA077","BANDA078","BANDA079",
"BANDA080","BANDA081","BANDA082","BANDA083","BANDA084","BANDA085","BANDA086","BANDA087"] #,"BANDA088","BANDA089","BANDA090", "BANDA091", "BANDA092", "BANDA093","BANDA094","BANDA095","BANDA096","BANDA097","BANDA098","BANDA099","BANDA100","BANDA101", "BANDA102","BANDA103","BANDA104","BANDA105","BANDA106","BANDA107","BANDA108","BANDA109","BANDA110","BANDA111","BANDA112","BANDA113", "BANDA114", "BANDA115", "BANDA116", "BANDA117","BANDA118","BANDA119"]
control_subjects = [ "BANDA001", "BANDA002","BANDA003","BANDA004","BANDA005","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014","BANDA016","BANDA018","BANDA027","BANDA033","BANDA034","BANDA038","BANDA043","BANDA046","BANDA050","BANDA051","BANDA054","BANDA058","BANDA059", "BANDA061"
"BANDA067","BANDA071","BANDA072","BANDA078","BANDA079","BANDA080", "BANDA081", "BANDA082","BANDA083","BANDA084","BANDA087"]
dep_subjects = ["BANDA024","BANDA047","BANDA077","BANDA082","BANDA086"]
anx_subjects = ["BANDA017","BANDA021","BANDA022","BANDA023","BANDA025","BANDA026","BANDA030","BANDA031","BANDA032","BANDA035","BANDA036","BANDA039","BANDA040","BANDA041","BANDA042","BANDA048",
"BANDA049""BANDA052","BANDA055","BANDA056","BANDA057","BANDA060","BANDA063","BANDA064","BANDA065","BANDA069","BANDA070","BANDA075","BANDA076"]
dep_and_anx_subjects = ["BANDA006","BANDA015","BANDA019","BANDA020","BANDA028","BANDA029","BANDA037","BANDA044","BANDA045","BANDA053","BANDA062","BANDA066","BANDA073","BANDA074","BANDA075","BANDA076","BANDA077","BANDA080","BANDA081","BANDA085"]


def snr():
	output=csv.writer(open('/space/erebus/1/users/data/scores/snr_output_old2.csv','w+'))
	output.writerow(['subject','scan','score'])	
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

			#axarr[i,j].plot(subjects.index(s)+1, snr, "o",c='C'+str(s_index%10))


			output.writerow([s,scan,snr])
			#color by subject type
			if s in control_subjects:
				axarr[i,j].plot(subjects.index(s)+1, snr, "o", c='r')
			elif s in anx_subjects:
				axarr[i,j].plot(subjects.index(s)+1, snr, "o", c='c')
			elif s in dep_and_anx_subjects:
				axarr[i,j].plot(subjects.index(s)+1, snr, "o", c='m')
			elif s in dep_subjects:
				axarr[i,j].plot(subjects.index(s)+1, snr, "o", c='y')

			if j==0:
				axarr[i,j].set_ylabel("SNR")
			if i==3:
				axarr[i,j].set_xlabel('Subject')

			axarr[i,j].set_xticks(range(1,len(subjects)+1),20)

			axarr[i,j].axvline(14.5, color='k', linestyle='--')
			axarr[i,j].set_ylim((0,35))

			control_patch = mpatches.Patch(color='r', label='control')
			anxious_patch = mpatches.Patch(color='c', label='anxious')
			comorbid_patch = mpatches.Patch(color='m', label='comorbid')
			depressed_patch = mpatches.Patch(color='y', label='depressed')

			axarr[i,j].legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])
				
			"""if "T1" in scan or "T2" in scan or "Diffusion" in scan:
				axarr[i,j].set_yticks([0,1,2,3])
			else:
				axarr[i,j].set_yticks([0,0.1,0.2])
			"""
			f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr_plots_patvscontrol",dpi=199)
		plotted+=1
	#mng = plt.get_current_fig_manager()
	#mng.full_screen_toggle()

	plt.show()
	#f.savefig("/space/erebus/1/users/vsiless/snr_20",dpi=199)
def plotSNRPerScan():
	snr_perScan=dict()
	with open('/space/erebus/1/users/data/scores/snr_output_old.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				
				s=row[0]
				scan=row[1][:]
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[],[]]

					if s in control_subjects:
						snr_perScan[scan][0].append(snr)
					elif s in anx_subjects:
						snr_perScan[scan][1].append(snr)
					elif s in dep_and_anx_subjects:
						snr_perScan[scan][2].append(snr)
					elif s in dep_subjects:
						snr_perScan[scan][3].append(snr)
			except:
				print(row)
				
	f, axarr = plt.subplots(4, 5,figsize=(23,14))
	f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
	plotted=0

	for scanName, values in snr_perScan.items():
		i=plotted%4
		j=int(plotted/4)
		print (scanName)
		axarr[i,j].set_title(scanName)
		axarr[i, j].violinplot(values, [1,2,3,4], points=20, widths=0.3, showmeans=True) #,showmedians=True)
		axarr[i,j].set_ylim((5,30))
	
		f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr",dpi=199)
		plotted+=1
	

	plt.show()
def plotSNRAvg():
	snr_perScan=dict()
	with open(':', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				s=row[0]
				scan=row[1][:-1]
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[],[]]

					if s in control_subjects:
						snr_perScan[scan][0].append(snr)
					elif s in anx_subjects:
						snr_perScan[scan][1].append(snr)
					elif s in dep_and_anx_subjects:
						snr_perScan[scan][2].append(snr)
					elif s in dep_subjects:
						snr_perScan[scan][3].append(snr)
			except:
				print(row)
				
	f, axarr = plt.subplots(1, 5,figsize=(23,5))
	f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
	plotted=0

	for scanName, values in snr_perScan.items():
		print (scanName)
		axarr[plotted].set_title(scanName)
		for q in range(len(values)):
			axarr[plotted].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
		axarr[plotted].set_ylim((5,30))
	
		axarr[plotted].set_xticks([0,1,2,3],["Controls","Anxious","Comorbid","Depressed"])
		f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr",dpi=199)

		plotted+=1
	for ax in axarr.flatten():
		ax.set_xticks([0,1,2,3])
		ax.set_xticklabels(["Controls","Anxious","Comorbid","Depressed"])
	plt.show()
def plotWithinScanMotion():
	perScan=[dict(),dict()]
	tipo="between" #within" #"between"
	labels=["Rotation","Translation"]
	#with open('/space/erebus/1/users/data/scores/motion_'+tipo+'_scan_output.csv', 'r') as csvfile:
	with open('//autofs/space/erebus_001/users/data/scores/new/motion_within_scan_output_081918.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				s=row[0]
				if "Rotation" in row[1]:
					ind=0
				else:
					ind=1
				if "T" not in row[2]:
					scan=row[2][:-1]
				else:				
					scan=row[2]	
					
				
				val=float(row[3])
				#except:
				#	val=0
				if val>0:
					if not scan in perScan[ind]:
						perScan[ind][scan]=[[],[],[],[]]

					if s in control_subjects:
						perScan[ind][scan][0].append(val)
					elif s in anx_subjects:
						perScan[ind][scan][1].append(val)
					elif s in dep_and_anx_subjects:
						perScan[ind][scan][2].append(val)
					elif s in dep_subjects:
						perScan[ind][scan][3].append(val)
			except:
				print(row)
		
	f, axarr = plt.subplots(2, 9,figsize=(23,5))
	f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
	
	for i in range(2):
		plotted=0
		for scanName, values in perScan[i].items():
			print (scanName)
			axarr[i][plotted].set_title(scanName)
			for q in range(len(values)):
				axarr[i][plotted].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
			axarr[i][plotted].set_ylim((0,1))
			axarr[i][plotted].set_ylabel(labels[i])
			axarr[i][plotted].set_xticks([0,1,2,3],["Controls","Anxious","Comorbid","Depressed"])
			f.savefig("/space/erebus/1/users/vsiless/QA_plots/"+tipo,dpi=199)

			plotted+=1
		for ax in axarr.flatten():
			ax.set_xticks([0,1,2,3])
			ax.set_xticklabels(["Controls","Anxious","Comorbid","Depressed"])
	plt.show()

	
plotSNRAvg()	
#plotWithinScanMotion()
#plotSNRPerScan()	
#snr()
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

