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


def WASI(premade_output = None):

    outliers=["BANDA071", "BANDA070","BANDA005","BANDA045","BANDA025","BANDA067","BANDA069","BANDA002","BANDA017","BANDA041","BANDA043","BANDA063","BANDA010","BANDA023","BANDA036","BANDA050","BANDA059","BANDA054","BANDA013","BANDA042","BANDA031","BANDA022"]#,"BANDA031"] #,"BANDA063"] #,"BANDA064"] #"BANDA061","BANDA062","BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA031","BANDA005","BANDA054","BANDA058","BANDA045"] #"BANDA029","BANDA009","BANDA033","BANDA038","BANDA039","BANDA048","BANDA057","BANDA061","BANDA065","BANDA028","BANDA021","BANDA031","BANDA067","BANDA069","BANDA070","BANDA004","BANDA005","BANDA014","BANDA024","BANDA034","BANDA044","BANDA043","BANDA052","BANDA049", 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA068', 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA047']
    subjects,info, scores = utils.loadBANDA(outliers)
    age= info['age']
    sex=info['gender']
    wasi=info['wasi']
    hand=info['hand']
    print(wasi)
    for key, score in scores.items():
        f, axarr = plt.subplots(1,1,figsize=(23,14))
        #f.tight_layout()
        f.subplots_adjust(left=.03, bottom=.06, right=.97, top=.95, wspace=.18, hspace=.30)

        axarr.set_title(str(key))
        #for calculating axis ranges
        y_values = []
        x_values = []
        
        X=np.array([])
        #for s in subjects:
        for s_index,s in enumerate(subjects):
            
            axarr.plot(score[s_index], wasi[s_index], "o",markersize=5, c='m')

            y_values.append(wasi[s_index])	
            x_values.append(score[s_index])
            if key != 'Anhedonia':
                X=np.append(X,[[1,score[s_index]]])
            else:
                if score[s_index]>2:
                    X=np.append(X,[[1,0]])
                else:
                    X=np.append(X,[[0,1]])
        
        #regression lines
        (sl,b) = polyfit(x_values,y_values, 1)
        yp = polyval([sl,b],x_values)
        axarr.plot(x_values,yp,'-',color='r')
        #GLM
        
        if key != 'Anhedonia':
            cval = np.hstack((0, -1))
        else:
            cval = np.hstack((1, -1))
        X= np.array(X).reshape(len(y_values),2)
        Y=np.array(y_values )
        
        model = GeneralLinearModel(X)
        model.fit(Y)
        z_vals = model.contrast(cval).p_value() # z-transformed statistics
        print(key, z_vals)

        axarr.set_ylabel("Average SNR")
        axarr.set_xlabel(str(key))

        #axarr.set_xlim(xmin_value-(np.median(x_values)*.30),xmax_value+(np.median(x_values)*.30))
        #axarr.set_ylim(ymin_value-(np.median(y_values)*.30),ymax_value+(np.median(y_values)*.30))


        #f.savefig("/space/erebus/1/users/jwang/comparisonPlots_1_63/plots/motion_snr/snr_avg_"+str(key),dpi=199)
    plt.show()

WASI()