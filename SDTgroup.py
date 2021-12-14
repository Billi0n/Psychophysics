import pandas as pd
from scipy.stats import norm
from statistics import mean
from os import listdir
from statsmodels.stats.anova import AnovaRM
import matplotlib.pyplot as plt

#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)
    return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))
    return stat

dataPath = "data_group/"
fileList = listdir(dataPath)

meanSDTs = pd.DataFrame({"participant" : [], "dPrime" : [], "criterion" : []})
counter = 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)

    expData = pd.DataFrame(rawData, columns = ["task","condition","key_resp_2.keys", "key_resp_2.rt"])
    expData = expData.rename(columns = {"task":"shape", "condition":"stimulus_type","key_resp_2.rt" : "RT", "key_resp_2.keys" : "resp"})

    expData2 = pd.DataFrame(rawData, columns = ["task","condition", "key_resp_3.keys", "key_resp_3.rt"])
    expData2 = expData2.rename(columns = {"task":"shape", "condition":"stimulus_type","key_resp_3.rt" : "RT", "key_resp_3.keys" : "resp"})

    accuracy = pd.DataFrame({"stimulus_type" : ["salient", "nonsalient"], "hits" : [0,0], "misses" : [0,0], "CRs" : [0,0], "FAs" : [0,0]})
    accuracy2 = pd.DataFrame({"stimulus_type" : ["salient", "nonsalient"], "hits" : [0,0], "misses" : [0,0], "CRs" : [0,0], "FAs" : [0,0]})

    for index, row in expData.iterrows():
        if row["stimulus_type"] == "nonsalient":
            rowInd = 1
            #Hit: go trial where participant responds. In this experiment, response is done with space key
            if row["shape"] == "go" and row["resp"] == "space":
                #loc is index with string, but only works for database
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["shape"] == "go" and row["resp"] == "None":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["shape"] == "nogo" and row["resp"] == "None":
                accuracy.loc[rowInd,"CRs"] += 1 #False alarm
            elif row["shape"] == "nogo" and row["resp"] == "space":
                accuracy.loc[rowInd,"FAs"] += 1

        elif row["stimulus_type"] == "salient":
            rowInd = 0
            #Hit
            if row["shape"] == "go" and row["resp"] == "space":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["shape"] == "go" and row["resp"] == "None": accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["shape"] == "nogo" and row["resp"] == "None":
                accuracy.loc[rowInd,"CRs"] += 1
            #False alarm
            elif row["shape"] == "nogo" and row["resp"] == "space":
                accuracy.loc[rowInd,"FAs"] += 1

    hitRatenonsalient = accuracy.loc[1]["hits"]/5
    FAratenonsalient = accuracy.loc[1]["FAs"]/5
    hitRatesalient = accuracy.loc[0]["hits"]/5
    FAratesalient = (accuracy.loc[0]["FAs"])/5

    missRatenonsalient = accuracy.loc[1]["misses"]/5
    rejectionRatenonsalient = accuracy.loc[1]["CRs"]/5
    missRatesalient = accuracy.loc[0]["misses"]/5
    rejectionRatesalient = (accuracy.loc[0]["CRs"])/5

    for index, row in expData2.iterrows():
        if row["stimulus_type"] == "nonsalient":
            #index for nonsalient condition is 0 in the table of accuracy
            rowInd = 1
            #Hit: go trial where participant responds. In this experiment, response is done with space key
            if row["shape"] == "go" and row["resp"] == "space":
                #loc is index with string, but only works for database
                accuracy2.loc[rowInd,"hits"] += 1
            #Miss
            elif row["shape"] == "go" and row["resp"] == "None":
                accuracy2.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["shape"] == "nogo" and row["resp"] == "None":
                accuracy2.loc[rowInd,"CRs"] += 1 #False alarm
            elif row["shape"] == "nogo" and row["resp"] == "space":
                accuracy2.loc[rowInd,"FAs"] += 1

        elif row["stimulus_type"] == "salient":
            rowInd = 0
            #Hit
            if row["shape"] == "go" and row["resp"] == "space":
                accuracy2.loc[rowInd,"hits"] += 1
            #Miss
            elif row["shape"] == "go" and row["resp"] == "None":
                accuracy2.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["shape"] == "nogo" and row["resp"] == "None":
                accuracy2.loc[rowInd,"CRs"] += 1
            #False alarm
            elif row["shape"] == "nogo" and row["resp"] == "space":
                accuracy2.loc[rowInd,"FAs"] += 1

    hitRatenonsalient2 = accuracy2.loc[1]["hits"]/5
    FAratenonsalient2 = accuracy2.loc[1]["FAs"]/5
    hitRatesalient2 = accuracy2.loc[0]["hits"]/5
    FAratesalient2 = (accuracy2.loc[0]["FAs"])/5

    missRatenonsalient2 = accuracy2.loc[1]["misses"]/5
    rejectionRatenonsalient2 = accuracy2.loc[1]["CRs"]/5
    missRatesalient2 = accuracy2.loc[0]["misses"]/5
    rejectionRatesalient2 = (accuracy2.loc[0]["CRs"])/5

    dnonsalient = dPrime(hitRatenonsalient,FAratenonsalient)
    criterionnonsalient = criterion(hitRatenonsalient,FAratenonsalient)
    dsalient= dPrime(hitRatesalient,FAratesalient)
    criterionsalient= criterion(hitRatesalient,FAratesalient)

    dnonsalient2 = dPrime(hitRatenonsalient2,FAratenonsalient2)
    criterionnonsalient2 = criterion(hitRatenonsalient2,FAratenonsalient2)
    dsalient2= dPrime(hitRatesalient2,FAratesalient2)
    criterionsalient2= criterion(hitRatesalient2,FAratesalient2)

    pNumList = [pNum, pNum,pNum,pNum]
    stimuliList = ["salient", "nonsalient", "salient","nonsalient"]
    shapeList = ["rectangle", "rectangle","circle","circle"]

    hitList=[]
    hitList.append(hitRatesalient)
    hitList.append(hitRatenonsalient)
    hitList.append(hitRatesalient2)
    hitList.append(hitRatenonsalient2)

    FAList=[]
    FAList.append(FAratesalient)
    FAList.append(FAratenonsalient)
    FAList.append(FAratesalient2)
    FAList.append(FAratenonsalient2)

    missList=[]
    missList.append(missRatesalient)
    missList.append(missRatenonsalient)
    missList.append(missRatesalient2)
    missList.append(missRatenonsalient2)

    rejectionList=[]
    rejectionList.append(rejectionRatesalient)
    rejectionList.append(rejectionRatenonsalient)
    rejectionList.append(rejectionRatesalient2)
    rejectionList.append(rejectionRatenonsalient2)

    dList =[]
    dList.append(dsalient)
    dList.append(dnonsalient)
    dList.append(dsalient2)
    dList.append(dnonsalient2)

    cList=[]
    cList.append(criterionsalient)
    cList.append(criterionnonsalient)
    cList.append(criterionsalient2)
    cList.append(criterionnonsalient2)

    #print(accuracy)
    #print(accuracy2)

    newLines = pd.DataFrame({"participant" : pNumList, "stimulus_type" : stimuliList, "shape" : shapeList,
                            "hits": hitList, "correct rejections": rejectionList, "false alarms": FAList, "misses": missList, "dPrime" :dList , "criterion": cList})

    meanSDTs = meanSDTs.append(newLines, ignore_index=True) #don't want index duplicates


print(meanSDTs)
print(dList)
print(cList)
print("d' (nonsalient block 1):", dnonsalient)
print("criterion (nonsalient block 1):", criterionnonsalient)
print("d' (salient block 1):", dsalient)
print("criterion (salient block 1):", criterionsalient)
print("d' (nonsalient block 2):", dnonsalient2)
print("criterion (nonsalient block 2):", criterionnonsalient2)
print("d' (salient block 2):", dsalient2)
print("criterion (salient block 2):", criterionsalient2)

#repeated measures anova
model = AnovaRM(data = meanSDTs, depvar = "dPrime", subject = "participant", within = ["stimulus_type", "shape"]).fit()
print(model)

model = AnovaRM(data = meanSDTs, depvar = "criterion", subject = "participant", within = ["stimulus_type", "shape"]).fit()
print(model)
