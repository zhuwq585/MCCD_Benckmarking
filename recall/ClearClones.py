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
        for pId in ProblemIdList:
            for language in LanguageList:
                resultFile = "./ToolResult/" + targetTool + "/" + language + "/" + language + "_" + pId + ".csv"
                os.system("rm " + resultFile)
        
        del CONFIG_OBJ['tools'][targetTool]
        
        open(CONFIG_FILE,"w").write(ujson.dumps(CONFIG_OBJ, indent=4))
    else:
        print(targetTool + " not found.")