import sys
import pandas as pd
import os
from pathlib import Path
import re

# Print out arguments passed to the program
arraynumber = int(sys.argv[1])
totalnumberofarrays = int(sys.argv[2])
dir = Path(sys.argv[3])
outputfolder = Path(sys.argv[4])
companyid_listpath = Path(sys.argv[5])
print("This is array", arraynumber, "/", totalnumberofarrays)
print("Input Dir:", str(dir))
print("Output Dir:", str(outputfolder))
print("Filepath to list of company IDs we want to filter by:", companyid_listpath)

# Load the list of company IDs
companyid_list = pd.read_excel(companyid_listpath, engine='openpyxl')['Boardex CompanyID'].dropna().astype('int64').tolist()

# Get total number of files
totalFiles = 0
file_list = []
for file in os.listdir(dir):
    if ".xlsx" in file:
        totalFiles +=1
        file_list.append(file)
print('Total number of files:', totalFiles)

# Get first and last file to cover for this process
if totalFiles <= totalnumberofarrays:
    numberoffiles_tocover = 1
else:
    numberoffiles_tocover = int(totalFiles / totalnumberofarrays)

if totalFiles < arraynumber:
    print('This process is not needed, since only the first', totalFiles, 'processes are needed.')
firstnumber = 1 + numberoffiles_tocover * (arraynumber - 1)
if arraynumber < totalnumberofarrays:
    lastnumber =  1 + numberoffiles_tocover * arraynumber - 1
else: #covers for imperfect division as well (remainder != 0)
    lastnumber = totalFiles

if arraynumber <= totalFiles:
    print('This process will cover file(s):', firstnumber, "to", lastnumber)

print("-------------------------------------------")

# Define some functions
'''
def get_data_folder_number(foldername):
    pattern = re.compile(r".+_(\d+)$")
    result = pattern.search(name)
    data_foldernumber = int(result.group(1))
    return data_foldernumber
'''
def get_df(filepath):
    row0 = pd.read_excel(filepath, header=None, nrows = 1, engine='openpyxl')
    pct_nan = round(pd.isna(row0).sum().mean() * 100, 1)
    if pct_nan > 0.5:
        print("% NaNs in first row:", pct_nan, "> 50%, taking category = row 0 and variable name = row 1")
        df = pd.read_excel(filepath, header=None, engine='openpyxl')
        
        # Get categories using forward fill. For identifiers, there is no category and so we get NaN.
        # This formula accounts for the following cases:
        # (Identifiers) NaN + Annual Report Year -> Annual Report Year (because NaN + ' - ' = NaN) 
        # (Director profile - characteristics) Annual Report Year + NaN -> Annual Report Year
        # (Everything else) Characteristics of Roles + Individual Role -> Characteristics of Roles - Individual Role
        df_columns = df.iloc[0,:].ffill().fillna('') + ' - ' + df.iloc[1,:].fillna('')
        df_columns = df_columns.str.replace('^ - ', '', regex=True)
        df_columns = df_columns.str.replace(' - $', '', regex=True)
        df.columns = df_columns

        # Remove the first two rows (which are column headers)
        df = df.iloc[2:,:]
    else:
        print("% NaNs in first row", pct_nan, "<= 50%, taking header = row 0 as usual")
        df = pd.read_excel(filepath, header=0, engine='openpyxl')
    
    return df

def find_first_column_containing_companyid(df):
    for column in df.columns:
        if "companyid" in column.lower():
            return column
    return None

def walkdir_print_dirs(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            print(os.path.join(root, name))
            print(name)

# Go through each file in the directory and filter by the list of company IDs provided
filenumber = 1
for i in range(firstnumber, lastnumber+1):
    for name in file_list:
        # Only handle files allocated to this process
        if filenumber >= firstnumber and filenumber <= lastnumber:
            # Print filepath
            filepath = Path(os.path.join(dir, name))
            print("Filepath:", filepath)

            # Get the df and find the first variable that contains the word 'companyid'
            df = get_df(filepath)
            print("df.columns:", df.columns)
            companyid = find_first_column_containing_companyid(df)
            
            # Skip df if no such variable is found
            if companyid == None:
                print("No column found that contains 'companyid', skipping df")
            # Process variable if such a variable is found
            else:
                # Get the output filepath
                outputfilename = filepath.stem + "_filtered" + filepath.suffix
                outputfilepath = Path(outputfolder / outputfilename)
                # Filter df based on list of company ids provided
                df_filtered = df[df[companyid].isin(companyid_list)]
                if df_filtered.shape[0] > 0:
                    # Save to outputfilepath
                    df_filtered.to_excel(outputfilepath, index=False)
                    print("Shape of filtered df:", df_filtered.shape)
                    print("Saved filtered df to:", outputfilepath)
                else:
                    # Nothing to save
                    print("No matching entries in this df, skipping df")
            print("-------------------------------------------")

        filenumber += 1
 
