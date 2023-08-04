import os, sys, ujson
CONFIG_FILE  = "./.config.json"


if __name__ == "__main__":
    if len(sys.argv) >= 3 :
        toolName = sys.argv[1]
        sourceFolder = sys.argv[2]
        
        BenchmarkConfig = ujson.loads(open(CONFIG_FILE,"r").read())
        ProblemIdList = BenchmarkConfig['problemId']
        
        try:
            cursor = 3
            LanguageList = []
            LanguageList.append(sys.argv[3])
            while cursor < len(sys.argv):
                cursor += 1
                LanguageList.append(sys.argv[3])
                
        except IndexError:
            LanguageList  = BenchmarkConfig['language']
        
        if toolName in BenchmarkConfig['tools']:
            if os.path.exists(sourceFolder):
                for problemId in ProblemIdList:
                    for language in LanguageList:
                        sourceFile = sourceFolder + "/" + language + "_" + problemId + ".csv"
                        targetFile = "./ToolResult/" + toolName + "/" + language + "/" + language + "_" + problemId + ".csv"
                        os.system("cp " + sourceFile + " " + targetFile)
            else:
                print(sourceFolder + " not exists.")
        else:
            print(toolName + " not added.")
        
        
    else:
        print("Missed parameters")