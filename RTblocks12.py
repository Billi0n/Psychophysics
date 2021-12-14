import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
from os import listdir
from statsmodels.stats.anova import AnovaRM


def removeoutliers(df_in, col_name):
       q1 = df_in[col_name].quantile(0.25)
       q3 = df_in[col_name].quantile(0.75)
       iqr = q3 - q1 #Interquartile range
       fence_low = q1 - 1.5 * iqr
       fence_high = q3 + 1.5 * iqr
       df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
       return df_out


dataPath = "data_group/"
fileList = listdir(dataPath)

meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})
counter = 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)

    expData1 = pd.DataFrame(rawData, columns = ["task","condition","key_resp_2.keys", "key_resp_2.rt"])
    expData1 = expData1.rename(columns = {"key_resp_2.rt" : "RT", "key_resp_2.keys" : "response"})
    expData2 = pd.DataFrame(rawData, columns = ["task","condition", "key_resp_3.keys", "key_resp_3.rt"])
    expData2 = expData2.rename(columns = {"key_resp_3.rt" : "RT", "key_resp_3.keys" : "response"})

    #only include trials with a response
    expData1 = expData1[expData1.RT.notnull()]
    expData2 = expData2[expData2.RT.notnull()]
    #only include trials with correct test responses for RT analysis
    rtData1 = expData1[(expData1.task == "go") & (expData1.response == "space")]
    rtData2 = expData2[(expData2.task == "go") & (expData2.response == "space")]

    #removeoutliers
    rtData1 = removeoutliers(rtData1,"RT")
    rtData2 = removeoutliers(rtData2,"RT")

    print(rtData1.to_string())
    print(rtData2.to_string())

    #data frame for RTs for each condition
    salientGoRTs1 = rtData1[(rtData1.condition == "salient")].RT
    nonsalientGoRTs1 = rtData1[(rtData1.condition == "nonsalient")].RT
    salientGoRTs2 = rtData2[(rtData2.condition == "salient")].RT
    nonsalientGoRTs2 = rtData2[(rtData2.condition == "nonsalient")].RT

    pNumList = [pNum, pNum,pNum,pNum]
    stimuliList = ["salient", "nonsalient","salient","nonsalient"]
    shapeList = ["rectangle", "rectangle","circle","circle"]

    meanRTsList = [mean(salientGoRTs1), mean(nonsalientGoRTs1),mean(salientGoRTs2),mean(nonsalientGoRTs2)]

    #new data --> data frame
    newLines = pd.DataFrame({"participant" : pNumList, "stimulus_type" : stimuliList,
                            "shape" : shapeList, "mean RT" : meanRTsList})

    #append newLines to meanRTs
    #(note: unlike appending a list, this doesn't change the initial data frame)
    meanRTs = meanRTs.append(newLines, ignore_index=True) #don't want index duplicates

print(meanRTs)

print("Salient rectangle mean RT",mean(salientGoRTs1))
print("Non-salient rectangle mean",mean(nonsalientGoRTs1))
print("Salient circle mean RT",mean(salientGoRTs2))
print("Non-salient circle mean",mean(nonsalientGoRTs2))

#vizualizing with a boxplot
fig, ax = plt.subplots()

box = ax.boxplot([salientGoRTs1, nonsalientGoRTs1, salientGoRTs2, nonsalientGoRTs2])

ax.set_ylabel("RT (s)")
ax.set_xticklabels(["Salient:Rectangle", "Non-salient:Rectangle", "Salient:Circle","Non-salient:Circle"])

plt.show()

#repeated measures anova
model = AnovaRM(data = meanRTs, depvar = "mean RT", subject = "participant", within = ["stimulus_type", "shape"]).fit()
print(model)
