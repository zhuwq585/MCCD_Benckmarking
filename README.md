# MCCD_Benckmarking
Let's benchmarking code clone detectors in several languages.


## Recall

### Download data

URL: https://www.dropbox.com/scl/fi/lezo5ul15qg6oudud82fx/RecallBenchmarking.zip?rlkey=pm5grsfq314s2cuw3bbdcm84l&dl=0

unzip RecallBenchmarking.zip, and 2 folders named benchmark-data and simi-source are in it. Put the 2 folders into MCCD_Benchmarking/recall/.

### Using the generated benchmark

0. Execute clone detection for each subset.
   
   problemId: "p02263","p00048","p00001","p00000","p02269","p02256","p02257","p02265","p00002","p00003","p00008","p00050","p02271","p00005"

   Results for each subset should be named as "Language_problemId.csv", and saved into the same folder refer to step 2.

   Each line in "Language_problemId.csv" represents a clone pair, formated in "segment1 file path,segment1 start line,segment1 endline,segment2 file path,segment2 start line,segment2 endline"


1. Add your target tool
   
   ```python3 AddDetector.py ToolName```

   + ``ToolName``: Identifier of the target clone detector. 

2. Import detection results of each subset.
   
    ```python3 ImportClones.py ToolName ResultFolder [Language+]```

    + ``ToolName``: Tool identifier
    + ``ResultFolder``: Path of the folder where results of each subset are. 
    + ``Language``: If only import a part of the target language, list target languages here.
3. Evaluation
   
   ```python3 Evaluation.py [ToolName]```
   + ``ToolName``: Identifier of the target detector. Evaluate all registed tools if not inputed.

4. Output All Results
   ```python3 GroupedData.py```
   + 
5. Clear tools or clones
   ```python3 CloneClones.py ToolName```
   + ``ToolName``: Tool identifier

    ```python3 RemoveDetector.py ToolName```
   + ``ToolName``: Tool identifier

<!-- ### Generate your own benchmark

Comming soon. -->

## Precision

Comming soon.

