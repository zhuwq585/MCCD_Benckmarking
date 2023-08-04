import ujson,os,sys
sys.path.append(sys.path[0][:-6])
from cloneMatcher import * 

CONFIG_FILE  = "./.config.json"


def similarityClassifier():    
    res = {}
    index = 0.00
    while index < 1.01:
        res[round(index,2)] = [0,0]
        index = index + 0.01
    return res

def evaluateSubset(toolResultFile, benchmarkFile):
    # if not os.path.exists(toolResultFile):
    #     return ""
    
    cloneMatcher = CloneMatcher(benchmarkFile, 0.7)
    cloneMatcher.importClone(toolResultFile)
    matchedClone = cloneMatcher.cloneMatch()
    unmatchedClone = cloneMatcher.getUnmatchedClone()
    
    sClassfier = similarityClassifier()
    for clone in matchedClone:
        simiTmp = round(float(cloneMatcher.cloneDict.clonePair[clone[0]][clone[3]][0]),2)
        sClassfier[simiTmp][0] += 1
        sClassfier[simiTmp][1] += 1
    
    for clone in unmatchedClone:
        simiTmp = round(float(cloneMatcher.cloneDict.clonePair[clone[0]][clone[1]][0]),2)
        sClassfier[simiTmp][1] += 1
    
    line1 = "simi,"
    line2 = "recall,"
    line3 = "detected_clone,"
    line4 = "all_clone,"
    for simi in sClassfier:
        line1 = line1 + str(simi) + ","
        try:
            line2 = line2 + str(sClassfier[simi][0] / sClassfier[simi][1]) + ","
        except ZeroDivisionError:
            line2 = line2 + "-1,"
        line3 = line3 + str(sClassfier[simi][0]) + ","
        line4 = line4 + str(sClassfier[simi][1]) + ","
        
    return line1 + "\n" + line2 + "\n" + line3 + "\n" + line4
    
def evaluateAll(tool, language, problemIdList):
    resultFile = open('./benchmarkResult/' + tool + "/" + language + '/all.csv','w')

    detected_list = None
    all_list      = None

    for problemId in problemIdList:
        resFile = './benchmarkResult/' + tool + "/" + language + '/' + problemId + '.csv'
        if os.path.exists(resFile):
            dataLines = open(resFile,'r').readlines()
            for index in range(len(dataLines)):
                dataLines[index] = dataLines[index] if dataLines[index][-1] != "\n" else dataLines[index][:-1]
                if dataLines[index][-1] == ",":
                    dataLines[index] = dataLines[index][:-1]
            
            if detected_list == None and all_list == None:
                detected_list = dataLines[2].split(',')[1:]
                all_list      = dataLines[3].split(',')[1:]
                for i in range(101):
                    detected_list[i] = int(detected_list[i])
                    all_list[i] = int(all_list[i])
            else:
                detected_tmp = dataLines[2].split(',')[1:]
                all_tmp = dataLines[3].split(',')[1:]
                for i in range(101):
                    detected_list[i] += int(detected_tmp[i])
                    all_list[i] += int(all_tmp[i])
        else:
            print(resFile + "not found")
            continue

    resultFile.write('simi,0.0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.0\n')

    recallList = []
    if detected_list == None:
        resultFile.write('Recall,')
        resultFile.write('\n')
        
        resultFile.write('Detected_clone,')
        resultFile.write('\n')
        
        resultFile.write('All_clone,')
        resultFile.write('\n')
        resultFile.close()
    else:
        for i in range(101):
            try:
                recall = int(detected_list[i]) / int(all_list[i])
                recallList.append( recall )
            except ZeroDivisionError:
                recallList.append(0)
        
        resultFile.write('Recall,')
        for recall in recallList:
            resultFile.write(str(recall) + ',')
        resultFile.write('\n')
        
        resultFile.write('Detected_clone,')
        for num in detected_list:
            resultFile.write(str(num) + ',')
        resultFile.write('\n')
        
        resultFile.write('All_clone,')
        for num in all_list:
            resultFile.write(str(num) + ',')
        resultFile.write('\n')
        resultFile.close()
        
                

if __name__ == "__main__":
    targetTools = []
    CONFIG_OBJ = ujson.loads(open(CONFIG_FILE,"r").read())
    
    ProblemIdList = CONFIG_OBJ['problemId']
    LanguageList = CONFIG_OBJ['language']
    
    if not os.path.exists("./benchmarkResult/"):
        os.mkdir("./benchmarkResult/")
    
    if len(sys.argv) <= 1:
        print("Evaluating all imported tools.")
        targetTools = list(CONFIG_OBJ['tools'].keys())
    else:
        if sys.argv[1] in CONFIG_OBJ['tools']:
            targetTools.append(sys.argv[1])    
        else:
            print(sys.argv[1] + " not added.")
    
    for targetTool in targetTools:
        for language in LanguageList:
            # result per pId
            for problemId in  ProblemIdList:
                print(targetTool + "-" + language + "-" + problemId)
                toolResultFile = "./ToolResult/" + targetTool + "/" + language + "/" + language + "_" + problemId + ".csv"
                benchmarkFile = "./benchmark-data/" + language + "/" + problemId + ".benchmark"
                
                reportText = evaluateSubset(toolResultFile, benchmarkFile)
                if len(reportText) < 1:
                    continue
                
                resultFile = "./benchmarkResult/" + targetTool + "/" + language + "/" + problemId + ".csv"
                open(resultFile,"w").write(reportText)
                
            # result pre language
            evaluateAll(targetTool, language, ProblemIdList)
            
            