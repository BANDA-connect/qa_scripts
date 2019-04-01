#/space/erebus/1/users/jwang/jon2/bin/python3.6 diffusion_plots.py

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

output="/space/erebus/1/users/data/comparisonPlots_1_88/"
output="/space/erebus/1/users/banda/plots"
matplotlib.rcParams.update({'font.size': 18})
def diffusion_measures(premade_output = None):
	measures = {'FA':-2,'MD':-5,'RD':-8,'AD':-11}

	#if premade_output == None:
		#diffusion_output=csv.writer(open('/space/erebus/1/users/data/scores/diffusion_output.csv','w+'))
		#diffusion_output.writerow(['subject','measure','structure','score','questionnaire','questionnaire_score'])

	outliers=['BANDA014','BANDA034','BANDA050','BANDA054','BANDA059','BANDA062','BANDA067','BANDA073','BANDA077','BANDA079','BANDA080','BANDA081','BANDA082','BANDA094','BANDA099','BANDA106']
#'BANDA014', 'BANDA032', 'BANDA033','BANDA034','BANDA050','BANDA031','BANDA051','BANDA054','BANDA059','BANDA062','BANDA067','BANDA069','BANDA070','BANDA071','BANDA073','BANDA076','BANDA077','BANDA078','BANDA079','BANDA080','BANDA081',"BANDA082","BANDA083",'BANDA089','BANDA087','BANDA088','BANDA090']#'BANDA031',"BANDA032","BANDA033","BANDA034","BANDA050","BANDA054","BANDA059","BANDA062","BANDA067","BANDA069","BANDA070","BANDA076","BANDA077","BANDA078","BANDA071","BANDA073",
#"BANDA079","BANDA081","BANDA080","BANDA082","BANDA083","BANDA086","BANDA087","BANDA088", "BANDA089","BANDA090"]#'BANDA014','BANDA031',"BANDA032","BANDA033","BANDA034","BANDA035","BANDA036","BANDA037","BANDA038","BANDA039","BANDA040",
#"BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049",
#"BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060", "BANDA061", "BANDA062", "BANDA063","BANDA067"
#"BANDA014","BANDA031","BANDA032",
#"BANDA033","BANDA034","BANDA035","BANDA036","BANDA037","BANDA038","BANDA039","BANDA040",
#"BANDA041","BANDA042","BANDA043","BANDA044","BANDA045","BANDA046","BANDA047","BANDA048","BANDA049",
#"BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060", "BANDA061", "BANDA062", "BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA072","BANDA073","BANDA074"]	
	subjects, info, scores = utils.loadBANDA(outliers)
	age= info['age']
	sex=info['gender']
	wasi=info['wasi']
	hand=info['hand']

	paths = {'Left CST':'lh.cst_AS_avg33_mni_bbr','Right CST':'rh.cst_AS_avg33_mni_bbr','Left ILF':'lh.ilf_AS_avg33_mni_bbr', 'Right ILF':'rh.ilf_AS_avg33_mni_bbr','Left UF':'lh.unc_AS_avg33_mni_bbr','Right UF':'rh.unc_AS_avg33_mni_bbr','CC Forceps Major':'fmajor_PP_avg33_mni_bbr','CC Forceps minor':'fminor_PP_avg33_mni_bbr','Left ATR':'lh.atr_PP_avg33_mni_bbr','Right ATR':'rh.atr_PP_avg33_mni_bbr','Left CAB':'lh.cab_PP_avg33_mni_bbr','Right CAB':'rh.cab_PP_avg33_mni_bbr','Left CCG':'lh.ccg_PP_avg33_mni_bbr','Right CCG':'rh.ccg_PP_avg33_mni_bbr','Left SLF - parietal':'lh.slfp_PP_avg33_mni_bbr','Right SLF - parietal':'rh.slfp_PP_avg33_mni_bbr','Left SLF - temporal':'lh.slft_PP_avg33_mni_bbr','Right SLF - temporal':'rh.slft_PP_avg33_mni_bbr'}	

	for key, score in scores.items():
		for measure_index, measure in enumerate(measures): 
			f, axarr = plt.subplots(3,6,figsize=(45,20))
			#f.tight_layout()

			if key=='Anhedonia':
				boxplot_data = [[[],[]]for i in range(18)]
				#box plot measures
				g, boxarr = plt.subplots(3,6,figsize=(45,20))

			plotted = 0
			for name in paths:
				#for calculating axis ranges
				ymin_value = 0
				ymax_value = 0
				xmin_value = 0
				xmax_value = 0
				x_values = []
				y_values = []
				#print (measures)
				#print (measure)
				#print (measures[measure])

				j = plotted%6
				i = int(plotted/6)
				axarr[i,j].set_title(name)
				if key == 'Anhedonia': boxarr[i,j].set_title(name)
				for s_index,s in enumerate(subjects):
					if premade_output ==None: 
						print (s)
						text_files = glob.glob('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/dpath/'+paths[name]+'/pathstats.overall.txt')
						#print ('/space/erebus/1/users/data/preprocess/FS/MGH_HCP/'+s+'/dpath/'+paths[name]+'/pathstats.overall.txt')	
						#print (text_files)				
						line = open(text_files[0],'r').readlines()[measures[measure]]
						#print(line)
						#n = line.strip('FA_Avg_Weight ' + '\n')
						n = line[14:]
						#print(n)
						#n = line.strip('MD_Avg_Weight ' + '\n')
						#n = line.strip('RD_Avg_Weight ' + '\n')
						#n = line.strip('AD_Avg_Weight ' + '\n')
						y = float(n)
						x = float(score[s_index])
						#diffusion_output.writerow([s,measure,name,y,key,x])

					else:
						with open('/space/erebus/1/users/data/scores/diffusion_output.csv', 'r') as output:
							output_reader = csv.DictReader(output, delimiter = ",")
							for row in iter(output_reader):
								skip = 0
								#print (row['subject'],s,key)
								if str(row['subject'])==s:
									if str(row['questionnaire'])==key:
										if measure == row['measure']:
											if name == row['path']:
												y = float(row['avg_score'])
												x = float(row['questionnaire_score'])
												break
									else:
										if skip > 0:skip+= 70
										else: skip+=69
										for i in range(skip):
											next(iter(output_reader))
				
					#print(s, key, x,y)
					axarr[i,j].plot(x, y, "o",markersize=5, c='m')

					x_values.append(x)
					y_values.append(y)
					


					if s_index == 0: ymin_value = y
					ymin_value = min(ymin_value,y)
					ymax_value = max(ymax_value,y)

					if s_index == 0: xmin_value = x
					xmin_value = min(xmin_value,x)
					xmax_value = max(xmax_value,x)

					if key=='Anhedonia':
						if float(x)<3: boxplot_data[j+i*6][0].append(y)	
						else: boxplot_data[j+i*6][1].append(y)	
						


				if key == 'Anhedonia':
					x_1 = [g for g in x_values if g>=3]
					x_2 = [g for g in x_values if g<3]			
					#regression lines
					(sl,b) = polyfit(x_1,y_values[-len(x_1):], 1)
					yp = polyval([sl,b],x_1)
					axarr[i,j].plot(x_1,yp,'-',color='g')

					#regression lines
					(sl,b) = polyfit(x_2,y_values[:len(x_2)], 1)
					yp = polyval([sl,b],x_2)
					axarr[i,j].plot(x_2,yp,'-',color='b')

				else:
					#regression lines
					(sl,b) = polyfit(x_values,y_values, 1)
					yp = polyval([sl,b],x_values)
					axarr[i,j].plot(x_values,yp,'-',color='r')

				X  = np.ones(len(x_values))	
				X =np.stack((X, x_values), axis=-1)
				Y=np.array(y_values)
		
				cval = np.hstack((0, 1))
				model = GeneralLinearModel(X)
				model.fit(Y)
				z_vals = model.contrast(cval).p_value() # z-transformed statistics
				#print(key,"+", z_vals)

				z_vals = model.contrast(cval*-1).p_value() # z-transformed statistics
				#print(key,"-", z_vals)

				axarr[i,j].set_ylabel("Average " + measure + " Score")
				axarr[i,j].set_xlabel(str(key))

				axarr[i,j].set_xlim(xmin_value-(np.median(x_values)*.30),xmax_value+(np.median(x_values)*.30))
				axarr[i,j].set_ylim(ymin_value-(np.median(y_values)*.30),ymax_value+(np.median(y_values)*.30))
				#print (i,j)
				#print (xmin_value, measure, xmin_value*.30)
				plotted+=1

				if key == 'Anhedonia':
					box_max_list = [max(a) for a in boxplot_data[j+i*6]]
					box_min_list = [min(a) for a in boxplot_data[j+i*6]]
					boxarr[i,j].set_ylabel("Average " + measure + " Score")
					boxarr[i,j].set_ylim(min(box_min_list)-.25,max(box_max_list)+.25)
					boxarr[i,j].boxplot(boxplot_data[j+i*6],labels=['no anhedonia','anhedonia'])

			plt.subplots_adjust(left=.03, bottom=.06, right=.99, top=.95, wspace=.25, hspace=.32)
			#plt.show()
			f.savefig("/space/erebus/1/users/data/comparisonPlots_1_114/diffusion/diff_"+str(measure)+"_"+str(key),dpi=199)
			if key == 'Anhedonia': g.savefig("/space/erebus/1/users/data/comparisonPlots_1_114/diffusion/diffusion_"+str(measure)+"Anhedonia_boxplot",dpi=199)
diffusion_measures()
