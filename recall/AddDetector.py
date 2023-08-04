import ujson, sys, os

TOOL_BASE_PATH  = "./.config.json"
LanguageList = ["Java","Python","C","C++"]


def folderCreation(newToolName) -> bool:
    try:
        # recall/ToolResult/[toolName]/[language]/
        if not os.path.exists("./ToolResult/"):
            os.mkdir("./ToolResult/")
        
        toolResult = "./ToolResult/" + newToolName + "/"
        os.mkdir(toolResult)
        for language in LanguageList:
            os.mkdir(toolResult + language + "/")
        
        # recall/benchmarkResult/[toolName]/[language]/
        benchmarkResult = "./benchmarkResult/" + newToolName + "/"
        os.mkdir(benchmarkResult)
        for language in LanguageList:
            os.mkdir(benchmarkResult + language + "/")
        
        return True
    
    except Exception:
        return False

if __name__ == "__main__":
    newToolName = sys.argv[1]
    description = input("Description: ")
    
    BenchmarkConfig = ujson.loads(open(TOOL_BASE_PATH,"r").read())
    LanguageList = BenchmarkConfig['language']
    
    if not newToolName in BenchmarkConfig['tools']:
        BenchmarkConfig['tools'][newToolName] = {
            "description" : description
        }
        
        if folderCreation(newToolName):
            # save
            open(TOOL_BASE_PATH,"w").write(ujson.dumps(BenchmarkConfig, indent=4))
            print("Added.")
        else:
            print("Err in folder creation.")
        
        
    else:
        print(newToolName + " already exists")    
        
    


