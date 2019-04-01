import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import minimize
from scipy.misc import factorial
from scipy.optimize import curve_fit, least_squares
from matplotlib import colors as mcolors
from os import mkdir, getcwd, path
import nibabel as nib
from scipy import stats
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
import statistics
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
by_name =[ name for name, color in colors.items()]

from sklearn import linear_model
from matplotlib.backends.backend_pdf import PdfPages
import sys
sys.path.insert(0, '/space/erebus/1/users/data/code/scripts/')
sys.path.insert(0, '/space/erebus/2/users/vsiless/lifespan-mgh/scripts/')
import matplotlib
matplotlib.rcParams.update({'font.size': 10})
import anatomiCutsUtils as utilete
import ecor_grant as ecor
import utils
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
import numpy as np
import subprocess


def surfaceAndShapeDNA():
    outliers=["BANDA071", "BANDA070","BANDA005","BANDA045","BANDA025","BANDA067","BANDA069","BANDA002","BANDA017","BANDA041","BANDA043","BANDA063","BANDA010","BANDA023","BANDA036","BANDA050","BANDA059","BANDA054","BANDA013","BANDA042","BANDA031","BANDA022"]#,"BANDA031"] #,"BANDA063"] #,"BANDA064"] #"BANDA061","BANDA062","BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA031","BANDA005","BANDA054","BANDA058","BANDA045"] #"BANDA029","BANDA009","BANDA033","BANDA038","BANDA039","BANDA048","BANDA057","BANDA061","BANDA065","BANDA028","BANDA021","BANDA031","BANDA067","BANDA069","BANDA070","BANDA004","BANDA005","BANDA014","BANDA024","BANDA034","BANDA044","BANDA043","BANDA052","BANDA049", 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA068', 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA047']
    subjects,info, scores = utils.loadBANDA(outliers)
    age= info['age']
    sex=info['gender']
    wasi=info['wasi']
    hand=info['hand']
    for i, s in enumerate(subjects):
        print(s,sex[i],age[i], scores['Anhedonia'][i])


    s1="BANDA001"
    toMeshBin="/autofs/space/rama_002/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/StreamlinesToMesh"
    folder="AnatomiCuts_long55_dwi"
    
    specificNode="1110110"
    specificChilds, specificParents = utilete.readTree(50, "/space/erebus/1/users/data/preprocess/"+s1+"/"+folder+"/HierarchicalHistory.csv")
    
    #tracts=["1110110","1111110"] 
    
    allowedNodes=[]
    numClusters=200
    allowedNodes=specificChilds[specificNode]
    childs, parents =utilete.readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/"+folder+"/HierarchicalHistory.csv")
    print(allowedNodes)
    
    allowedNodes=["1000000","1001110","10101111","1100010010","1100100111","110100010", "110110010","1101110110","111001000","1110110011","1111010100","1111101010"]
    for i,k in enumerate(allowedNodes):
        output=k
       
        subprocess.call("cd /space/rama/2/users/vsiless/code/commons/shapeDNA-tria/", shell=True)
        
        for s2 in subjects:
            try:
                childs2, parents2 =utilete.readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s2+"/"+folder+"/HierarchicalHistory.csv")
                correspondance  =  "/space/erebus/1/users/data/preprocess/"+s2+"/Hungarian_AnatomiCuts_long55_dwi/"+s1+"_"+s2+"_c"+str(numClusters)+"_labels_hungarian.csv"
                
                correspondancesLabels=utilete.getCorrespondingClusters(correspondance,False)
                print (correspondancesLabels[k])
                stringy0="mkdir -p /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output
                stringy1 =toMeshBin+" /space/erebus/1/users/data/preprocess/"+s2+"/"+folder+"/images/"+correspondancesLabels[k]+".nii.gz /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk 2 100000 3 3"
                stringy2="/space/rama/2/users/vsiless/code/commons/shapeDNA-tria/triaIO --infile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --outfile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --smooth 2"
                stringy3="/autofs/space/rama_002/users/vsiless/code/commons/shapeDNA-tria/shapeDNA-tria --mesh /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --num 500 --reducecomp --outfile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk-500.ev"
                stringy4="/autofs/space/rama_002/users/vsiless/code/commons/shapeDNA-tria/shapeDNA-tria --mesh /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --num 1000 --reducecomp --outfile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk-1000.ev"
                stringy5="/autofs/space/rama_002/users/vsiless/code/commons/shapeDNA-tria/shapeDNA-tria --mesh /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --num 100 --reducecomp --outfile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk-100.ev"
                stringy6="/autofs/space/rama_002/users/vsiless/code/commons/shapeDNA-tria/shapeDNA-tria --mesh /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --num 5 --reducecomp --outfile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk-5.ev"
                stringy7="/autofs/space/rama_002/users/vsiless/code/commons/shapeDNA-tria/shapeDNA-tria --mesh /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk --num 50 --reducecomp --outfile /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".vtk-5.ev"
                stringy8="cp /space/erebus/1/users/data/preprocess/"+s2+"/"+folder+"/images/"+correspondancesLabels[k]+".nii.gz  /space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s2+".nii.gz"
                stringy="pbsubmit -c '"+stringy0+";"+stringy1+";"+stringy2+";"+stringy3+";"+stringy4+";"+stringy5+";"+stringy6+";"+stringy7+";"+stringy8+";'"
                #stringy=stringy0+";"+stringy1+";"+stringy2+";"+stringy3+";"+stringy4+";"+stringy5+";"+stringy6
                subprocess.call(stringy, shell=True)

            except Exception as inst:
                print (inst           )# __str__ allows args to be printed directly

    #print(np.shape(EVs)    )
    #print(EVs)


def copyVTKs():
    outliers=["BANDA071", "BANDA070","BANDA005","BANDA045","BANDA025","BANDA067","BANDA069","BANDA002","BANDA017","BANDA041","BANDA043","BANDA063","BANDA010","BANDA023","BANDA036","BANDA050","BANDA059","BANDA054","BANDA013","BANDA042","BANDA031","BANDA022"]#,"BANDA031"] #,"BANDA063"] #,"BANDA064"] #"BANDA061","BANDA062","BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA031","BANDA005","BANDA054","BANDA058","BANDA045"] #"BANDA029","BANDA009","BANDA033","BANDA038","BANDA039","BANDA048","BANDA057","BANDA061","BANDA065","BANDA028","BANDA021","BANDA031","BANDA067","BANDA069","BANDA070","BANDA004","BANDA005","BANDA014","BANDA024","BANDA034","BANDA044","BANDA043","BANDA052","BANDA049", 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA068', 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA047']
    subjects,info, scores = utils.loadBANDA(outliers)
    s1="BANDA001"
    toMeshBin="/autofs/space/rama_002/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/StreamlinesToMesh"
    folder="AnatomiCuts_long55_dwi"
    
    specificNode="1110110"
    specificChilds, specificParents = utilete.readTree(50, "/space/erebus/1/users/data/preprocess/"+s1+"/"+folder+"/HierarchicalHistory.csv")
    
    #tracts=["1110110","1111110"] 
    
    allowedNodes=[]
    numClusters=200
    allowedNodes=specificChilds[specificNode]
    childs, parents =utilete.readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/"+folder+"/HierarchicalHistory.csv")
    print(allowedNodes)
    
    allowedNodes=["1000000","1001110","10101111","1100010010","1100100111","110100010", "110110010","1101110110","111001000","1110110011","1111010100","1111101010"]
    for i,k in enumerate(allowedNodes):
        output=k
       
        subprocess.call("cd /space/rama/2/users/vsiless/code/commons/shapeDNA-tria/", shell=True)
        
        for s2 in subjects:
            try:
                childs2, parents2 =utilete.readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s2+"/"+folder+"/HierarchicalHistory.csv")
                correspondance  =  "/space/erebus/1/users/data/preprocess/"+s2+"/Hungarian_AnatomiCuts_long55_dwi/"+s1+"_"+s2+"_c"+str(numClusters)+"_labels_hungarian.csv"
                
                correspondancesLabels=utilete.getCorrespondingClusters(correspondance,False)
                print (correspondancesLabels[k])
                stringy0="mkdir -p /space/erebus/1/users/data/preprocess/shapeDNA/clusters/"+folder+"/"+output
                stringy =stringy0 + "; cp /space/erebus/1/users/data/preprocess/"+s2+"/"+folder+"/"+correspondancesLabels[k]+".vtk /space/erebus/1/users/data/preprocess/shapeDNA/clusters/"+folder+"/"+output+"/"+s2+".vtk"
                subprocess.call(stringy, shell=True)

            except Exception as inst:
                print (inst           )# __str__ allows args to be printed directly

    #print(np.shape(EVs)    )
    #print(EVs)

def plotShapeDNADistances():
    plt.tight_layout()
    outliers=[] #"BANDA071", "BANDA070","BANDA005","BANDA045","BANDA025","BANDA067","BANDA069","BANDA002","BANDA017","BANDA041","BANDA043","BANDA063","BANDA010","BANDA023","BANDA036","BANDA050","BANDA059","BANDA054","BANDA013","BANDA042","BANDA031","BANDA022"]#,"BANDA031"] #,"BANDA063"] #,"BANDA064"] #"BANDA061","BANDA062","BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA031","BANDA005","BANDA054","BANDA058","BANDA045"] #"BANDA029","BANDA009","BANDA033","BANDA038","BANDA039","BANDA048","BANDA057","BANDA061","BANDA065","BANDA028","BANDA021","BANDA031","BANDA067","BANDA069","BANDA070","BANDA004","BANDA005","BANDA014","BANDA024","BANDA034","BANDA044","BANDA043","BANDA052","BANDA049", 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA068', 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA047']
    subjects,info, scores = utils.loadBANDA(outliers)
    age= info['age']
    sex=info['gender']
    wasi=info['wasi']
    hand=info['hand']
    for i, s in enumerate(subjects):
        print(s,sex[i],age[i], scores['Anhedonia'][i])


    s1="BANDA001"
    toMeshBin="/autofs/space/rama_002/users/vsiless/code/vivs/aire-branches/aire_diffregistration/bin/StreamlinesToMesh"
    folder="AnatomiCuts_long55_dwi"
    
    specificNode="1111110"
    specificChilds, specificParents = utilete.readTree(50, "/space/erebus/1/users/data/preprocess/"+s1+"/"+folder+"/HierarchicalHistory.csv")
    
    #tracts=["1110110","1111110"] 
    
    allowedNodes=[]
    numClusters=200
    allowedNodes=specificChilds[specificNode]
    childs, parents =utilete.readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/"+folder+"/HierarchicalHistory.csv")
    print(allowedNodes)

    cvs=[]
    eigenvalues=[100] #,500,1000]
    #ferr, axarr = plt.subplots(rows,columns)
    allowedNodes=['111111000', '111111001', '111111010', '111111011','11101101', '1110110000', '1110110001', '1110110010', '1110110011']
    allowedNodes=["1000000","1001110","10101111","1100010010","1100100111","110100010", "110110010","1101110110","111001000","1110110011","1111010100","1111101010"]

    for score  in scores:
        ferr, axarr = plt.subplots(4,len(allowedNodes))
    
        for evNumber in eigenvalues:
            for i,k in enumerate(allowedNodes):
        
                output=k
                xx=[]
                yy=[]
                y=[]
                yyy=[]
                yyyy=[]
                axarr[0,i].set_title(k)
                for j, s1 in enumerate(subjects):
                    try: 
                        ev1, vol = ecor.getEigenvalues("/space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s1+".vtk-"+str(evNumber)+".ev")
                        print(vol)
                        #image = nib.load("/space/erebus/1/users/data/preprocess/shapeDNA/"+folder+"/"+output+"/"+s1+".nii.gz").get_data()
                        #image/=image.max()
                        #image= np.ceil(image)
                        #vol =np.sum(image)  
                        #ev1/=ev1[1]
                        normVol= math.sqrt(sum((ev1*vol**2/3)**2))
                        normEV1=math.sqrt(sum((ev1/ev1[1])**2))
                        #anhe=scores['Anhedonia'][j]
                        anhe=scores[score][j]
                        """if scores['Anhedonia'][j] >2:
                            anhe=1
                        else:
                            anhe=0
                        """
                        #plt.scatter(1,ev1[1]) #sum(ev1)/(len(ev1)-1 ))
                        axarr[0,i].scatter(anhe,normVol) 
                        axarr[1,i].scatter(anhe,vol )

                        axarr[2,i].scatter(anhe,normEV1) 
                        axarr[3,i].scatter(anhe,ev1[1] )
                        xx.append(anhe)
                        
                        #yy.append(ev1[1]) #sum(ev1)/(len(ev1)-1 ))
                        yy.append(normVol)
                        y.append(vol)
                        yyy.append(ev1[1])
                        yyyy.append(normEV1)
                    except Exception as inst:
                        print (inst           )# __str__ allows args to be printed directly
                    
                    
           

                fitted=np.poly1d(np.polyfit(xx, yy, 1))(np.unique(xx))
                axarr[0,i].plot(np.unique(xx), fitted, linewidth=2.0,color="black")
                axarr[0,i].plot(np.unique(xx),[fitted[0]]*len(np.unique(xx)),'--',linewidth=2.0,color="black")

                
                fitted=np.poly1d(np.polyfit(xx, y, 1))(np.unique(xx))
                axarr[1,i].plot(np.unique(xx), fitted, linewidth=2.0,color="black")
                axarr[1,i].plot(np.unique(xx),[fitted[0]]*len(np.unique(xx)),'--',linewidth=2.0,color="black")

                fitted=np.poly1d(np.polyfit(xx, yyyy, 1))(np.unique(xx))
                axarr[2,i].plot(np.unique(xx), fitted, linewidth=2.0,color="black")
                axarr[2,i].plot(np.unique(xx),[fitted[0]]*len(np.unique(xx)),'--',linewidth=2.0,color="black")


                fitted=np.poly1d(np.polyfit(xx, yyy, 1))(np.unique(xx))
                axarr[3,i].plot(np.unique(xx), fitted, linewidth=2.0,color="black")
                axarr[3,i].plot(np.unique(xx),[fitted[0]]*len(np.unique(xx)),'--',linewidth=2.0,color="black")


        axarr[0,0].set_ylabel("ev.vol^(2/3)")
        axarr[1,0].set_ylabel("vol")
        axarr[2,0].set_ylabel("ev/ev1")
        axarr[3,0].set_ylabel("ev1")
        for i in range(9):
            for j in range(4):
                axarr[j,i].set_xticks([0,1])
                axarr[j,i].set_xticklabels(["HC",score])    
        plt.legend()   
        
    plt.show()
def ecorGrantTest():
    ev1, vol = ecor.getEigenvalues("/space/erebus/1/users/data/preprocess/shapeDNA/AnatomiCuts_long55_dwi/1101110110/BANDA064.vtk-100.ev")
    ev1 = ev1*vol**2/3
    ev2, vo2 = ecor.getEigenvalues("/space/erebus/1/users/data/preprocess/shapeDNA/AnatomiCuts_long55_dwi/1101110110/BANDA014.vtk-100.ev")
    ev2 = ev2*vo2**2/3
   
    print(math.sqrt(sum((ev1-ev2)**2)))
    
    ev1, vol = ecor.getEigenvalues("/space/erebus/1/users/data/preprocess/shapeDNA/AnatomiCuts_long55_dwi/111001000/BANDA004.vtk-100.ev")
    ev1 = ev1*vol**2/3
    ev2, vo2 = ecor.getEigenvalues("/space/erebus/1/users/data/preprocess/shapeDNA/AnatomiCuts_long55_dwi/1100010010/BANDA006.vtk-100.ev")
    ev2 = ev2*vo2**2/3
   
    print(math.sqrt(sum((ev1-ev2)**2)))
ecorGrantTest()   
#plotShapeDNADistances()
"""stringy=""
for i in range(72,100):
    stringy+=" BANDA0"+str(i)
for i in range(100,107):
    stringy+=" BANDA"+str(i)
print(stringy)"""
#surfaceAndShapeDNA()
#copyVTKs()