import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import minimize
from scipy.misc import factorial
from scipy.optimize import curve_fit, least_squares
from matplotlib import colors as mcolors
from scipy.stats import sem
from os import mkdir, getcwd, path
import nibabel as nib
from scipy import stats
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
by_name =[ name for name, color in colors.items()]
from sklearn import linear_model
from matplotlib.backends.backend_pdf import PdfPages
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
import numpy as np
import utils
from nipy.modalities.fmri.glm import GeneralLinearModel
import statsmodels.api as sm


import numpy as np
from nipy.modalities.fmri.glm import GeneralLinearModel
import matplotlib

matplotlib.rcParams.update({'font.size': 18})    
def getDict(archivo, withHeader):
    #print(archivo)
    fas =dict()
    with open(archivo, 'r') as csvfile:
        corReader= csv.reader(csvfile, delimiter=',', quotechar='|')	
        header=withHeader
        for row in corReader:
            if not header and len(row)>1:
                #print(row[0].replace(" ","").replace("//","/").split("/")[-1].replace("trk",""),row[1])
                fas[row[0].replace(" ","").replace("//","/").split("/")[-1].replace(".trk","")]= float(row[1])
            else:
                header=False
    return fas

def correspondingMeasures():
    outliers=["BANDA079","BANDA072","BANDA071", "BANDA070","BANDA005","BANDA045","BANDA025","BANDA067","BANDA069","BANDA002","BANDA017","BANDA041","BANDA043","BANDA063","BANDA010","BANDA023","BANDA036","BANDA050","BANDA059","BANDA054","BANDA013","BANDA042","BANDA031","BANDA022"]#,"BANDA031"] #,"BANDA063"] #,"BANDA064"] #"BANDA061","BANDA062","BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA031","BANDA005","BANDA054","BANDA058","BANDA045"] #"BANDA029","BANDA009","BANDA033","BANDA038","BANDA039","BANDA048","BANDA057","BANDA061","BANDA065","BANDA028","BANDA021","BANDA031","BANDA067","BANDA069","BANDA070","BANDA004","BANDA005","BANDA014","BANDA024","BANDA034","BANDA044","BANDA043","BANDA052","BANDA049", 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA068', 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA047']
    subjects,info, scores = utils.loadBANDA(outliers)
    age= info['age']
    sex=info['gender']
    wasi=info['wasi']
    hand=info['hand']
    for i, s in enumerate(subjects):
        print(s,sex[i],age[i], scores['Anhedonia'][i])

    measures=["FA","MD","RD","AD"]
    s1="BANDA001"
    columns=4
    rows=1
    numClusters=200
    specificNode="" #1110110" #1111110" #1111110" #1110110" #1110110" # #1111110" #1111110"
    specificChilds, specificParents = readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/HierarchicalHistory.csv")
    allowedNodes=[]
    if specificNode!= "":
        print("hola")
        numClusters=200
        allowedNodes=specificChilds[specificNode]
    childs, parents = readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/HierarchicalHistory.csv")
    print(allowedNodes)
    nodesNames=[]
   
    for key, score in scores.items():
        ferr, axarr = plt.subplots(rows,columns)
        for count, ev in enumerate(measures):
            FAs=[]
            #s1_fas  =  getDict("/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv", True)
            
            s1_fas  =  getFADictLevels("/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv", True, childs, parents)
            #print(s1_fas)
            for s2 in subjects[1:]:
                
                index =0
                correspondance = "/space/erebus/1/users/data/preprocess/"+s2+"/Hungarian_AnatomiCuts_long55_dwi/"+s1+"_"+s2+"_c"+str(numClusters)+"_labels_hungarian.csv"
                
                childs2, parents2 = readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s2+"/AnatomiCuts_long55_dwi/HierarchicalHistory.csv")
                #s2_fas  =  getDict("/space/erebus/1/users/data/preprocess/"+s2+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv",True)
                s2_fas  =  getFADictLevels("/space/erebus/1/users/data/preprocess/"+s2+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv", True, childs2, parents2)
                print(s2_fas)
                print("/space/erebus/1/users/data/preprocess/"+s2+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv")
                with open(correspondance, 'r') as csvfile:
                    corReader= csv.reader(csvfile, delimiter=',', quotechar='|')	
                    header=True
                    for row in corReader:
                        if not header and len(row)>1:
                            #print(row[0])
                            if len(FAs) <numClusters and (len(allowedNodes)==0 or ( row[0] in allowedNodes and len(FAs)< len(allowedNodes))):
                                FAs.append([s1_fas[row[0]]])
                                if len(nodesNames)<numClusters:
                                    nodesNames.append(row[0])
                            #print(index)
                            if (len(allowedNodes)==0 or row[0] in allowedNodes):
                                print(s2_fas[row[1]])
                                FAs[index].append(s2_fas[row[1]])
                            
                                index+=1
                        else:
                            header = False

            #mfqs= np.array(mfqs)
            FAs = np.array(FAs)
            #print(len(FAs))
            if key !='Anhedonia':     
                for i in range(len(FAs)):
                    params = utils.createParams()
                    minner = Minimizer(utils.fitting, params, fcn_args=(score,sex,"linear",FAs[i]))
                    result = minner.minimize() 

                    #report_fit(result)
                    if np.mean(np.abs(result.residual)) <100:
                        y_fit = utils.fitting(result.params,np.unique(score),[],"linear" ) 
                        num_col = len(by_name)

                        axarr[count].plot(np.unique(score),y_fit,color=by_name[i%num_col],  label='fit')
                        axarr[count].scatter(score,FAs[i],color=by_name[i%num_col],  label='fit')
                        axarr[count].set_ylabel(ev)
                        axarr[count].set_xlabel(key)

                init=0
                #numClusters=200
                Y=np.array([])
                X=np.array([])
                for j in range(len(FAs[0])):
                    x=[]
                    y=[]
                    for i in range(init, len(FAs)):
                        y.append(FAs[i][j])        
                    if len(y)>0:
                        X=np.append(X,[[1,score[j]]])
                        if( len(Y)==0):
                            Y=y
                        else:
                            #print(np.shape(Y), np.shape(y))
                            Y= np.vstack((Y,[y]))
              
                X= np.array(X).reshape(len(Y),2)
                Y=np.array(Y)
              
                cval = np.hstack((0, -1))
                model = GeneralLinearModel(X)
                model.fit(Y)
                p_vals = model.contrast(cval).p_value() # z-transformed statistics
                print(key, ev, p_vals)
                for index, p in enumerate(p_vals):
                    if p*len(FAs) <0.05:
                        print (nodesNames[index],p*len(FAs))
                #print(np.shape(X), np.shape(Y))
                #gauss_log = sm.GLM(Y, X) #, family=sm.families.Gaussian(sm.families.links.log))
                #gauss_log_results = gauss_log.fit()
                #print(gauss_log_results.summary())
                #print(p_value)
            else:
                #print(ev,len(FAs[0]),len(FAs[:][0]),len(FAs[0][:]))
                sex_anh=[]
                sex_no_anh=[]
                age_anh=[]
                age_no_anh=[]
                wasi_anh=[]
                wasi_no_anh=[]
                hand_anh=[]
                hand_no_anh=[]
                yes=[]
                no=[]
                no2=[]
                no_anh=[]
                anh=[]
                #print(score)
                init=0
                #numClusters=200
                for i in range(init,len(FAs)):
                    yes.append([])
                    no.append([])
                    no2.append([])
                Y=np.array([])
                X=np.array([])
                print(len(FAs[0]))
                for j in range(len(FAs[0])):
                    elems=[]
                    x=[]
                    y=[]
                    for i in range(init, len(FAs)):
                        elems.append(FAs[i][j])
                        if score[j]<=2 and score[j]>=0:
                            no[i-init].append(FAs[i][j])
                            y.append(FAs[i][j])  
                            axarr[count].scatter([i+1],[FAs[i][j]],color='#53868B',alpha=0.1)
                            
                        elif score[j]>2:
                            yes[i-init].append(FAs[i][j])
                            y.append(FAs[i][j])  
                            axarr[count].scatter([i+1],[FAs[i][j]],color='#FF7F24', alpha=0.1)
                            
                        
                        # else:
                        #    print(score[j])      
                    if len(y)>0:
                        if  score[j]<=2 and score[j]>=0:
                            no_anh.append(elems)
                            
                            sex_no_anh.append(sex[j])
                            age_no_anh.append(age[j])
                            wasi_no_anh.append(wasi[j])
                            hand_no_anh.append(hand[j])
                            regression=[1,0,sex[j]]
                            
                            
                        elif score[j]>2:
                            anh.append(elems)
                            
                            regression=[0,1,sex[j]]
                            sex_anh.append(sex[j])
                            age_anh.append(age[j])
                            wasi_anh.append(wasi[j])
                            hand_anh.append(hand[j])
                        if( len(Y)==0):
                            Y=y
                        else:
                            #print(np.shape(Y), np.shape(y))
                            Y= np.vstack((Y,[y]))

                        if sex[j]==1:
                            regression.append(1)
                        else:
                            regression.append(0)
                        regression.append(age[j])
                            

                        X=np.append(X,[regression])
                print(len(no_anh),len(anh)) 
                #X=np.append(X,np.array(x))
                axarr[count].errorbar(range(1,len(FAs)+1),np.mean(no, axis=1),yerr=sem(no, axis=1),label='Withuot Anhedonia',fmt='o', color='#53868B')
                axarr[count].errorbar(range(1,len(FAs)+1),np.mean(yes, axis=1),yerr=sem(yes, axis=1),label='With Anhedonia',fmt='o', color='#FF7F24')
                axarr[count].set_ylabel(ev)
                axarr[count].set_xlabel("Sub-cluster index")
                axarr[count].set_xticks(range(1,len(FAs)+1)) #[1,10,20,30,40,50]) #range(1,len(FAs)+1))
                if ev=="AD":
                    axarr[count].set_ylim(.7,.9)
                
                axarr[count].set_title("Cluster 1") #range(1,len(FAs)+1))
                
                axarr[0].legend()
                print("Non anhedonia : female rate ", np.mean(sex_no_anh), " mean age " ,np.mean( age_no_anh), " mean wasi " ,np.mean( wasi_no_anh)," mean hand " ,np.mean( hand_no_anh))
                print("Anhedonia : female rate ", np.mean(sex_anh), " mean age " ,np.mean( age_anh), " mean wasi " ,np.mean( wasi_anh)," mean hand " ,np.mean( hand_anh))
                
                #print(np.shape(no_anh), np.shape(anh), len(yes[0]),len(no[0]))
                #print ("N"+ev+"=",str(no_anh[0:14]).strip().replace(",","").replace("]) array([",";").replace("[array(","").replace(")]","").replace("\n"," ").replace("] [",";").replace("[[","[").replace("]]","]"))
                #print ("N2=",str(no_anh[15:29]).strip().replace(",","").replace("]) array([",";").replace("[array(","").replace(")]","").replace("\n"," ").replace("] [",";").replace("[[","[").replace("]]","]"))
                #print ("A"+ev+"=",str(anh).strip().replace(",","").replace("]) array([",";").replace("[array(","").replace(")]","").replace("\n"," ").replace("] [",";").replace("[[","[").replace("]]","]"))
                """t-test
                t,p= stats.ttest_ind(no_anh, anh)
                print(ev,t,p, len(p))
              
                #slope, intercept, r_value, p_value, std_err = stats.linregress(y,x)
                """

                """
                nobs2 = 100
                x = np.arange(nobs2)
                np.random.seed(54321)
                X = np.column_stack((x,x**2))
                X = sm.add_constant(X, prepend=False)
                lny = np.exp(-(.03*x + .0001*x**2 - 1.0)) + .001 * np.random.rand(nobs2)
                gauss_log = sm.GLM(lny, X, family=sm.families.Gaussian(sm.families.links.log))
                
                """
                X= np.array(X).reshape(len(Y),5)
                Y=np.array(Y)
                #print(np.shape(X), np.shape(Y))
                #gauss_log = sm.GLM(Y, X) #, family=sm.families.Gaussian(sm.families.links.log))
                #gauss_log_results = gauss_log.fit()
                #print(gauss_log_results.summary())
                #print(p_value)
                
                cval = np.hstack((-1, 1,0,0,0))
                model = GeneralLinearModel(X)
                model.fit(Y)
                p_vals = model.contrast(cval).p_value() # z-transformed statistics
                print(key, ev, p_vals)
                for index, p in enumerate(p_vals):
                    if p*len(FAs) <0.05:
                        print (nodesNames[index],p*len(FAs), p, index)

                cval = np.hstack((1, -1,0,0,0))
                model = GeneralLinearModel(X)
                model.fit(Y)
                p_vals = model.contrast(cval).p_value() # z-transformed statistics
                print(key, ev, p_vals)
                for index, p in enumerate(p_vals):
                    if p*len(FAs) <0.05:
                        print (nodesNames[index],p*len(FAs),p,index)

    plt.show()
def saveMeasurementsFile(subjects, indices, filename, scores, allowedNodes,measures,values):
    with open(filename,'w') as csvfile:
        writer =  csv.writer(csvfile,delimiter=",", quotechar="|",quoting=csv.QUOTE_MINIMAL)
        header=["Subject"]
        for b in measures:
            for a in allowedNodes:
                header.append(b+a)
            #header.append(b)
        header.append("Anhedonia")
        print(header)
        writer.writerow(header)    
        for k in indices:
            s=subjects[k]
            row=[s]
            for i in range(len(measures)):
                for j in range(len(allowedNodes)):
                    row.append(values[i][j][k])
                #print(len(values[i][k]))
                #row.append(np.mean(np.array(values)[i,:,k]))
            row.append(1 if scores['Anhedonia'][k]>3 else 0)
            #print(s)
            #print(row)
            writer.writerow(row)
def predictionDictionary(subjects,indices, scores, allowedNodes,measures,values):
    prediction = dict()
    for b in measures:
        for a in allowedNodes:
            prediction[b+a]=[]
    for k in indices:
        s=subjects[k]
        print(s)
        for i,b in enumerate(measures):
            for j,a  in enumerate(allowedNodes):
                prediction[b+a].append(values[i][j][k])
        print(1 if scores['Anhedonia'][k]>3 else 0)
        
    print(prediction)
def gatherData():
    outliers=["BANDA079","BANDA070","BANDA071","BANDA045","BANDA005", "BANDA080"] #, "BANDA070","BANDA005","BANDA045","BANDA025","BANDA067","BANDA069","BANDA002","BANDA017","BANDA041","BANDA043","BANDA063","BANDA010","BANDA023","BANDA036","BANDA050","BANDA059","BANDA054","BANDA013","BANDA042","BANDA031","BANDA022"]#,"BANDA031"] #,"BANDA063"] #,"BANDA064"] #"BANDA061","BANDA062","BANDA063","BANDA064","BANDA065","BANDA066","BANDA067","BANDA068","BANDA069","BANDA070","BANDA071","BANDA031","BANDA005","BANDA054","BANDA058","BANDA045"] #"BANDA029","BANDA009","BANDA033","BANDA038","BANDA039","BANDA048","BANDA057","BANDA061","BANDA065","BANDA028","BANDA021","BANDA031","BANDA067","BANDA069","BANDA070","BANDA004","BANDA005","BANDA014","BANDA024","BANDA034","BANDA044","BANDA043","BANDA052","BANDA049", 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA068', 'BANDA054', 'BANDA056', 'BANDA058', 'BANDA059', 'BANDA062', 'BANDA066', 'BANDA047']
    subjects,info, scores = utils.loadBANDA(outliers)
    age= info['age']
    sex=info['gender']
    wasi=info['wasi']
    hand=info['hand']
    for i, s in enumerate(subjects):
        print(s,sex[i],age[i], scores['Anhedonia'][i])

    measures=["FA","MD","RD","AD"]
    s1="BANDA001"
    columns=4
    rows=1
    numClusters=50
    specificNode=["1110110" ,"1111110" ] ##1111110" #1110110" #1110110" # #1111110" #1111110"
    specificChilds, specificParents = readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/HierarchicalHistory.csv")
    allowedNodes=[]
    if specificNode!= "":
        #print("hola")
        numClusters=200
        for a in specificNode:
            allowedNodes+=specificChilds[a]
    allowedNodes= np.array(allowedNodes).reshape(-1)
    print(allowedNodes)

    childs, parents = readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/HierarchicalHistory.csv")
    nodesNames=[]
    values =[] 
    #for key, score in scores.items():
    #    ferr, axarr = plt.subplots(rows,columns)
    for count, ev in enumerate(measures):
        FAs=[]
        s1_fas  =  getFADictLevels("/space/erebus/1/users/data/preprocess/"+s1+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv", True, childs, parents)
        for s2 in subjects[1:]:
            index =0
            correspondance = "/space/erebus/1/users/data/preprocess/"+s2+"/Hungarian_AnatomiCuts_long55_dwi/"+s1+"_"+s2+"_c"+str(numClusters)+"_labels_hungarian.csv"
            childs2, parents2 = readTree(numClusters, "/space/erebus/1/users/data/preprocess/"+s2+"/AnatomiCuts_long55_dwi/HierarchicalHistory.csv")
            s2_fas  =  getFADictLevels("/space/erebus/1/users/data/preprocess/"+s2+"/AnatomiCuts_long55_dwi/measures/"+ev+".csv", True, childs2, parents2)
            with open(correspondance, 'r') as csvfile:
                corReader= csv.reader(csvfile, delimiter=',', quotechar='|')	
                header=True
                for row in corReader:
                    if not header and len(row)>1:
                        if len(FAs) <numClusters and (len(allowedNodes)==0 or ( row[0] in allowedNodes and len(FAs)< len(allowedNodes))):
                            FAs.append([s1_fas[row[0]]])
                            if len(nodesNames)<numClusters:
                                nodesNames.append(row[0])
                        if (len(allowedNodes)==0 or row[0] in allowedNodes):
                            FAs[index].append(s2_fas[row[1]])
                            index+=1
                    else:
                        header = False
        values.append(np.array(FAs))
    #print(np.shape(values))
    saveMeasurementsFile(subjects, range(12,70), "/space/erebus/1/users/data/preprocess/anatomicuts_values_train.csv", scores, allowedNodes,measures,values)
    saveMeasurementsFile(subjects, list(range(2,12))+list(range(70,80)), "/space/erebus/1/users/data/preprocess/anatomicuts_values_test.csv", scores, allowedNodes,measures,values)
    predictionDictionary(subjects, list(range(0,2))+list(range(80,83)), scores, allowedNodes,measures,values)
       
        
def getFADictLevels(faFile, withHeader, childs, parent, corr=None):
    #print(faFile)
    fas =dict()
    norms =dict()
    with open(faFile, 'r') as csvfile:
        corReader= csv.reader(csvfile, delimiter=',', quotechar='|')	
        header=withHeader
        for row in corReader:
            if not header:
                cluster=row[0].replace(" ","").replace("//","/")
                cluster=cluster.split("/")[-1].split(".trk")[0]
                #print(cluster)
                if corr != None:
                    cluster = corr[cluster]
                #cluster = int(clusterN.split("/")[-1].split(".")[0])
                #cluster = int(clusterN) # int(clusterN.split("/")[-1].split(".")[0])
                #print(cluster)
                if cluster in childs:
                    fas[cluster]= float(row[1]) # *float(row[4])
                    norms[cluster] = 1 #float(row[4])
                elif cluster in parent:
                    if parent[cluster] in fas:
                        fas[parent[cluster]] +=float(row[1]) #* float(row[4])
                        norms[parent[cluster]] += 1 #float(row[4])
                    else:
                        fas[parent[cluster]] =float(row[1]) # *float(row[4])
                        norms[parent[cluster]] = 1 #float(row[4])
            else:
                header=False

    for k in fas:
        fas[k] /= norms[k]

    return fas
def readTree(numNodes, hierarchicalHisto):
    almostFoundAllClusters=False
    foundAllClusters=False
    nodes_childs=dict()
    whos_dad=dict()

    header=True
    with open(hierarchicalHisto, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')	
        clusters=set()
           
        for row in reader:
            if not header :
                if not foundAllClusters:
                    try:
                        if row[0] in clusters:
                            clusters.remove(row[0])
                        clusters.add(row[1])
                        if len(clusters)==numNodes :
                            foundAllClusters=True
                            for i in clusters:
                                nodes_childs[i]=[]
                            
                    except:
                        None
                else:
                        if row[0] in whos_dad :
                            dad = whos_dad[row[0]]
                            if row[0] in nodes_childs[dad]:
                                nodes_childs[dad].remove(row[0])
                            nodes_childs[dad].append(row[1])
                            whos_dad[row[1]]=dad	
                        else:
                            nodes_childs[row[0]].append(row[1])
                            whos_dad[row[1]]=row[0]
            else:
                header=False
    return nodes_childs, whos_dad

#correspondingMeasures()
gatherData()