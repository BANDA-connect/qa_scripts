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
from collections import OrderedDict
import matplotlib
matplotlib.rcParams.update({'font.size': 18})

outliers=["BANDA051","BANDA104","BANDA131","BANDA134","BANDA129","BANDA137"]

subjects,  catdic = utils.getBandaLabels(outliers)

print(subjects)
control_subjects = catdic['control']
anx_subjects = catdic['anx']
dep_subjects = catdic['dep']

# dep_and_anx_subjects = catdic['dep_anx']
partial_scan_subjects = catdic['partial_scan']
no_scan_subjects = catdic['no_scan']

colors=['#74c7a5', '#FF8600','#36649E']
labels=['Controls', 'Anxious', 'Depressed']
labelGroups=['Controls', 'Anxious', 'Depressed']

print(labels, colors)

def plotSNRPerScan():
	snr_perScan=dict()
	#with open('/space/erebus/1/users/data/scores/snr_output_old.csv', 'r') as csvfile:   #output csv file from: snr_patvscontrol snr()
	with open('/autofs/space/erebus_001/users/data/scores/new2/snr_avg_output_rjj020419.csv','r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:

				s=row[0]
				scan=row[1][:]
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[]]

					if s in control_subjects:
						snr_perScan[scan][0].append(snr)
					elif s in anx_subjects:
						snr_perScan[scan][1].append(snr)
					elif s in dep_subjects:
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
		axarr[i,j].set_ylim((5,30))

		f.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/snr",dpi=199)
		plotted+=1


	plt.show()



def plotSNRAvg():
	snr_perScan=dict()
	with open('/autofs/space/erebus_001/users/data/scores/new/snr_output_newtest.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				s=row[0]
				if "T" in row[1]:
					scan= row[1]
				else:
					scan=row[1][:-1]
				print(scan)
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[]]

					if s in control_subjects:
						snr_perScan[scan][0].append(snr)
					elif s in anx_subjects:
						snr_perScan[scan][1].append(snr)
					elif s in dep_and_anx_subjects or  s in dep_subjects :
						snr_perScan[scan][2].append(snr)

			except:
				print(row)

	sets={3:["T1","T2","Diffusion"],4:["Rest","Gambling","FaceMatching","Conflict"]}
	for sizeFig, scansInFigure  in sets.items():
		f, axarr = plt.subplots(1, sizeFig,figsize=(23,5))
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
		plotted=0

		for scanName, values in snr_perScan.items():
			print (scanName)
			if scanName in scansInFigure:
				axarr[plotted].set_title(scanName)
				for q in range(len(values)):
					violin_parts = axarr[plotted].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
					for pc in violin_parts['bodies']:
						pc.set_facecolor(colors[q])
						pc.set_edgecolor(colors[q])
						pc.set_linewidth(1)
						pc.set_alpha(0.5)
					for partname in ('cbars','cmins','cmaxes','cmeans'):
						vp = violin_parts[partname]
						vp.set_edgecolor(colors[q])
						vp.set_linewidth(1)
				axarr[plotted].set_ylim((0,30))
				axarr[plotted].set_xticks([0,1,2],["Controls","Anxious","Depressed"])


				plotted+=1
		f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr",dpi=199)

		if "T1" in scansInFigure:
			axarr[0].set_ylabel("SNR")
		else:
			axarr[0].set_label("tSNR")

		for ax in axarr.flatten():
			ax.set_xticks([0,1,2])
			ax.set_xticklabels(labels)
		plt.show()
def plotWithinScanMotion():
	perScan=[dict(),dict()]
	tipo="within" #within" #"between"
	labels=["Rotation","Translation"]
	with open('/space/erebus/1/users/data/scores/new/motion_'+tipo+'_scan_output_subj1,140.csv', 'r') as csvfile:
	#with open('//autofs/space/erebus_001/users/data/scores/new/motion_within_scan_output_081918.csv', 'r') as csvfile:
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

					if s in control_subjects:
						perScan[ind][scan][0].append(val)
					elif s in anx_subjects:
						perScan[ind][scan][1].append(val)
					elif s in dep_and_anx_subjects or s in dep_subjects:
						perScan[ind][scan][2].append(val)

			except:
				print(row)

	sets={5:["T1","T2","T1 all vnavs - no reacq", "T2 all vnavs - no reacq","Diffusion"],4:["Rest","Gambling","FaceMatching","Conflict"]}
	for sizeFig, scansInFigure  in sets.items():

		f, axarr = plt.subplots(2, sizeFig,figsize=(23,5))
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

		for i in range(2):
			plotted=0
			for scanName, values in perScan[i].items():
				if scanName in scansInFigure:
					print (scanName)
					axarr[i][plotted].set_title(scanName)
					for q in range(len(values)):
						violin_parts = axarr[i][plotted].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
						for pc in violin_parts['bodies']:
							pc.set_facecolor(colors[q])
							pc.set_edgecolor(colors[q])
							pc.set_linewidth(1)
							pc.set_alpha(0.5)

						for partname in ('cbars','cmins','cmaxes','cmeans'):
							vp = violin_parts[partname]
							vp.set_edgecolor(colors[q])
							vp.set_linewidth(1)
					axarr[i][plotted].set_ylim((0,1))
					axarr[i][plotted].set_ylabel(labels[i])
					axarr[i][plotted].set_xticks([0,1,2],["Controls","Anxious","Depressed"])
					#f.savefig("/space/erebus/1/users/vsiless/QA_plots/"+tipo,dpi=199)
					#f.savefig("/space/erebus/1/users/data/scores/new/plots/"+tipo+"_avg_plot",dpi=199)

					plotted+=1
				for ax in axarr.flatten():
					ax.set_xticks([0,1,2])
					ax.set_xticklabels(["Controls","Anxious","Depressed"])
	plt.tight_layout()
	plt.show()

def plotBetweenScanMotion():
	titles=["Diffusion","Rest","T1-T2","Gambling","FaceMatching","Conflict"]

	perScan=[dict(),dict()]
	tipo="between"
	labels=["Rotation","Translation"]
	with open('/space/erebus/1/users/data/scores/new/motion_'+tipo+'_scan_output_subj1,140.csv', 'r') as csvfile:
	#with open('//autofs/space/erebus_001/users/data/scores/new/motion_within_scan_output_081918.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				s=row[0]
				if "Rotation" in row[1]:
					ind=0
				else:
					ind=1
				if "T" not in row[2]:
					scan=''.join(filter(lambda x: x.isalpha(), row[2]))
				else:
					scan=row[2]
				print(scan)

				val=float(row[3])
				#except:
				#	val=0
				if val>0:
					if not scan in perScan[ind]:
						perScan[ind][scan]=[[],[],[]]

					if s in control_subjects:
						perScan[ind][scan][0].append(val)
					elif s in anx_subjects:
						perScan[ind][scan][1].append(val)
					elif s in dep_and_anx_subjects or s in dep_subjects:
						perScan[ind][scan][2].append(val)

			except:
				print(row)
	sets={2:["T1_T2","DiffusionDiffusion"],4:["RestRest","GamblingGambling","FaceMatchingFaceMatching","ConflictConflict"]}
	labels_sets={"T1_T2":"T1-T2","DiffusionDiffusion":"Diffusion","RestRest":"Rest","GamblingGambling":"Gambling","FaceMatchingFaceMatching":"FaceMatching","ConflictConflict":"Conflict"}
	for sizeFig, scansInFigure  in sets.items():

		f, axarr = plt.subplots(2, sizeFig,figsize=(23,5))
		f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

		for i in range(2):
			plotted=0
			for scanName, values in perScan[i].items():
				if scanName in scansInFigure:
					print (scanName)
					axarr[i][plotted].set_title(labels_sets[scanName])
					for q in range(len(values)):
						violin_parts =axarr[i][plotted].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
						for pc in violin_parts['bodies']:
							pc.set_facecolor(colors[q])
							pc.set_edgecolor(colors[q])
							pc.set_linewidth(1)
							pc.set_alpha(0.5)
						for partname in ('cbars','cmins','cmaxes','cmeans'):
							vp = violin_parts[partname]
							vp.set_edgecolor(colors[q])
							vp.set_linewidth(1)

					axarr[i][plotted].set_ylim((0,25))
					axarr[i][plotted].set_ylabel(labels[i])
					axarr[i][plotted].set_xticks([0,1,2],["Controls","Anxious","Depressed"])
					#f.savefig("/space/erebus/1/users/vsiless/QA_plots/"+tipo,dpi=199)
					#f.savefig("/space/erebus/1/users/data/scores/new/plots/"+tipo+"_avg_plot",dpi=199)

					plotted+=1
				for ax in axarr.flatten():
					ax.set_xticks([0,1,2])
					ax.set_xticklabels(["Controls","Anxious","Depressed"])
	plt.show()


def subjectsHistograms():
	objects = ('Controls', 'Anxious', 'Depressed')
	y_pos = np.arange(len(objects))
	performance = [len(control_subjects),len(anx_subjects), len(dep_and_anx_subjects)+len(dep_subjects)]

	plt.bar(y_pos, performance, .35, align='center', color=['#74c7a5', '#FF8600','#36649E'] )
	plt.xticks(y_pos, objects)
	plt.ylabel('subjects')

	plt.show()

def ContinuousScoresHisto():
	subjects, sex, scores = utils.loadBANDAscores(outliers)

	for key, score in scores.items():
		plt.figure(key)
		# example data
		num_bins = 5
		# the histogram of the data
		n, bins, patches = plt.hist(score, num_bins, normed=1, facecolor='blue', alpha=0.5)

	plt.show()

def ContinuousScores():
	subjects, sex, scores = utils.loadBANDAscores(outliers)
	first=True
	for key, score in scores.items():
		plt.figure(key)
		# example data
		num_bins = 5
		for i,s in enumerate(score):
			c = colors[0]


			if subjects[i] in control_subjects:
				c=colors[0]
			elif subjects[i] in anx_subjects:
				c=colors[1]
			elif subjects[i] in dep_and_anx_subjects or subjects[i] in dep_subjects:
				c=colors[2]

			plt.scatter(i,s, color=c, label=labelGroups[colors.index(c)])

		plt.ylabel(key)
		plt.xlabel("subject")

		if key is "SHAPS_CNT":
			plt.ylabel("SHAPS > 2 = Anehedonia ")
			plt.plot(range(0,140), [2.5]*140, '--', color='black')

		if first:
			first=False
			handles, labels = plt.gca().get_legend_handles_labels()
			by_label = OrderedDict(zip(labels, handles))
		plt.legend(by_label.values(), by_label.keys())
	plt.show()
def plotSNRContinuousMeasures():
	snr_perScan=dict()
	with open('/autofs/space/erebus_001/users/data/scores/new/snr_output_newtest.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				s=row[0]
				if "T" in row[1]:
					scan= row[1]
				else:
					scan=row[1][:-1]
				print(scan)
				snr=float(row[2])
				if snr>0:
					if not scan in snr_perScan:
						snr_perScan[scan]=[[],[],[]]

					if s in control_subjects:
						snr_perScan[scan][0].append((snr,s))
					elif s in anx_subjects:
						snr_perScan[scan][1].append((snr,s))
					elif s in dep_and_anx_subjects or s in dep_subjects:
						snr_perScan[scan][2].append((snr,s))

			except:
				print(row)

	subjects, sex, scores = utils.loadBANDAscores(outliers)
	sets={3:["T1","T2","Diffusion"],4:["Rest","Gambling","FaceMatching","Conflict"]}
	for sizeFig, scansInFigure  in sets.items():

		for key, score in scores.items():
			#plt.figure(key)
			if key in ["BIS","BAS","MFQ","SHAPS_CNT"]:
				f, axarr = plt.subplots(1, sizeFig,figsize=(23,3))
				#f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
				plotted=0
				print(key)
				for scanName, categories in snr_perScan.items():

					if scanName in scansInFigure:
						axarr[plotted].set_title(scanName)
						for q in range(len(categories)):
							for snr,sub in categories[q]:
								if sub in subjects:
									try:
										axarr[plotted].scatter(score[subjects.index(sub)], snr, color=colors[q], label=labelGroups[q]) #,showmedians=True)
									except:
										print(sub)
						axarr[plotted].set_xlabel(key)
						if "T1" in scansInFigure:
							axarr[0].set_ylabel("SNR")
						else:
							axarr[0].set_ylabel("tSNR")
						if key is "SHAPS_CNT":
							axarr[plotted].set_xlabel("SHAPS > 2 = Anehedonia ")
							axarr[plotted].plot( [2.5]*30, range(0,30), '--', color='black')
						plotted+=1


	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = OrderedDict(zip(labels, handles))
	plt.legend(by_label.values(), by_label.keys())
	plt.tight_layout()
	plt.show()
def plotWithinScanMotionContinuousMeasures():
	perScan=[dict(),dict()]
	tipo="within" #within" #"between"
	labelsY=["Rotation","Translation"]
	#colors=[ 'green','violet','cyan']
	#labels=['Controls', 'Anxious', 'Depressed']

	with open('/space/erebus/1/users/data/scores/new/motion_'+tipo+'_scan_output_subj1,140.csv', 'r') as csvfile:
	#with open('//autofs/space/erebus_001/users/data/scores/new/motion_within_scan_output_081918.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				if "vnav" not in  row[2]:
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
					if val>0:
						if not scan in perScan[ind]:
							perScan[ind][scan]=[[],[],[]]

						if s in control_subjects:
							perScan[ind][scan][0].append((val,s))
						elif s in anx_subjects:
							perScan[ind][scan][1].append((val,s))
						elif s in dep_subjects:
							perScan[ind][scan][2].append((val,s))

			except:
				print(row)

	subjects, sex, scores = utils.loadBANDAscores(outliers)
	sets={3:["T1","T2","Diffusion"],4:["Rest","Gambling","FaceMatching","Conflict"]}
	for sizeFig, scansInFigure  in sets.items():

		for key, score in scores.items():

			if key in ["BIS","BAS","MFQ","SHAPS_CNT"]:
				f, axarr = plt.subplots(2, sizeFig,figsize=(23,5))
				f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

				for i in range(2):
					#f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
					plotted=0

					for scanName, categories in perScan[i].items():
						print (scanName)
						if scanName in scansInFigure:
							axarr[i][plotted].set_title(scanName)
							#print(categories)
							for q in range(len(categories)):
								for snr,sub in categories[q]:
									if sub in subjects:
										try:
											axarr[i][plotted].scatter(score[subjects.index(sub)], snr, color=colors[q], label=labelGroups[q]) #,showmedians=True)
										except:
											print(sub)
							axarr[i][plotted].set_xlabel(key)
							axarr[i][plotted].set_ylabel(labelsY[i])

							axarr[i][plotted].set_ylim(0,1)

							#axarr[plotted].set_xticks([0,1,2,3],["Controls","Anxious","Comorbid","Depressed"])
							#f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr",dpi=199)
							if key is "SHAPS_CNT":
								axarr[i][plotted].set_xlabel("SHAPS > 2 = Anehedonia ")
								axarr[i][plotted].plot( [2.5]*30, range(0,30), '--', color='black')

							plotted+=1
				f.tight_layout()
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = OrderedDict(zip(labels, handles))
	plt.legend(by_label.values(), by_label.keys())
	plt.tight_layout()
	plt.show()


def plotBetweenScanMotionContinuousMeasures():
	#subjects, subject_lbl = utils.getBandaLabels(outliers)

	perScan=[dict(),dict()]
	tipo="between" #within" #"between"
	labelsY=["Rotation","Translation"]
	#colors=[ 'green','violet','cyan']
	#labels=['Controls', 'Anxious', 'Depressed']
	titles=["Diffusion","Rest","T1-T2","Gambling","FaceMatching","Conflict"]
	with open('/space/erebus/1/users/data/scores/new2/motion_'+tipo+'_scan_output_140.csv', 'r') as csvfile:
	#with open('//autofs/space/erebus_001/users/data/scores/new/motion_within_scan_output_081918.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			try:
				if "vnav" not in  row[2]:
					s=row[0]
					if "Rotation" in row[1]:
						ind=0
					else:
						ind=1
					if "T" not in row[2]:
						scan=''.join(filter(lambda x: x.isalpha(), row[2]))
					else:
						scan=row[2]
					print(scan)


					val=float(row[3])
					if val>0:
						if not scan in perScan[ind]:
							perScan[ind][scan]=[[],[],[]]

						if s in control_subjects:
							perScan[ind][scan][0].append((val,s))
						elif s in anx_subjects:
							perScan[ind][scan][1].append((val,s))
						elif s in dep_subjects:
							perScan[ind][scan][2].append((val,s))

			except:
				print(row)

	subjects, sex, scores = utils.loadBANDAscores(outliers)
	sets={2:["T1_T2","DiffusionDiffusion"],4:["RestRest","GamblingGambling","FaceMatchingFaceMatching","ConflictConflict"]}
	labels_sets={"T1_T2":"T1-T2","DiffusionDiffusion":"Diffusion","RestRest":"Rest","GamblingGambling":"Gambling","FaceMatchingFaceMatching":"FaceMatching","ConflictConflict":"Conflict"}
	for sizeFig, scansInFigure  in sets.items():

		for key, score in scores.items():

			if key in ["BIS","BAS","MFQ","SHAPS_CNT"]:
				#plt.figure(key)
				f, axarr = plt.subplots(2, sizeFig,figsize=(23,5))
				f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

				for i in range(2):
					#f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)
					plotted=0

					for scanName, categories in perScan[i].items():
						if scanName in scansInFigure:
							print (scanName)
							axarr[i][plotted].set_title(labels_sets[scanName])
							#print(categories)
							for q in range(len(categories)):
								for snr,sub in categories[q]:
									if sub in subjects:
										try:
											axarr[i][plotted].scatter(score[subjects.index(sub)], snr, color=colors[q], label=labelGroups[q]) #,showmedians=True)
										except:
											print(sub)
							axarr[i][plotted].set_xlabel(key)
							axarr[i][plotted].set_ylabel(labelsY[i])

							if key is "SHAPS_CNT":
								axarr[i][plotted].set_xlabel("SHAPS > 2 = Anehedonia ")
								axarr[i][plotted].plot( [2.5]*30, range(0,30), '--', color='black')

							plotted+=1
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = OrderedDict(zip(labels, handles))
	plt.legend(by_label.values(), by_label.keys())
	plt.tight_layout()
	plt.show()

#subjectsHistograms()
#ContinuousScores()

#plotSNRAvg()
#plotSNRContinuousMeasures()

#plotWithinScanMotion()
#plotBetweenScanMotion()

plotWithinScanMotionContinuousMeasures()
#plotBetweenScanMotionContinuousMeasures()


#ContinuousScores()
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


"""
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

			#if "T1" in scan or "T2" in scan or "Diffusion" in scan:
			#	axarr[i,j].set_yticks([0,1,2,3])
			#else:
			#	axarr[i,j].set_yticks([0,0.1,0.2])

			f.savefig("/space/erebus/1/users/vsiless/QA_plots/snr_plots_patvscontrol",dpi=199)
		plotted+=1
	#mng = plt.get_current_fig_manager()
	#mng.full_screen_toggle()

	plt.show()
	#f.savefig("/space/erebus/1/users/vsiless/snr_20",dpi=199)
	"""
