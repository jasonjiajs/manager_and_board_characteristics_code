import sys
import pandas as pd
import os
from pathlib import Path
import re

arraynumber = int(sys.argv[1])
totalnumberofarrays = int(sys.argv[2])
print("This is array", arraynumber, "/", totalnumberofarrays)

dir = Path("/project/kh_mercury_1/boardex/data")
totalFiles = 0
totalDirectories = 0

for root, dirs, files in os.walk(dir, topdown=False):
    for name in dirs:
        totalDirectories += 1

print('Total number of folders:', totalDirectories)

numberoffolders_tocover = int(totalDirectories / totalnumberofarrays)
firstfolder = 1 + numberoffolders_tocover * (arraynumber - 1)
if arraynumber < totalnumberofarrays:
    lastfolder =  1 + numberoffolders_tocover * arraynumber - 1
else: #covers for imperfect division as well (remainder != 0)
    lastfolder = totalDirectories
print('This process will cover folders:', firstfolder, "to", lastfolder)

def get_data_folder_number(foldername):
    pattern = re.compile(r".+_(\d+)$")
    result = pattern.search(name)
    data_foldernumber = int(result.group(1))
    return data_foldernumber

for i in range(firstfolder, lastfolder+1):
    folder = "BoardEx-2021-09-15-Part_" + str(i)
    folderpath = Path(dir / folder)
    print("folder:", folderpath)

    for root, dirs, files in os.walk(folderpath, topdown=False):
        for name in files:
            filepath = Path(os.path.join(root, name))
            # print(filepath)
 
