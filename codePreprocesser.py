import re,os
PROBLEM_LIST = "problemsForCodePreprocesser.csv"
LANGUAGE_LIST = ["Python","Java","C","C++"]
CODENET_DATA = "Project_CodeNet/data/"

LANGUAGE_DICT = {
    "Java":{
        "multilineComment": "/\*(?:.|[\r\n])*?\*/",
        "inlineComment" : "//.*\n"
    },
    "C":{
        "multilineComment": "/\*(?:.|[\r\n])*?\*/",
        "inlineComment" : "//.*\n"
    },
    "C++": {
        "multilineComment": "/\*(?:.|[\r\n])*?\*/",
        "inlineComment" : "//.*\n"
    },
    "Python": {
        "inlineComment": "#.*\n",
        "multilineComment" : '"""(?:.|[\r\n])*?"""'
    }
}

def codePreprint(language, sourceFilePath):
    
    # Read source code
    try:
        source = open(sourceFilePath,"r").read()
    except FileNotFoundError:
        print("Filt not found: " + sourceFilePath)
        return None
    
    # Remove MultilineComments
    pattern = re.compile(LANGUAGE_DICT[language]["multilineComment"])
    if language == "Python":
        searchRes = []
        while True:
            matchRes = pattern.search(source)
            if matchRes == None:
                break
            else:
                searchRes.append([matchRes.start(), matchRes.end(), source[matchRes.start():matchRes.end()]])
                # print(str(matchRes.start()) + "," + str(matchRes.end()))
                # print(len(source))
                # print(source[matchRes.start():matchRes.end()])
                source = source[:matchRes.start()] + "#"*(matchRes.end() - matchRes.start()) + source[matchRes.end():]
                # print(source[matchRes.start():matchRes.end()])


        # if len(searchRes) > 0:
        #     print(sourceFilePath)
        
        for searchedMultilineString in searchRes:
            cursor = searchedMultilineString[0] - 1
            cursorSta = True

            while cursor >= 0 and cursorSta:
                if re.match("\s", source[cursor]):
                    cursor -= 1
                else:
                    if source[cursor] == "=": # replace @@@@ with original code
                        source = source[:searchedMultilineString[0]] + searchedMultilineString[-1] + source[searchedMultilineString[1]:]
                    else: # remove @@@@
                        pass
                        # tmp = searchedMultilineString[-1].split("\n")
                        # tmp = "#" + "\n#".join(tmp)
                        # source = source[:searchedMultilineString[0]] + tmp + source[searchedMultilineString[1]:]
                    cursorSta = False
        
                # cursor = matchRes.start() - 1
                # cursorSta = True
                # while cursor >= 0 and cursorSta:
                #     if re.match("\s", source[cursor]):
                #         cursor -= 1
                #     else:
                #         if source[cursor] == "=":
                #             cursorSta = False
                #         else:
                #             source = source[:matchRes.start()] + source[matchRes.end():]
                #             cursorSta = False

                            
    else:
        while True:
            matchRes = pattern.search(source)
            if matchRes == None:
                break
            else:
                source = source[:matchRes.start()] + source[matchRes.end():]        
    
    # Remove SinglelineComments
    pattern = re.compile(LANGUAGE_DICT[language]["inlineComment"])
    while True:
        matchRes = pattern.search(source)
        if matchRes == None:
            break
        else:
            source = source[:matchRes.start()] + source[matchRes.end()-1:]     
    
    # Remove Continus Break-Newline
    lines = source.split("\n")
    pattern = re.compile("\S")
    res = []
    for line in lines:
        tmp = pattern.search(line)
        if tmp != None:
            res.append(line)
    
    source = "\n".join(res)
      
    try:
        if source[0] == "\n":
            source = source[1:]
        if source[-1] == "\n":
            source = source[:-1]
    except IndexError:
        print(sourceFilePath)
        
    return source

if __name__ == "__main__":
    Problem_List = []
    with open(PROBLEM_LIST,"r") as f:
        for line in f.readlines():
            if line[-1] == "\n":
                Problem_List.append(line[:-1])
            else:
                Problem_List.append(line)
                
    for language in LANGUAGE_LIST:
        for problemId in Problem_List:
            print("Executing: " + language + " - " + problemId)
            File_List_File = "./fileList_accepted/" + problemId + "/" + language + ".txt"
            File_List = []
            with open(File_List_File,"r") as f:
                for line in f.readlines():
                    File_List.append(CODENET_DATA +  (line if line[-1]!="\n" else line[:-1]))
            targetFolder = "./preprintedData/" + problemId + "/" + language + "/"

            if not os.path.exists(targetFolder):
                os.system("mkdir -pv " + targetFolder)

            for file in File_List:
                targetFile = targetFolder + file.split("/")[-1]
                # if os.path.exists(targetFile):
                #     continue
                preprintedCode = codePreprint(language, file)
                
                with open(targetFile,"w") as f:
                    f.write(preprintedCode)
        # codePreprint("Python","/Users/syu/workspace/Project_CodeNet/data/p03140/Python/s750776801.py")