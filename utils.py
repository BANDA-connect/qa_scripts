#/space/erebus/1/users/jwang/jon2/bin/python3.6
import numpy as np
import csv
from scipy.optimize import minimize
from scipy.misc import factorial
from scipy.optimize import curve_fit, least_squares
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
import sys
import math
import glob
import os.path
import matplotlib
print( matplotlib.get_cachedir())
import matplotlib.pyplot as plt
import dicom
from numpy import linalg as LA
from pyquaternion import Quaternion
import matplotlib.patches as mpatches
import csv

def getBandaDiagnosis(outliers=[]):
    labelfile = "/autofs/space/erebus_001/users/admin/participant_info/participant_diagnosis_labels.csv"
    subjects=[]
    control=[]
    anxious=[]
    depressed=[]
    comorbid=[]
    partsubjects=[]
    skipsubjects=[]

    with open(labelfile, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row['banda_id'])>0 and row['banda_id']not in outliers and row['complete_flag']=='full':
                subjects.append(row['banda_id'])
                if row['diagnosis']=='control':
                    control.append(row['banda_id'])
                elif row['diagnosis']=='anx':
                    anxious.append(row['banda_id'])
                elif row['diagnosis']=='dep':
                    depressed.append(row['banda_id'])
                elif row['diagnosis']=='dep_anx':
                    comorbid.append(row['banda_id'])
            elif len(row['banda_id'])>0 and row['banda_id']not in outliers and row['complete_flag']=='partialscan':
                partsubjects.append(row['banda_id'])
            elif len(row['banda_id'])>0 and row['banda_id']not in outliers and row['complete_flag']=='didnotscan':
                skipsubjects.append(row['banda_id'])

    subjects_lbl=dict()
    subjects_lbl['allsubjects']=subjects
    subjects_lbl['control']=control
    subjects_lbl['anx']=anxious
    subjects_lbl['dep']=depressed
    subjects_lbl['dep_anx']=comorbid
    subjects_lbl['partial_scan']=partsubjects
    subjects_lbl['no_scan']=skipsubjects

    return subjects, subjects_lbl


def loadBANDA(outliers=[]):
    archivo = "/space/erebus/1/users/data/scores/BANDA_SelfReportScores_Composite_091218.csv"
    subjects=[]
    mfqs=[]
    shaps=[]
    rcadsD=[]
    rcadsA=[]
    rcadsA_gad=[]
    rcadsA_pd=[]
    rcadsA_soc=[]
    rcadsA_sad=[]
    anhedonia=[]
    gender=[]
    age=[]
    wasi=[]
    hand=[]

    with open(archivo, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row['banda_id'])>0 and len(row['MFQTOT_i'].strip())>0 and row['banda_id']not in outliers and row['shapstot_i']!='':
                subjects.append(row['banda_id'])
                #print(row['banda_id'],float(row['shapstot_i']), row['shapstot_i'], row['shapscount_i'])
                mfqs.append(float(row['MFQTOT_i']))

                shaps.append(float(row['shapstot_i']))
                rcadsD.append(float(row['RCADS_Depression_Total_raw_i']))
                rcadsA.append(float(row['RCADS_Anxiety_Total_raw_i']))
                rcadsA_gad.append(float(row['RCADS_gad_raw_i']))
                rcadsA_pd.append(float(row['RCADS_pd_raw_i']))
                rcadsA_soc.append(float(row['RCADS_soc_raw_i']))
                rcadsA_sad.append(float(row['RCADS_sad_raw_i']))
                #anhedonia.append(float(row['shapsanh_i']))
                anhedonia.append(float(row['shapscount_i']))
                gender.append(int(row['gender']))
                age.append(float(row['age']))
                wasi.append(float(row['wasi']))
                if row['handed_write']==1:
                    #left
                    hand.append(0)
                elif row['handed_write']==3:
                    #either
                    hand.append(2)
                elif row['handed_write']==2:
                    #right
                    hand.append(1)
                elif row['handed_write']=='':
                    #unknown
                    hand.append(2)

    scores= dict()
    scores['MFQ'] = np.array(mfqs)
    scores['SHAPS'] = np.array(shaps)
    scores['RCADSD'] = np.array(rcadsD)
    scores['RCADSA'] = np.array(rcadsA)
    scores['RCADSA_GAD'] = np.array(rcadsA_gad)
    scores['RCADSA_PD'] = np.array(rcadsA_pd)
    scores['RCADSA_SOC'] = np.array(rcadsA_soc)
    scores['RCADSA_SAD'] = np.array(rcadsA_sad)
    scores['Anhedonia'] = np.array(anhedonia)
    subjects_info=dict()
    subjects_info['gender']=gender
    subjects_info['age']=age
    subjects_info['wasi']=wasi
    subjects_info['hand']=hand
    return subjects, subjects_info, scores




#For BANDA001-BANDA140:

def getBandaLabels(outliers=[]):
    labelfile = "/autofs/space/erebus_001/users/admin/participant_info/participant_diagnosis_labels_140.csv"
    subjects=[]
    control=[]
    anxious=[]
    depressed=[]

    partsubjects=[]
    skipsubjects=[]

    with open(labelfile, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row['banda_id'])>0 and row['banda_id']not in outliers and row['complete_flag']=='full':
                subjects.append(row['banda_id'])
                if row['diagnosis_label']=='control':
                    control.append(row['banda_id'])
                elif row['diagnosis_label']=='anx':
                    anxious.append(row['banda_id'])
                elif row['diagnosis_label']=='dep':
                    depressed.append(row['banda_id'])
            elif len(row['banda_id'])>0 and row['banda_id']not in outliers and row['complete_flag']=='partialscan':
                partsubjects.append(row['banda_id'])
            elif len(row['banda_id'])>0 and row['banda_id']not in outliers and row['complete_flag']=='didnotscan':
                skipsubjects.append(row['banda_id'])

    subjects_lbl=dict()
    subjects_lbl['allsubjects']=subjects
    subjects_lbl['control']=control
    subjects_lbl['anx']=anxious
    subjects_lbl['dep']=depressed
    subjects_lbl['partial_scan']=partsubjects
    subjects_lbl['no_scan']=skipsubjects

    return subjects, subjects_lbl


def loadBANDA140(outliers=[]):
    archivo = "/space/erebus/1/users/data/scores/BANDA_140_composites.csv"
    subjects=[]
    mfqs=[]
    wasi=[]
    shaps=[]
    shaps_cnt=[]
    anhedonia=[]
    rcads_depression=[]
    rcads_anxiety=[]
    rcads_generalized_anx=[]
    rcads_panic=[]
    rcads_social=[]
    rcads_separation_anx=[]
    rcads_obsessive_compulsive=[]
    bis=[]
    bas=[]
    bas_drive=[]
    bas_fun=[]
    bas_reward=[]
    stai_state=[]
    stai_trait=[]
    gender=[]
    age=[]
    hand=[]
    diagnosis=[]
    diagnosis_label=[]

    with open(archivo, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row['banda_id'])>0 and len(row['wasi'].strip())>0 and row['banda_id']not in outliers and row['shaps']!='':
                subjects.append(row['banda_id'])
                #print(row['banda_id'],float(row['shapstot_i']), row['shapstot_i'], row['shapscount_i'])
                mfqs.append(float(row['mfq']))
                wasi.append(float(row['wasi']))
                shaps.append(float(row['shaps']))
                anhedonia.append(float(row['shaps_count']))
                shaps_cnt.append(float(row['shaps_count']))
                rcads_depression.append(float(row['rcads_depression']))
                rcads_anxiety.append(float(row['rcads_anxiety']))
                rcads_generalized_anx.append(float(row['rcads_generalized_anx']))
                rcads_panic.append(float(row['rcads_panic']))
                rcads_social.append(float(row['rcads_social']))
                rcads_separation_anx.append(float(row['rcads_separation_anx']))
                rcads_obsessive_compulsive.append(float(row['rcads_obsessive_compulsive']))
                bis.append(float(row['bis']))
                bas.append(float(row['bas']))
                bas_drive.append(float(row['bas_drive']))
                bas_fun.append(float(row['bas_fun']))
                bas_reward.append(float(row['bas_reward']))
                stai_state.append(float(row['stai_state']))
                stai_trait.append(float(row['stai_trait']))
                gender.append(int(row['gender']))
                age.append(float(row['age']))
                hand.append(float(row['handedness_round']))
                diagnosis.append(row['diagnosis'])
                diagnosis_label.append(row['diagnosis_label'])

    scores= dict()
    scores['MFQ'] = np.array(mfqs)
    scores['SHAPS'] = np.array(shaps)
    scores['RCADS_DEP'] = np.array(rcads_depression)
    scores['RCADS_ANX'] = np.array(rcads_anxiety)
    scores['RCADS_GenAnx'] = np.array(rcads_generalized_anx)
    scores['RCADS_Panic'] = np.array(rcads_panic)
    scores['RCADS_Social'] = np.array(rcads_social)
    scores['RCADS_SepAnx'] = np.array(rcads_separation_anx)
    scores['RCADS_OCD'] = np.array(rcads_obsessive_compulsive)
    scores['Anhedonia'] = np.array(anhedonia)

    subjects_info=dict()
    subjects_info['gender']=gender
    subjects_info['age']=age
    subjects_info['wasi']=wasi
    subjects_info['hand']=hand
    subjects_info['diagnosis']=diagnosis
    subjects_info['diagnosis_label']=diagnosis_label

    return subjects, subjects_info, scores






def createParams(amp=1,shift=0.5,decay=0.03, sex=0.5):
    params = Parameters()
    params.add('amp',   value=amp) # -1, max=0)
    params.add('shift', value=shift) #, min=0, max=1)
    params.add('decay', value=decay) #, max=1)
    params.add('sex', value=sex) #, min=0, max=1)
    return params

def fitting(params, x, y_sex, fit,data=[]):
    amp = params['amp']
    decay = params['decay']
    shift = params['shift']
    sex_param = params['sex']

    if len(y_sex)>0:
        if fit == 'poisson' or fit == 'Poisson':
            model = amp * np.array(x) * np.exp( -decay *np.array(x)) + shift + sex_param*np.array(y_sex)
        elif fit=='exponential':
            model = decay *pow(2,amp*np.array(x)) +shift +  sex_param*np.array(y_sex)
        elif fit=='quadratic':
            model = amp * np.array(x) + decay *pow(np.array(x),2)  + shift + sex_param*np.array(y_sex)
        else:
            model = amp * np.array(x) + shift + sex_param*np.array(y_sex)
    else:
        if fit == 'poisson' or fit == 'Poisson':
            model = amp * np.array(x) * np.exp( -decay *np.array(x)) + shift
        elif fit=='exponential':
            model = decay *pow(2,amp*np.array(x))  +shift
        elif fit=='quadratic':
            model = amp * np.array(x) + decay *pow(np.array(x),2)  + shift
        else:
            model = amp * np.array(x) + shift


    if data==[]:
        return model
    return model - data

def getValues(inFile, xColumn,lineIndex, acq_time,ref):
    prevValues =[]
    volumes=1
    tra = [0,0,0]
    absol = [0,0,0]
    linei=0
    iind=0
    with open(inFile) as motionFile:
        for line in motionFile:
            if linei >= lineIndex[0] and linei <lineIndex[len(lineIndex)-1] :
                values =  line.split()
                if len(prevValues )>5:
                    t=0
                    for i in range(xColumn, xColumn+3):
                        if linei == lineIndex[iind]:
                            tra[i-xColumn] += math.fabs(float(values[i])-float(prevValues[i]))

                    volumes +=1
                if linei==ref or ref<0:
                    prevValues = values
                if linei==lineIndex[0]:
                    for i in range(xColumn, xColumn+3):
                        absol[i-xColumn]= float(values[i])
                iind+=1
            if len(lineIndex) == iind:
                break
            linei+=1
    return (tra, volumes*acq_time, absol)

def getTranslation(inFile, xColumn,lineIndex,acq_time,ref=-1, inFile2=None, lineIndex2=None):

    tra = getValues( inFile,xColumn,lineIndex,acq_time,ref)
    tra2=[0,0,0]
    if not inFile2 ==None :
        tra2 = getValues( inFile2,xColumn,lineIndex2,acq_time,ref)
        res = np.array(tra[2]) - np.array(tra2[2])
    else:
        res= np.array(tra[0])/tra[1]



    return math.sqrt(sum(res**2)) #/tra[1]

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

def getTranslationAbsolute(inFile, xColumn,lineIndex,acq_time,ref=0):
    return getTranslation( inFile,xColumn,lineIndex,acq_time,ref)


def getRotationAbsolute(inFile, xColumn,lineIndex,acq_time,ref=0):
    return getRotation(inFile,xColumn,lineIndex,acq_time,ref)

def getFileData(fileN):
    if "dMRI" in fileN:
        column =0
        acq_time=3.230
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


def GetCompositeScores():
    testsDict={'mfq':33,'shaps':14,'rcads':47,'stai_state':20,'stai_trait':20,'bisbas':24}
    testsList=['mfq','shaps','rcads','stai_state','stai_trait','bisbas']
    #testsBISBAS=['bas_drive','bas_fun','bas_reward','bis']

    stai_state_rvscore=[1,2,5,8,10,11,15,16,19,20]
    stai_trait_rvscore=[1,6,7,10,13,16,19]

    shaps_rvscore=[1,3,6,8,10,11,13]

    bisbas_truescore=[2,22]
    bas_drive_nbs=[3,9,12,21]
    bas_fun_nbs=[5,10,15,20]
    bas_reward_nbs=[4,7,13,18,23]
    bis_nbs=[2,8,13,16,19,22,24]

    rcads_soc_nbs=[4,7,8,12,20,30,32,38,43]
    rcads_pd_nbs=[3,14,24,26,28,34,39,41]
    rcads_mdd_nbs=[2,6,11,15,19,21,25,29,40,47]
    rcads_sad_nbs=[5,9,17,18,45,46]
    rcads_gad_nbs=[1,13,22,27,35,37]
    rcads_ocd_nbs=[10,16,23,31,42,44]

    BANDA_ID=[]
    STAI_TRAIT_TOTs=[]
    STAI_STATE_TOTs=[]
    BAS_DRIVE_TOTs=[]
    BAS_FUN_TOTs=[]
    BAS_REWARD_TOTs=[]
    BIS_TOTs=[]

    rawscores = "/autofs/space/erebus_001/users/data/scores/banda_rawscores_091118.csv"

    output=csv.writer(open('/autofs/space/erebus_001/users/data/scores/BANDA_SelfReportScores_Composite_091218.csv','w+'))

    output.writerow(['banda_id','subject_id','gender','age','wasi','hand','SHAPS_TOT_i','SHAPS_COUNT_i',\
    'SHAPS_ANH_i','MFQ_TOT_i','RCADS_sad_raw_i','RCADS_gad_raw_i','RCADS_pd_raw_i','RCADS_soc_raw_i',\
    'RCADS_ocd_raw_i','RCADS_mdd_raw_i','RCADS_Depression_Total_raw_i','RCADS_Anxiety_Total_raw_i',\
    'RCADS_Total_Score_raw_i','STAI_STATE_TOT_i','STAI_TRAIT_TOT_i','BAS_DRIVE_TOT_i','BAS_FUN_TOT_i',\
    'BAS_REWARD_TOT_i','BIS_TOT_i'])


    with open(rawscores, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            #BANDA_ID.append(row['banda_id'])
            out_id=row['banda_id']
            out_subjid=row['subject_id']
            out_diagnosis=row['group']
            out_age=row['age']
            out_hand=row['handed_tot']
            if row['gender'] == 'F':
                out_gender=0
            elif row['gender'] == 'M':
                out_gender=1
            out_wasi=row['wasi']
            #out_shaps_tot=row['shapstot_i']
            #out_shaps_cnt=row['shapscount_i']
            #out_shaps_anh=row['shaps_anh_i']

            for test in testsList:
                curr_tot=0
                nbScores=testsDict[test]
                if test == 'stai_trait':
                    for i in range(1,nbScores+1,1):
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in stai_trait_rvscore:
                                curr_score=4-float(row[name])+1
                                curr_tot=curr_tot+curr_score
                            else:
                                curr_score=float(row[name])
                                curr_tot=curr_tot+curr_score
                    #STAI_TRAIT_TOTs.append(curr_tot)
                    out_stai_trait=curr_tot
                elif test == 'stai_state':
                    for i in range(1,nbScores+1,1):
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in stai_state_rvscore:
                                curr_score=4-float(row[name])+1
                                curr_tot=curr_tot+curr_score
                            else:
                                curr_score=float(row[name])
                                curr_tot=curr_tot+curr_score
                    #STAI_STATE_TOTs.append(curr_tot)
                    out_stai_state=curr_tot
                elif test == 'mfq':
                    for i in range(1,nbScores+1,1):
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            curr_tot=curr_tot+curr_score
                    out_mfq=curr_tot
                elif test == 'shaps':
                    curr_count=0
                    for i in range(1,nbScores+1,1):
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in shaps_rvscore:
                                curr_score=float(row[name])+1
                                curr_score=4-curr_score+1
                                curr_tot=curr_tot+curr_score
                            else:
                                curr_score=float(row[name])+1
                                curr_tot=curr_tot+curr_score
                            if curr_score == 3 or curr_score == 4:
                                curr_count = curr_count + 1
                    if curr_count >= 3:
                        out_shaps_anh = 1
                    else:
                        out_shaps_anh = 0
                    out_shaps_tot=curr_tot
                    out_shaps_cnt=curr_count
                elif test == 'rcads':
                    soc_tot=0
                    for i in rcads_soc_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            soc_tot=soc_tot+curr_score
                        out_rcads_soc=soc_tot
                    pd_tot=0
                    for i in rcads_pd_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            pd_tot=pd_tot+curr_score
                        out_rcads_pd=pd_tot
                    mdd_tot=0
                    for i in rcads_mdd_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            mdd_tot=mdd_tot+curr_score
                        out_rcads_mdd=mdd_tot
                    sad_tot=0
                    for i in rcads_sad_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            sad_tot=sad_tot+curr_score
                        out_rcads_sad=sad_tot
                    gad_tot=0
                    for i in rcads_gad_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            gad_tot=gad_tot+curr_score
                        out_rcads_gad=gad_tot
                    ocd_tot=0
                    for i in rcads_ocd_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            curr_score=float(row[name])
                            ocd_tot=ocd_tot+curr_score
                        out_rcads_ocd=ocd_tot
                    out_rcads_dep_tot=out_rcads_mdd
                    out_rcads_anx_tot=out_rcads_gad+out_rcads_sad+out_rcads_pd+out_rcads_soc+out_rcads_ocd
                    out_rcads_total=out_rcads_dep_tot+out_rcads_anx_tot
                elif test == 'bisbas':
                    drive_tot=0
                    for i in bas_drive_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in bisbas_truescore:
                                curr_score=float(row[name])
                                drive_tot=drive_tot+curr_score
                            else:
                                curr_score=4-float(row[name])+1
                                drive_tot=drive_tot+curr_score
                        #BAS_DRIVE_TOTs.append(curr_tot)
                        out_bas_drive=drive_tot
                    fun_tot=0
                    for i in bas_fun_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in bisbas_truescore:
                                curr_score=float(row[name])
                                fun_tot=fun_tot+curr_score
                            else:
                                curr_score=4-float(row[name])+1
                                fun_tot=fun_tot+curr_score
                        #BAS_FUN_TOTs.append(curr_tot)
                        out_bas_fun=fun_tot
                    reward_tot=0
                    for i in bas_reward_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in bisbas_truescore:
                                curr_score=float(row[name])
                                reward_tot=reward_tot+curr_score
                            else:
                                curr_score=4-float(row[name])+1
                                reward_tot=reward_tot+curr_score
                        #BAS_REWARD_TOTs.append(curr_tot)
                        out_bas_reward=reward_tot
                    bis_tot=0
                    for i in bis_nbs:
                        name="%s%d_i" % (test,i)
                        if row[name] != 'NA':
                            if i in bisbas_truescore:
                                curr_score=float(row[name])
                                bis_tot=bis_tot+curr_score
                            else:
                                curr_score=4-float(row[name])+1
                                bis_tot=bis_tot+curr_score
                        #BIS_TOTs.append(curr_tot)
                        out_bis=bis_tot
            output.writerow([out_id,out_subjid,out_gender,out_age,out_wasi,out_hand,out_shaps_tot,out_shaps_cnt,out_shaps_anh,out_mfq,out_rcads_sad,out_rcads_gad,out_rcads_pd,out_rcads_soc,out_rcads_ocd,out_rcads_mdd,out_rcads_dep_tot,out_rcads_anx_tot,out_rcads_total,out_stai_state,out_stai_trait,out_bas_drive,out_bas_fun,out_bas_reward,out_bis])
            #output.writerow([out_id,out_subjid,out_gender,out_age,out_wasi,out_hand,out_shaps_tot,out_shaps_cnt,out_shaps_anh,out_mfq,out_stai_state,out_stai_trait,out_bas_drive,out_bas_fun,out_bas_reward,out_bis])




# def loadBANDAscores(outliers=[]):
#     archivo = "/space/erebus/1/users/data/scores/BANDA_SelfReportScores_Composite_091218.csv"
#     subjects=[]
#     mfqs=[]
#     shaps=[]
#     rcadsD=[]
#     rcadsA=[]
#     rcadsA_gad=[]
#     rcadsA_pd=[]
#     rcadsA_soc=[]
#     rcadsA_sad=[]
#     anhedonia=[]
#     staiS=[]
#     staiT=[]
#     bis=[]
#     bas=[]
#     basD=[]
#     basF=[]
#     basR=[]
#     gender=[]
#     age=[]
#     wasi=[]
#     hand=[]

#     with open(archivo, 'r') as csvfile:
#         reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
#         for row in reader:
#             if len(row['banda_id'])>0 and len(row['MFQ_TOT_i'].strip())>0 and row['banda_id']not in outliers and row['SHAPS_TOT_i']!='':
#                 subjects.append(row['banda_id'])
#                 #print(row['banda_id'],float(row['shapstot_i']), row['shapstot_i'], row['shapscount_i'])
#                 mfqs.append(float(row['MFQ_TOT_i']))
#                 shaps.append(float(row['SHAPS_TOT_i']))
#                 rcadsD.append(float(row['RCADS_Depression_Total_raw_i']))
#                 rcadsA.append(float(row['RCADS_Anxiety_Total_raw_i']))
#                 rcadsA_gad.append(float(row['RCADS_gad_raw_i']))
#                 rcadsA_pd.append(float(row['RCADS_pd_raw_i']))
#                 rcadsA_soc.append(float(row['RCADS_soc_raw_i']))
#                 rcadsA_sad.append(float(row['RCADS_sad_raw_i']))
#                 #anhedonia.append(float(row['shapsanh_i']))
#                 anhedonia.append(float(row['SHAPS_COUNT_i']))
#                 staiS.append(float(row['STAI_STATE_TOT_i']))
#                 staiT.append(float(row['STAI_TRAIT_TOT_i']))
#                 bis.append(float(row['BIS_TOT_i']))
#                 bas.append(float(row['BAS_TOT_i']))
#                 basD.append(float(row['BAS_DRIVE_TOT_i']))
#                 basF.append(float(row['BAS_FUN_TOT_i']))
#                 basR.append(float(row['BAS_REWARD_TOT_i']))
#                 gender.append(int(row['gender']))
#                 age.append(float(row['age']))
#                 wasi.append(float(row['wasi']))
#                 hand.append(float(row['hand']))

#     scores= dict()
#     scores['MFQ'] = np.array(mfqs)
#     scores['SHAPS'] = np.array(shaps)
#     scores['RCADSD'] = np.array(rcadsD)
#     scores['RCADSA'] = np.array(rcadsA)
#     scores['RCADSA_GAD'] = np.array(rcadsA_gad)
#     scores['RCADSA_PD'] = np.array(rcadsA_pd)
#     scores['RCADSA_SOC'] = np.array(rcadsA_soc)
#     scores['RCADSA_SAD'] = np.array(rcadsA_sad)
#     scores['Anhedonia'] = np.array(anhedonia)
#     scores['STAIS'] = np.array(staiS)
#     scores['STAIT'] = np.array(staiT)
#     scores['BIS'] = np.array(bis)
#     scores['BAS'] = np.array(bas)
#     scores['BASD'] = np.array(basD)
#     scores['BASF'] = np.array(basF)
#     scores['BASR'] = np.array(basR)
#     subjects_info=dict()
#     subjects_info['gender']=gender
#     subjects_info['age']=age
#     subjects_info['wasi']=wasi
#     subjects_info['hand']=hand
#     return subjects, subjects_info, scores





def loadBANDAscores(outliers=[]):

	archivo = "/space/erebus/1/users/data/scores/BANDA_140_composites.csv"
	subjects=[]
	diagnoses=[]
	gender=[]
	age=[]
	hand=[]
	wasi=[]
	mfqs=[]
	shaps_total=[]
	shaps_cnt=[]
	rcadsDep=[]
	rcadsAnx=[]
	rcadsAnx_gad=[]
	rcadsAnx_pd=[]
	rcadsAnx_soc=[]
	rcadsAnx_sad=[]
	rcadsAnx_ocd=[]
	#anhedonia=[]
	staiState=[]
	staiTrait=[]
	bis=[]
	bas=[]
	basDrive=[]
	basFun=[]
	basReward=[]


	with open(archivo, 'r') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for row in reader:
			if len(row['banda_id'])>0 and row['banda_id']not in outliers:
				try:
					subjects.append(row['banda_id'])
					#print(row['banda_id'],float(row['shapstot_i']), row['shapstot_i'], row['shapscount_i'])
					diagnoses.append(row['diagnosis'])
					gender.append(int(row['gender']))
					age.append(float(row['age']))
					wasi.append(float(row['wasi']))
					hand.append(float(row['handedness_round']))
					mfqs.append(float(row['mfq']))
					shaps_total.append(float(row['shaps']))
					shaps_cnt.append(float(row['shaps_count']))
					rcadsDep.append(float(row['rcads_depression']))
					rcadsAnx.append(float(row['rcads_anxiety']))
					rcadsAnx_gad.append(float(row['rcads_generalized_anx']))
					rcadsAnx_pd.append(float(row['rcads_panic']))
					rcadsAnx_soc.append(float(row['rcads_social']))
					rcadsAnx_sad.append(float(row['rcads_separation_anx']))
					rcadsAnx_ocd.append(float(row['rcads_obsessive_compulsive']))
					#anhedonia.append(float(row['shapsanh_i']))
					#anhedonia.append(float(row['SHAPS_COUNT_i']))
					staiState.append(float(row['stai_state']))
					staiTrait.append(float(row['stai_trait']))
					bis.append(float(row['bis']))
					bas.append(float(row['bas']))
					basDrive.append(float(row['bas_drive']))
					basFun.append(float(row['bas_fun']))
					basReward.append(float(row['bas_reward']))
				except:
					print(row['banda_id'])
	scores= dict()
	scores['MFQ'] = np.array(mfqs)
	scores['SHAPS_TOT'] = np.array(shaps_total)
	scores['SHAPS_CNT'] = np.array(shaps_cnt)
	scores['RCADSD'] = np.array(rcadsDep)
	scores['RCADSA'] = np.array(rcadsAnx)
	scores['RCADSA_GAD'] = np.array(rcadsAnx_gad)
	scores['RCADSA_PD'] = np.array(rcadsAnx_pd)
	scores['RCADSA_SOC'] = np.array(rcadsAnx_soc)
	scores['RCADSA_SAD'] = np.array(rcadsAnx_sad)
	scores['RCADSA_OCD'] = np.array(rcadsAnx_ocd)
	#scores['Anhedonia'] = np.array(anhedonia)
	scores['STAIS'] = np.array(staiState)
	scores['STAIT'] = np.array(staiTrait)
	scores['BIS'] = np.array(bis)
	scores['BAS'] = np.array(bas)
	scores['BASD'] = np.array(basDrive)
	scores['BASF'] = np.array(basFun)
	scores['BASR'] = np.array(basReward)
	subjects_info=dict()
	subjects_info['gender']=gender
	subjects_info['age']=age
	subjects_info['wasi']=wasi
	subjects_info['hand']=hand
	subjects_info['diagnosis']=diagnoses
	return subjects, subjects_info, scores




#loadBANDAscores()
