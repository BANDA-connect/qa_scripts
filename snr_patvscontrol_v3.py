#author: Viviana Siless - vsiless@mgh.harvard.edu   #/space/erebus/1/users/jwang/jon2/bin/python3.6
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
import utils


studies = {'Diffusion1':'dMRI_AP1.nii.gz','Diffusion2':'dMRI_PA1.nii.gz','Diffusion3':'dMRI_AP2.nii.gz','Diffusion4':'dMRI_PA2.nii.gz','Rest1':'fMRI_rest1_AP.nii.gz', 'Rest2':'fMRI_rest2_PA.nii.gz', 'Rest3':'fMRI_rest3_AP.nii.gz', 'Rest4':'fMRI_rest4_PA.nii.gz', 'Gambling1':'tfMRI_gambling1_AP.nii.gz', 'Gambling2':'tfMRI_gambling2_PA.nii.gz','FaceMatching1':'tfMRI_faceMatching1_AP.nii.gz', 'FaceMatching2':'tfMRI_faceMatching2_PA.nii.gz', 'Conflict1':'tfMRI_conflict1_AP.nii.gz', 'Conflict2':'tfMRI_conflict2_PA.nii.gz', 'Conflict3':'tfMRI_conflict3_AP.nii.gz', 'Conflict4':'tfMRI_conflict4_PA.nii.gz', 'T2':'T2.nii.gz','T1':'T1.nii.gz'}
scans=['Diffusion1','Diffusion2','Diffusion3','Diffusion4','Rest1','Rest2','Rest3','Rest4','Gambling1','Gambling2','FaceMatching1','FaceMatching2','Conflict1','Conflict2','Conflict3','Conflict4','T1','T2']
diffusion=[ [0,98], [98,196],[196,295],[295,394]]

outliers=["BANDA051","BANDA104","BANDA131","BANDA134","BANDA129","BANDA137"]

def snr():
	output=csv.writer(open('/autofs/space/erebus_001/users/data/scores/new2/snr_avg_output_rjj020419.csv','w+'))
	output.writerow(['subject','scan','score'])

	# subjects, subjects_lbl = utils.getBandaDiagnosis(outliers)
	subjects, subjects_lbl = utils.getBandaLabels(outliers)

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
		for s_index,s in enumerate(subjects_lbl['allsubjects']):
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
			# if s in subjects_lbl['control']:
			# 	axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='r')
			# elif s in subjects_lbl['anx']:
			# 	axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='c')
			# elif s in subjects_lbl['dep_anx']:
			# 	axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='m')
			# elif s in subjects_lbl['dep']:
			# 	axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='y')

			if s in subjects_lbl['control']:
				axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='r')
			elif s in subjects_lbl['anx']:
				axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='c')
			elif s in subjects_lbl['dep']:
				axarr[i,j].plot(subjects_lbl['allsubjects'].index(s)+1, snr, "o", c='y')

			if j==0:
				axarr[i,j].set_ylabel("SNR")
			if i==3:
				axarr[i,j].set_xlabel('Subject')

			axarr[i,j].set_xticks(range(1,len(subjects)+1),20)

			axarr[i,j].axvline(14.5, color='k', linestyle='--')
			axarr[i,j].set_ylim((0,35))

			# control_patch = mpatches.Patch(color='r', label='control')
			# anxious_patch = mpatches.Patch(color='c', label='anxious')
			# comorbid_patch = mpatches.Patch(color='m', label='comorbid')
			# depressed_patch = mpatches.Patch(color='y', label='depressed')
			#
			# axarr[i,j].legend(handles=[control_patch,anxious_patch,comorbid_patch,depressed_patch])

			control_patch = mpatches.Patch(color='r', label='control')
			anxious_patch = mpatches.Patch(color='c', label='anxious')
			depressed_patch = mpatches.Patch(color='y', label='depressed')

			axarr[i,j].legend(handles=[control_patch,anxious_patch,depressed_patch])

			"""if "T1" in scan or "T2" in scan or "Diffusion" in scan:
				axarr[i,j].set_yticks([0,1,2,3])
			else:
				axarr[i,j].set_yticks([0,0.1,0.2])
			"""
			#f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr_plots_patvscontrol",dpi=199)
		plotted+=1
	#mng = plt.get_current_fig_manager()
	#mng.full_screen_toggle()

	#plt.show()
	#f.savefig("/space/erebus/1/users/vsiless/snr_20",dpi=199)
	f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/snr_plots_patvscontrol_140",dpi=199)


def plotSNRPerScan():
	snr_perScan=dict()
	subjects, subjects_lbl = utils.getBandaLabels(outliers)

	with open('/autofs/space/erebus_001/users/data/scores/new2/snr_avg_output_rjj020419.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:

				s=row[0]
				scan=row[1][:]
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[]]

					if s in subjects_lbl['control']:
						snr_perScan[scan][0].append(snr)
					elif s in subjects_lbl['anx']:
						snr_perScan[scan][1].append(snr)
					elif s in subjects_lbl['dep']:
						snr_perScan[scan][2].append(snr)
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
		axarr[i, j].violinplot(values, [1,2,3], points=20, widths=0.3, showmeans=True) #,showmedians=True)
		if scanName == 'T1' or scanName == 'T2':
			axarr[i,j].set_ylim((0,15))
		else:
			axarr[i,j].set_ylim((5,30))
		axarr[i,j].set_xticks([1,2,3],["Controls","Anxious","Depressed"])
		#f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr",dpi=199)
		#f.savefig("/autofs/space/erebus_001/users/data/scores/new/plots/snrPerScan_subj1,140",dpi=199)
		plotted+=1

	f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/snrPerScan_140",dpi=199)
	#f.savefig("/autofs/space/erebus_001/users/data/scores/new/plots/snrPerScan_subj1,140",dpi=199)
	#plt.show()


def plotSNRAvg():
	snr_perScan=dict()
	subjects, subjects_lbl = utils.getBandaLabels(outliers)

	with open('/autofs/space/erebus_001/users/data/scores/new2/snr_avg_output_rjj020419.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				s=row[0]
				scan=row[1][:-1]
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[]]

					if s in subjects_lbl['control']:
						snr_perScan[scan][0].append(snr)
					elif s in subjects_lbl['anx']:
						snr_perScan[scan][1].append(snr)
					elif s in subjects_lbl['dep']:
						snr_perScan[scan][2].append(snr)
			except:
				print(row)

	f, axarr = plt.subplots(1, 6,figsize=(23,5))
	f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
	plotted=0

	for scanName, values in snr_perScan.items():
		print (scanName)
		axarr[plotted].set_title(scanName)
		for q in range(len(values)):
			axarr[plotted].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
		if scanName == 'T':
			axarr[plotted].set_ylim((0,15))
		else:
			axarr[plotted].set_ylim((5,30))

		axarr[plotted].set_xticks([0,1,2],["Controls","Anxious","Depressed"])
		#f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr",dpi=199)

		plotted+=1
	for ax in axarr.flatten():
		ax.set_xticks([0,1,2])
		ax.set_xticklabels(["Controls","Anxious","Depressed"])

	f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/snrAvg_140",dpi=199)
	#plt.show()

###stp

def plotWithinScanMotion():
	perScan=[dict(),dict()]
	tipo="within" #"between"
	labels=["Rotation","Translation"]

	subjects, subjects_lbl = utils.getBandaLabels(outliers)

	with open('/space/erebus/1/users/data/scores/new2/motion_'+tipo+'_scan_output_140.csv', 'r') as csvfile:
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
						perScan[ind][scan]=[[],[],[]]

					if s in subjects_lbl['control']:
						perScan[ind][scan][0].append(val)
					elif s in subjects_lbl['anx']:
						perScan[ind][scan][1].append(val)
					elif s in subjects_lbl['dep']:
						perScan[ind][scan][2].append(val)
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
			axarr[i][plotted].set_xticks([0,1,2],["Controls","Anxious","Depressed"])
			# f.savefig("/space/erebus/1/users/vsiless/QA_plots/"+tipo,dpi=199)

			plotted+=1
		for ax in axarr.flatten():
			ax.set_xticks([0,1,2,3])
			ax.set_xticklabels(["Controls","Anxious","Comorbid","Depressed"])
	# plt.show()
	f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/"+tipo+"_withinScanMotion",dpi=199)

#plotSNRAvg()
plotWithinScanMotion()
#plotSNRPerScan()
#snr()
