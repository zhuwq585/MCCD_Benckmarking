import ujson
CONFIG_FILE  = "./.config.json"

if __name__ == "__main__":
    
    CONFIG_OBJ = ujson.loads(open(CONFIG_FILE,"r").read())
    PROBLEM_ID_LIST = CONFIG_OBJ['problemId']
    LANGUAGE_LIST = CONFIG_OBJ['language']
    TOOL = CONFIG_OBJ['tools']
    
    print("language,tool,[0,19],[20,39],[40,59],[60,79],[80,99],100 ")
    for language in LANGUAGE_LIST:
        for tool in TOOL:
            data = open("./benchmarkResult/" + tool + "/" + language + "/all.csv","r").readlines()
            for lineIndex in range(len(data)):
                if data[lineIndex][-1] == "\n":
                    data[lineIndex] = data[lineIndex][:-1]
                if data[lineIndex][-1] == ",":
                    data[lineIndex] = data[lineIndex][:-1]
                    
            # [0,19],[20,39],[40,59],[60,79],[80,99],100
            detectedClone = data[2].split(",")[1:]
            allClone      = data[3].split(",")[1:]
            
            if len(detectedClone) < 2 or len(allClone) < 2:
                continue
            
            
            detectedClone_grouped = [0]*6
            allClone_grouped      = [0]*6
            
            groupIndex = 0
            simiIndex  = 0
            for index in range(101):
                detectedClone_grouped[groupIndex] += int(detectedClone[index])
                allClone_grouped[groupIndex] += int(allClone[index])
                simiIndex += 1
                if simiIndex == 20:
                    simiIndex = 0
                    groupIndex += 1
            res = language + "," + tool + ","
            for groupIndex in range(6):
                res = res + str(round( detectedClone_grouped[groupIndex]/allClone_grouped[groupIndex] ,2)) + "," + str(detectedClone_grouped[groupIndex]) + ","
            print(res)
            