import os 

class CloneDict:
    def __init__(self, infoFilePath) -> None:
        self.segmentDict = {} # id -> filePath, startLine, endLine
        self.clonePair = {} # segment1 -> segment2 -> count, [similarity]
        self.truePositive_num = 0
        self.allPairNum = 0
        
        if not self.__initialize(infoFilePath):
            print("CloneDict initialization failed.")
        
    def __initialize(self, infoFilePath):
        if not os.path.exists(infoFilePath):
            print("File not found: " + infoFilePath)
            return None
        
        with open(infoFilePath,'r') as f:
            status = 0
            lineTmp = None
            splitTmp = None
            for line in f.readlines():
                lineTmp = line if line[-1]!='\n' else line[:-1]
                splitTmp = lineTmp.split(",")
            
                if len(splitTmp) == 1:
                    # change status
                    if splitTmp[0] == "segmentDict":
                        status = 1
                    elif splitTmp[0] == "clonePair":
                        status = 2
                elif len(splitTmp) > 1:
                    # read data
                    if status == 1:
                        self.segmentDict[splitTmp[0]] = {
                            "filePath" : splitTmp[1],
                            "startLine": int(splitTmp[2]),
                            "endLine"  : int(splitTmp[3]),
                            "tokenNum" : int(splitTmp[4])
                            }
                    elif status == 2:
                        tmp = self.__segmentIdSort(splitTmp[0],splitTmp[1])
                        if not tmp[0] in self.clonePair:
                            self.clonePair[tmp[0]] = {}
                        self.clonePair[tmp[0]][tmp[1]] = [splitTmp[2], 0] # [similarity, count]
                        self.allPairNum += 1
                else:
                    continue
        return True
    
    def __segmentIdSort(self, id1, id2):
        return (id1, id2) if int(id1) <= int(id2) else (id2, id1)


class CloneMatcher:
    def __init__(self, infoFilePath, coverage) -> None:
        self.cloneDict = CloneDict(infoFilePath)
        self.reportedClones = [] # imported clones
        self.matchedReportedClones = [] # matched clones in imported clones
        self.trueMatchedReportedClones = []
        
        coverage = float(coverage)
        if coverage >= 0 and coverage <= 1:
            self.coverage = coverage
        
    def clear(self):
        self.reportedClones = []
        self.matchedReportedClones = []
        self.trueMatchedReportedClones = []
    
    def importClone(self, reportFile) -> bool:
        if not os.path.exists(reportFile):
            print("Report file not found: " + reportFile)
            return None
        
        with open(reportFile,"r") as f:
            lineTmp  = None
            splitTmp = None
            for line in f.readlines():
                lineTmp = line if line[-1] != '\n' else line[:-1]
                splitTmp = lineTmp.split(",")
                
                if len(splitTmp) == 6:
                    subId1 = self.getSubmissionIdFromPath(splitTmp[0])
                    subId2 = self.getSubmissionIdFromPath(splitTmp[3])
                    
                    if int(subId1) <= int(subId2):
                        self.reportedClones.append([subId1,int(splitTmp[1]),int(splitTmp[2]),subId2, int(splitTmp[4]), int(splitTmp[5])]    )     
                    else:
                        self.reportedClones.append([subId2,int(splitTmp[4]),int(splitTmp[5]),subId1, int(splitTmp[1]), int(splitTmp[2])]    )     
                elif len(splitTmp) == 2:
                    subId1 = self.getSubmissionIdFromPath(splitTmp[0])
                    subId2 = self.getSubmissionIdFromPath(splitTmp[1])
                    
                    if int(subId1) <= int(subId2):
                        self.reportedClones.append([subId1,1,-1,subId2, 1, -1]    )     
                    else:
                        self.reportedClones.append([subId2,1,-1,subId1, 1, -1]    )     
                    
        self.checkAllReportedClones4LineCoverage()
        
    def checkAllReportedClones4LineCoverage(self):
        for reportedClone in self.reportedClones:
            if self.segmentCoverageCheck(reportedClone[0],reportedClone[1],reportedClone[2]) and self.segmentCoverageCheck(reportedClone[3],reportedClone[4],reportedClone[5]):
                self.matchedReportedClones.append(reportedClone)
                       
                
    
    def cloneMatch(self):
        matchedClone = []
        
        for reportedClone in self.matchedReportedClones:

            if reportedClone[0] in self.cloneDict.clonePair:
                if reportedClone[3] in self.cloneDict.clonePair[reportedClone[0]]:
                        matchedClone.append(reportedClone)
                        self.cloneDict.clonePair[reportedClone[0]][reportedClone[3]][1] += 1

        
        self.trueMatchedReportedClones = matchedClone
        return matchedClone
    
    def getUnmatchedClone(self):
        unmatchedClone = []
        for id1 in self.cloneDict.clonePair:
            for id2 in self.cloneDict.clonePair[id1]:
                if self.cloneDict.clonePair[id1][id2][1] == 0:
                    unmatchedClone.append((id1,id2))
        
        return unmatchedClone
    
    def segmentCoverageCheck(self, sid, reportedStartLine, reportedEndLine) -> bool:
        ## block-level になる際に修正が必要
        if reportedEndLine == -1:
            return True
        else:
            try:
                return reportedEndLine - reportedStartLine + 1 >= round((self.cloneDict.segmentDict[sid]['endLine'] - self.cloneDict.segmentDict[sid]['startLine'] + 1) * self.coverage)
            except KeyError:
                print("Unmatched sid: " + sid)
                return False    
    def getSubmissionIdFromPath(self, path) -> str:
        return path.split("/")[-1][1:].split(".")[0]