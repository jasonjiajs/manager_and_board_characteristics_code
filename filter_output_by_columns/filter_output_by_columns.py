import pandas as pd, numpy as np
from pathlib import Path
import os, sys, glob
from itertools import compress

# Print out arguments passed to the program
arraynumber = int(sys.argv[1])
totalnumberofarrays = int(sys.argv[2])
listofcols_path = Path(sys.argv[3])
inputfolder = Path(sys.argv[4])
outputfolder = Path(sys.argv[5])
get_only_characteristics_and_educationandachievements = int(sys.argv[6])

print("Output from Python Script:")
print("This is array", arraynumber, "/", totalnumberofarrays)
print("File path of .xslx containing list of columns in Boardex and ExecuComp:", str(listofcols_path))
print("Input Folder (containing .xlsx filtered by isins):", str(inputfolder))
print("Output Folder (after we further filter by columns):", str(outputfolder))
print("Get only 'Characteristics' and 'EducationandAchievements':", str(get_only_characteristics_and_educationandachievements))


# Use glob to return all excel files in the input directory
file_list = glob.glob(str(inputfolder) + "/*.xlsx")

# Convert the strings back into paths
file_list = [Path(file) for file in file_list]

# Get total number of files
totalFiles = len(file_list)
print('Total number of files in input folder:', totalFiles)

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

print("-----------------------------------------------------------")

# Import list_of_columns.xlsx for boardex
df = pd.read_excel(listofcols_path, sheet_name=['ExecuComp', 'Boardex - Europe'], engine='openpyxl')

# Get df for execucomp (not needed here)
# df_execucomp = df['ExecuComp']
# df_execucomp

# Get df for boardex and filter to keep the relevant columns
df_boardex = df['Boardex - Europe']
df_boardex = df_boardex[['Include in Dataset', 'Excel Workbook', 'Excel Workbook (SMDEs)', 'Sheet', 'Variable Name']]

# Filter to keep only variables that you want to keep 
df_boardex = df_boardex[df_boardex['Include in Dataset'] == 1]
df_boardex = df_boardex.reset_index(drop=True)

# Substitute 'Europe - ' with '' in string_to_replace at all occurances
df_boardex['Excel Workbook'] = df_boardex['Excel Workbook'].str.replace('Europe - ','')
df_boardex['Excel Workbook (SMDEs)'] = df_boardex['Excel Workbook (SMDEs)'].str.replace('Europe - ','')

# Remove the "[...] - " part from variable names, because it's the header and not the actual variable name
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Characteristics of Roles\t - ','')
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Director Experience - ','')
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Ratios - ','')
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Director Count Totals - ','')
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Ratios - ','')
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Annual Direct Compensation - ','')
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Total - ','')

# Rename 'Director Type (ED or SD)' to 'Director Type', because different excel files name it differently, 
# e.g. 'Director Type (ED or SD)' or Director Type (ED , SD or SM)''
df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Director Type \\(ED or SD\\)', 'Director Type')

# Get unique list of excel workbook names
unique_workbook_names = df_boardex['Excel Workbook'].unique()
unique_workbook_names_smde = df_boardex['Excel Workbook (SMDEs)'].unique()
unique_workbook_names = np.append(unique_workbook_names, unique_workbook_names_smde)

# Remove NaN (float) from an array of valid file names (strings) and NaN (float).
unique_workbook_names = unique_workbook_names[~pd.isnull(unique_workbook_names)]

# If specified, just get the 'Characteristics' and 'Education & Achievements' workbooks.
if get_only_characteristics_and_educationandachievements == 1:
    unique_workbook_names = ['Director Profile - Characteristics', 'Director Profile - Education & Achievements', 'SMDEs Profile - Characteristics', 'SMDEs Profile - Education & Achievements']

# Define functions for main loop
def get_colstokeep(unique_workbook_name, df_boardex, sheet):
    list_colstokeep = []
    
    # Filter by unique_workbook_name
    if 'SMDE' in unique_workbook_name:
        df_boardex = df_boardex[df_boardex['Excel Workbook (SMDEs)'] == unique_workbook_name]
    else:
        df_boardex = df_boardex[df_boardex['Excel Workbook'] == unique_workbook_name]
        
    # Filter by sheet
    df_boardex = df_boardex[df_boardex['Sheet'] == sheet]

    # Get list of unique columns to keep
    list_colstokeep = list(df_boardex['Variable Name'].unique())
    
    return list_colstokeep

def get_sheetstoopen(unique_workbook_name, df_boardex):
    list_sheetstoopen = []
    
    # Filter by unique_workbook_name
    if 'SMDE' in unique_workbook_name:
        df_boardex = df_boardex[df_boardex['Excel Workbook (SMDEs)'] == unique_workbook_name]
    else:
        df_boardex = df_boardex[df_boardex['Excel Workbook'] == unique_workbook_name]
    
    # Get list of unique sheets to keep
    list_sheetstoopen = list(df_boardex['Sheet'].unique())
    
    return list_sheetstoopen

def get_df(filepath, sheet):
    row0 = pd.read_excel(filepath, sheet_name=sheet, header=None, nrows = 1, engine='openpyxl')
    pct_nan = round(pd.isna(row0).sum().mean() * 100, 1)
    if pct_nan > 0.5:
        print("% NaNs in first row:", pct_nan, "> 50%, taking header = row 1 by skipping row 0")
        df = pd.read_excel(filepath, sheet_name=sheet, header=1, engine='openpyxl')
    else:
        print("% NaNs in first row", pct_nan, "<= 50%, taking header = row 0 as usual")
        df = pd.read_excel(filepath, sheet_name=sheet, header=0, engine='openpyxl')
    
    return df

# Main loop
list_files_kept = []
list_files_not_kept = []

filenumber = 1
for i in range(firstnumber, lastnumber+1):
    for file in file_list:
        # Only handle files allocated to this process
        if filenumber >= firstnumber and filenumber <= lastnumber:
            stem = file.stem
            name = file.name

            # Check if the current file name is a substring of any of the unique workbook names
            list_bools_workbook_names = [workbook_name in name for workbook_name in unique_workbook_names]

            if(any(list_bools_workbook_names)):
                # Keep track of list of files kept
                list_files_kept.append(name)
                print("File name (kept):", name)
                
                # Get the unique workbook name
                unique_workbook_name = list(compress(unique_workbook_names, list_bools_workbook_names))[0]
                print("Unique workbook name:", unique_workbook_name)
                
                # Check how many sheets need to be opened for this file.
                list_sheetstoopen = get_sheetstoopen(unique_workbook_name, df_boardex) 
                print("List of sheets to open:", list_sheetstoopen)
                num_sheets = len(list_sheetstoopen)
                
                for sheet_index, sheet in enumerate(list_sheetstoopen):
                    # Open the specific sheet in file
                    print("------")
                    print("Sheet", sheet_index, ":", sheet)
                    df = get_df(file, sheet_index)
                    print("df.columns (before processing):", df.columns)

                    # Rename 'Director Type (...)' to 'Director Type', because different excel files name it differently, 
                    # e.g. 'Director Type (ED or SD)' or Director Type (ED , SD or SM)''
                    list_bools_colheaders = ['Director Type' in column_header for column_header in df.columns]
                    if any(list_bools_colheaders):
                        coltoreplace = list(compress(df.columns, list_bools_colheaders))[0]
                        df = df.rename(columns = {coltoreplace: "Director Type"})
                    
                    # Strip/trim column headers of df to maintain consistency
                    columns_dict = {}
                    for column_header in df.columns:
                        columns_dict[column_header] = column_header.strip() 
                    df = df.rename(columns = columns_dict)
                    print("df.columns (after processing):", df.columns)

                    # Get columns to keep
                    list_colstokeep = get_colstokeep(unique_workbook_name, df_boardex, sheet)
                    print("List of cols to keep (before processing):", list_colstokeep)

                    # Strip/trim columns in list_colstokeep to maintain consistency
                    list_colstokeep = [col.strip() for col in list_colstokeep]
                    print("List of cols to keep (after processing):", list_colstokeep)

                    # Filter by the columns we want
                    df = df[list_colstokeep]
                    
                    # Save df if it is non-empty (should always be the case, since 
                    # the output .xlsx files are all non-empty)
                    if (df.shape[0] > 0) and (df.shape[1] > 0):
                        if len(list_sheetstoopen) > 1:
                            outputfilename = stem + '_sheet' + str(sheet_index) + '_cols.xlsx'
                        else:
                            outputfilename = stem + '_cols.xlsx'
                        outputfilepath = Path(outputfolder / outputfilename)
                        df.to_excel(outputfilepath, index=False)
                        print("df saved to:", str(outputfilepath))
                    else:
                        # Nothing to save
                        print("Warning: df has no rows and/or columns!")
                print("-----------------------------------------------------------")
                
            else:
                # Keep track of list of files not kept
                list_files_not_kept.append(name)      
        
        filenumber += 1 
         

# Print list of files kept and not kept
print("List of files kept:", list_files_kept)
print("------")
print("List of files not kept:", list_files_not_kept)