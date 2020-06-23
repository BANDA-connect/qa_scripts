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
import matplotlib.patches as mpatches
import csv
import utils


def getValues(inFile, xColumn,lineIndex, acq_time,ref, toMillimeters=None):
	prevValues =[]
	volumes=1
	all_tra = [ ]
	tra = [0,0,0]
	absol = [0,0,0]
	linei=0
	iind=0
	with open(inFile) as motionFile:
		for line in motionFile:
			if linei >= lineIndex[0] and linei <lineIndex[len(lineIndex)-1] :

				values =  line.split()
				if linei == lineIndex[iind]:
					tra_i = [0,0,0]
					if len(prevValues )>5:
						for i in range(xColumn, xColumn+3):
							if toMillimeters is None:
								tra_i[i-xColumn] = math.fabs(float(values[i])-float(prevValues[i]))
							else:
								tra_i[i-xColumn] = math.fabs(float(toMillimeters(float(values[i])))-float(toMillimeters(float(prevValues[i]))))
								#tra_i[i-xColumn] = math.fabs(float(toMillimeters(math.fabs(float(values[i])-float(prevValues[i])))))

							tra[i-xColumn]+= tra_i[i-xColumn]
						all_tra.append(tra_i) 		
						volumes +=1
					iind+=1
				if linei==ref or ref<0:
					prevValues = values
				if linei==lineIndex[0]:
					for i in range(xColumn, xColumn+3):
						absol[i-xColumn]= float(values[i])
						#absol[i-xColumn]= tra_i[i-xColumn])
			if lineIndex[-1] <= iind:
				break
			linei+=1
	return (tra, volumes*acq_time, np.array(absol), np.array(all_tra))

def getTranslation(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None, avg=True):

	tra = getValues( inFile,xColumn,lineIndex,acq_time,ref)
	tra2=[0,0,0]
	if not inFile2 ==None :
		tra2 = getValues( inFile2,xColumn,lineIndex2,acq_time,ref)
		res = np.array(tra[2]) - np.array(tra2[2])
	else:
		res= np.array(tra[0])/tra[1]


	if avg:
		print("avg tra")
		return math.sqrt(sum(res**2)) #/tra[1]
	else:	#this only works for within
		return tra

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

def radiansToMillimeters(value):
	return value*50


def getRotationMillimeters(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None, avg=True):
	col= 0 if xColumn == 3 else 3

	rot =getValues(inFile,col,lineIndex,acq_time,ref) #, radiansToMillimeters)
	rot2=[0,0,0]
	if not inFile2 ==None :
		rot2 = getValues( inFile2,col,lineIndex2,acq_time,ref)
		res = np.absolute(np.array(rot[2]) - np.array(rot2[2]))
	else:
		res= np.array(rot[0])/rot[1]
	if avg:
		print("avg")
		return math.sqrt(sum(res**2)) #/tra[1]
	else: #this only works for within 
		return rot

def getFD(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None, avg=False):
	rot = getRotationMillimeters(inFile, xColumn, lineIndex, acq_time, ref, avg=False)[3]
	trans = getTranslation(inFile, xColumn, lineIndex, acq_time, ref, avg=False)[3]
	if not inFile2 ==None :
		rot2 = getRotationMillimeters(inFile2, xColumn, lineIndex2, acq_time, ref, avg=False)[3]
		trans2 = getTranslation(inFile2, xColumn, lineIndex2, acq_time, ref, avg=False)[3]

		return radiansToMillimeters(sum(np.absolute(rot-rot2)))+sum(np.absolute(trans-trans2))

	else:
		c=0
		for i in range(len(rot)):
			val = (radiansToMillimeters(sum(rot[i])) + sum(trans[i]))
			c+= val**2
		print(math.sqrt(c/len(rot)))
		return math.sqrt(c/len(rot))

def getFramewiseThreashold(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None):
	rot = getRotationMillimeters(inFile, xColumn, lineIndex, acq_time, ref,inFile2, lineIndex2,avg=False)[3]
	trans = getTranslation(inFile, xColumn, lineIndex, acq_time, ref,inFile2, lineIndex2, avg=False)[3]
	c=0

	for i in range(len(rot)):
		#val = math.sqrt(sum(rot[i]**2 + trans[i]**2))
		val = (radiansToMillimeters(sum(rot[i])) + sum(trans[i]))
		if val >.9:
			c = 1 +c
			#print(radiansToMillimeters(sum(rot[i])),sum(trans[i]))
			#print(val)
	print(c)
	return c


def getTranslationAbsolute(inFile, xColumn,lineIndex,acq_time,ref=0):
	return getTranslation( inFile,xColumn,lineIndex,acq_time,ref)


def getRotationAbsolute(inFile, xColumn,lineIndex,acq_time,ref=0):
	return getRotation(inFile,xColumn,lineIndex,acq_time,ref)

def getFileData(fileN):
	if "dMRI" in fileN:
		column =0
		acq_time=3.230
	elif "T1" in fileN:
		column=3
		acq_time=2.400
	elif "T2" in fileN:
		column=3
		acq_time=3.200
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
	for m in metric:
		for name  in scans:
			index=[0,1000]
			for f in glob.glob("directory/file.par"):
				f = getFilePath(fileN,s)
				ind = range(index[0], index[1])
				column =3
				acq_time=.8 #TR
				t=  m(f,column,np.sort(ind),acq_time)
				plt.plot(subjects_lbl['allsubjects'].index(s)+1, t, "o", c='r')

				#fg.savefig("/autofs/space/erebus_001/users/data/scores/new2/plots/motion_within_scan_patvscontrol"+m,dpi=199)
	plt.show()


subjects=["subject1", "subject2"]

metric = [getFramewiseThreashold, getFD,  getTranslation, getRotation] #, getFD] #, getTranslationAbsolute, getRotationAbsolute]
#metric = [ getTranslation, getRotation] #, getFD] #, getTranslationAbsolute, getRotationAbsolute]
metric_label=["FDT","FD","Rotation ($\degree/s$)", "Absolute translation per second", "Absolute rotation per second",]

plotWithinScanMotion()
