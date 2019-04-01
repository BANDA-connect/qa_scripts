#author: Viviana Siless - vsiless@mgh.harvard.edu
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
def vNavRead(folder, protocol, sequence, outputCom, outputScore):
	dicoms = glob.glob(folder+'/MR*')

	#plt.figure("vnavs")

	vnavsT1=[]
	vnavsT2=[]
	vnavsT1Score=[]
	vnavsT2Score=[]
	vnavsT1Comms=[]
	vnavsT2Comms=[]

	vNav=0
	vNav2=0
	f = open(outputCom, 'w')

	for d in dicoms:
		dcm =dicom.read_file(d)
		if dcm.ProtocolName == protocol and dcm.SequenceName==sequence:
			quat=dcm.ImageComments.split()
			if vNav ==0 and len(vnavsT1Score)>1:
				vnavsT1Score=[]
			vnavsT1Comms.append(str(dcm.AcquisitionNumber)+ " " + dcm.ImageComments)
			if int(dcm.AcquisitionNumber) >1 :

				vnavsT1.append(np.array([float(quat[1]),float(quat[2]),float(quat[3]),float(quat[4]),float(quat[6]),float(quat[7]),float(quat[8])]))
				if len(vnavsT1)>1:
					vnavsT1Score.append(getvNavScore(vnavsT1))	
					print (vnavsT1Comms[len(vnavsT1Comms)-2] ,"vnav score:", vnavsT1Score[len(vnavsT1Score)-1])
					f.write(str(vnavsT1Comms[len(vnavsT1Comms)-2]) + "vnav score:" + str(vnavsT1Score[len(vnavsT1Score)-1])+"\n")
				vNav+=1			

			else:
				vnavsT1.append(np.array([0.0,1.0,0.0,0.0,0.0,0.0,0.0]))
				vnavsT1Score.append(getvNavScore(vnavsT1))	
				print (vnavsT1Comms[len(vnavsT1Comms)-2], "vnav score:",vnavsT1Score[len(vnavsT1Score)-1])
				f.write(str(vnavsT1Comms[len(vnavsT1Comms)-2] )+ "vnav score:"+str(vnavsT1Score[len(vnavsT1Score)-1])+"\n")
				vNav=0				
	f.close()

	f = open(outputScore, 'w')
	f.write(str(vnavsT1Score).replace("[","").replace("]",""))
	f.close()

	#plt.plot(range(len(vnavsT1Score)),vnavsT1Score)
	#plt.set_xlabel('TR (T1)')
	#plt.set_ylabel('vnav score')

	#plt.legend(ncol=3)	
		
	#plt.show()

def dummyTest():
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

vNavRead("/autofs/cluster/gerenuk/user/andre/T2-SPACE_vNav_comparison/Prisma_fit-67026-20170530-172631-001981/","T2w_SPC_vNav_mo_nomoco", "ABCD3d1_32ns", "/cluster/scratch/friday/viv/T2w_SPC_vNav_mo_nomoco_comments.csv", "/cluster/scratch/friday/viv/T2w_SPC_vNav_mo_nomoco_score.csv")
#readVNavsScoreFiles()
