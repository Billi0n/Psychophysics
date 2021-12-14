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

    expData = pd.DataFrame(rawData, columns = ["type","shape","key_resp_5.keys", "key_resp_5.rt"])
    expData = expData.rename(columns = {"key_resp_5.rt" : "RT", "key_resp_5.keys" : "response"})


    #only include trials with a response
    expData = expData[expData.RT.notnull()]
    #only include trials with correct test responses for RT analysis
    rtDatast = expData[(expData.type == "st") & (expData.response == "right")]
    rtDatanon = expData[(expData.type == "nonst") & (expData.response == "left")]

    #removeoutliers
    rtDatast = removeoutliers(rtDatast,"RT")
    rtDatanon = removeoutliers(rtDatanon,"RT")

    print(rtDatast.to_string())
    print(rtDatanon.to_string())

    #data frame for RTs for each condition
    stimuliRTs = rtDatast[(rtDatast.type == "st")].RT
    nonstimuliRTs = rtDatanon[(rtDatanon.type == "nonst")].RT


    pNumList = [pNum, pNum]
    stimuliList = ["stimuli","nonstimuli"]

    meanRTsList = [mean(stimuliRTs), mean(nonstimuliRTs)]

    #new data --> data frame
    newLines = pd.DataFrame({"participant" : pNumList, "type" : stimuliList,
                            "mean RT" : meanRTsList})

    #append newLines to meanRTs
    #(note: unlike appending a list, this doesn't change the initial data frame)
    meanRTs = meanRTs.append(newLines, ignore_index=True) #don't want index duplicates

print(meanRTs)

print("Stimuli mean RT",mean(stimuliRTs))
print("Non-stimuli mean RT",mean(nonstimuliRTs))

#vizualizing with a boxplot
fig, ax = plt.subplots()

box = ax.boxplot([stimuliRTs, nonstimuliRTs])

ax.set_ylabel("RT (s)")
ax.set_xticklabels(["Stimuli", "Non-stimuli"])

plt.show()

#repeated measures anova
model = AnovaRM(data = meanRTs, depvar = "mean RT", subject = "participant", within = ["type"]).fit()
print(model)
