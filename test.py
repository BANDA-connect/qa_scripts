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

def vNavRead():

	#subjects = ["BANDA050","BANDA051","BANDA052","BANDA053","BANDA054","BANDA055","BANDA056","BANDA057","BANDA058","BANDA059","BANDA060"]
	#subjects = ["BANDA004","BANDA005","BANDA006","BANDA007","BANDA008","BANDA009","BANDA010","BANDA011","BANDA012","BANDA013", "BANDA014", "BANDA015"]
	#subjects = ["BANDA092","BANDA093","BANDA094","BANDA095","BANDA096","BANDA097","BANDA098","BANDA099", "BANDA100","BANDA101","BANDA102","BANDA103","BANDA104","BANDA105","BANDA106","BANDA107","BANDA108","BANDA109", "BANDA110","BANDA111","BANDA112","BANDA113","BANDA114","BANDA115","BANDA116","BANDA117","BANDA118","BANDA119"]
	#,"BANDA088","BANDA089","BANDA090","BANDA091",]
	#subjects = ["BANDA138","BANDA139","BANDA140"]
	subjects = ["BANDA002"] #,"BANDA139","BANDA140"]
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
				print( dcm.AcquisitionNumber, dcm.ImageComments)				
				"""if int(dcm.AcquisitionNumber) >1 :

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
					vNav2=0"""

		print (vnavsT1Score)
		print (vnavsT2Score)
		print(s, "T1", sum(np.array(vnavsT1Score)>0.5))
		print(s, "T2", sum(np.array(vnavsT2Score)>0.5))

vNavRead()
