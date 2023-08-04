import ujson, sys, os
CONFIG_FILE  = "./.config.json"

if __name__ == "__main__":
    CONFIG_OBJ = ujson.loads(open(CONFIG_FILE,"r").read())
    
    ProblemIdList = CONFIG_OBJ['problemId']
    LanguageList = CONFIG_OBJ['language']
    
    targetTool = None
    try:
        targetTool = sys.argv[1]
    except Exception:
        print("No tool inputed.")
        
    if targetTool in CONFIG_OBJ['tools']:
        toolResFolder = "./ToolResult/" + targetTool
        benchmarkResFolder = "./benchmarkResult/" + targetTool
        os.system("rm -rf " + toolResFolder)
        os.system("rm -rf " + benchmarkResFolder)
        
        del CONFIG_OBJ['tools'][targetTool]
        open(CONFIG_FILE,"w").write(ujson.dumps(CONFIG_OBJ, indent=4))
    else:
        print(targetTool + " not found.")