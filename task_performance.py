import csv
import numpy as np
import glob
import matplotlib
#print matplotlib.get_cachedir()
import matplotlib.pyplot as plt

subjects = ["BANDA001","BANDA002","BANDA003","BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013"]
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

mode=["Practice","Scanner"]

f, axarr = plt.subplots(2, 3)

for m in mode:
	axarr[mode.index(m),2].set_title("Conflict "+m)
	values=[[],[],[],[]]
	for s in subjects:
		files = glob.glob('/space/erebus/1/users/data/tfMRI_output/'+s+'/'+s+'_'+m+'*_conflict*.csv')
		#print files
		correct=0
		
		if len(files)>0:
			with open(files[-1]) as csvfile:
				reader = csv.DictReader(csvfile)
				total=0
				for row in reader:
					pressed = np.array(row['PressedKeys'].replace("]","").replace("[","").replace("'","").split(":"))
					if row['correctResponse'] == 'IDENTICAL':
						answer=row['responseKeySAME']
					else:
						answer=row['responseKeyDIFFERENT']
					answer=answer.replace("]","").replace("[","").replace("'","")
					try:
						if int(pressed[-1]) == int(answer) :
							correct +=1
						total+=1
					except:
						if row['TrialsInRun.thisTrialN'].isdigit() :
							#print "no answer", pressed[-1]	
							total+=1
				correct = float(correct)/total
				if correct>0:
					if s in control_subjects:
						values[0].append(correct)
					elif s in anx_subjects:
						values[1].append(correct)
					elif s in dep_and_anx_subjects:
						values[2].append(correct)
					elif s in dep_subjects:
						values[3].append(correct)
				#print(values)
		
	for q in range(len(values)):
		print(values[q])
		axarr[mode.index(m),2].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
	axarr[mode.index(m),2].set_ylim((0,1.1))
	axarr[mode.index(m),2].set_ylabel("Correct answers rate")
	axarr[mode.index(m),2].set_xticks([0,1,2,3],["Controls","Anxious","Comorbid","Depressed"])
		
	for ax in axarr.flatten():
		ax.set_xticks([0,1,2,3])
		ax.set_xticklabels(["Controls","Anxious","Comorbid","Depressed"])

		
	axarr[mode.index(m),0].set_title("Gambling "+m)
	values=[[],[],[],[]]
	for s in subjects:
		files = glob.glob('/space/erebus/1/users/data/tfMRI_output/'+s+'/'+s+'_'+m+'*_Gambling*.csv')
		#print files
		answered=0
		if len(files)>0:
			with open(files[-1]) as csvfile:
				reader = csv.DictReader(csvfile)
				total=0
				for row in reader:
					pressed = row['allPressedKeys'].replace("]","").replace("[","").replace("'","").split(":")
					try:
						if int(pressed[-1]) in [1,2,8,9] :
							answered +=1
						total+=1	
					except:
						if row['current_trial.thisN'].isdigit() :
							#print "no answer", pressed[-1]	
							total+=1
	
				correct = float(answered)/total

				if correct>0:
					if s in control_subjects:
						values[0].append(correct)
					elif s in anx_subjects:
						values[1].append(correct)
					elif s in dep_and_anx_subjects:
						values[2].append(correct)
					elif s in dep_subjects:
						values[3].append(correct)
					#print(values)
		
	for q in range(len(values)):
		print(values[q])
		axarr[mode.index(m),0].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
	axarr[mode.index(m),0].set_ylim((0,1.1))
	axarr[mode.index(m),0].set_ylabel("Correct answers rate")
	axarr[mode.index(m),0].set_xticks([0,1,2,3],["Controls","Anxious","Comorbid","Depressed"])
		
	for ax in axarr.flatten():
		ax.set_xticks([0,1,2,3])
		ax.set_xticklabels(["Controls","Anxious","Comorbid","Depressed"])

	axarr[mode.index(m),1].set_title("faceMatching "+m)
	values=[[],[],[],[]]
	for s in subjects:
		files = glob.glob('/space/erebus/1/users/data/tfMRI_output/'+s+'/'+s+'_'+m+'*_FaceMatching*.csv')
		#print files
		correct=0
		if len(files)>0:
			with open(files[-1]) as csvfile:
				reader = csv.DictReader(csvfile)
				total=0
				for row in reader:
					
					pressed = np.array(row['allPressedKeys'].replace("]","").replace("[","").replace("'","").split(":"))
					answer_R=row['corr_ans'].replace("]","").replace("[","").replace("'","")
					answer_L=row['corr_ans_Left'].replace("]","").replace("[","").replace("'","")
					#print answer_R, answer_L
					try:

						if float(pressed[-1]) == float(answer_L) or float(pressed[-1]) == float(answer_R):
							correct +=1
						total +=1	
						#print row['allPressedKeys']
						#print total
					except:
						if row['trials.thisN'].isdigit() :
							#print "no answer"
							total +=1					
						#else:
						#print row['allPressedKeys']
				if correct >0:
					correct = float(correct)/total

					if s in control_subjects:
						values[0].append(correct)
					elif s in anx_subjects:
						values[1].append(correct)
					elif s in dep_and_anx_subjects:
						values[2].append(correct)
					elif s in dep_subjects:
						values[3].append(correct)
				#print(values)
		
	for q in range(len(values)):
		print(values[q])
		axarr[mode.index(m),1].violinplot(values[q], [q], points=20, widths=0.3, showmeans=True) #,showmedians=True)
	axarr[mode.index(m),1].set_ylim((0,1.1))
	axarr[mode.index(m),1].set_ylabel("Correct answers rate")
	axarr[mode.index(m),1].set_xticks([0,1,2,3],["Controls","Anxious","Comorbid","Depressed"])
		
	for ax in axarr.flatten():
		ax.set_xticks([0,1,2,3])
		ax.set_xticklabels(["Controls","Anxious","Comorbid","Depressed"])
plt.show()

