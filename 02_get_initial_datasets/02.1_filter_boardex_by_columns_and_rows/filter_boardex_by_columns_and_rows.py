import pandas as pd, numpy as np
from pathlib import Path
import os, sys, glob, re
from itertools import compress

# Print out arguments passed to the program
arraynumber = int(sys.argv[1])
totalnumberofarrays = int(sys.argv[2])
listofcols_path = Path(sys.argv[3])
companyid_listpath = Path(sys.argv[4])
inputfolder = Path(sys.argv[5])
outputfolder = Path(sys.argv[6])
# get_only_characteristics_and_educationandachievements = int(sys.argv[6])

print("Output from Python Script:")
print("This is array", arraynumber, "/", totalnumberofarrays)
print("Filepath of .xslx containing list of columns in Boardex and ExecuComp:", str(listofcols_path))
print("Filepath to list of company IDs we want to filter by:", companyid_listpath)
print("Input Folder (containing raw BoardEx .xlsx files):", str(inputfolder))
print("Output Folder (after we filter by both columns and rows):", str(outputfolder))
# print("Get only 'Characteristics' and 'EducationandAchievements':", str(get_only_characteristics_and_educationandachievements))

# Use glob to return all excel files in the input directory (recursively)
# i.e. all files in inputfolder, all files in all subfolders of inputfolder and so on
file_list = glob.glob(str(inputfolder) + "/**/*.xlsx", recursive=True)

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
df_listofcols = pd.read_excel(listofcols_path, sheet_name=['ExecuComp', 'Boardex - Europe'], engine='openpyxl')

# Get df for execucomp (not needed here)
# df_execucomp = df_listofcols['ExecuComp']

# Get and process the list of columns for Boardex files
def get_and_process_boardex_listofcols(df_listofcols):
    # Get df for boardex and filter to keep the relevant columns
    df_boardex = df_listofcols['Boardex - Europe']
    df_boardex = df_boardex[['Include in Dataset', 'Excel Workbook', 'Excel Workbook (SMDEs)', 'Sheet', 'Variable Name']]

    # Filter to keep only variables that you want to keep 
    df_boardex = df_boardex[df_boardex['Include in Dataset'] == 1]
    df_boardex = df_boardex.reset_index(drop=True)

    # Substitute 'Europe - ' with '' in string_to_replace at all occurances
    df_boardex['Excel Workbook'] = df_boardex['Excel Workbook'].str.replace('Europe - ','')
    df_boardex['Excel Workbook (SMDEs)'] = df_boardex['Excel Workbook (SMDEs)'].str.replace('Europe - ','')

    # Remove unexpected characters
    df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('\t','')

    # Rename 'Director Type (ED or SD)' to 'Director Type', because different excel files name it differently, 
    # e.g. 'Director Type (ED or SD)' or Director Type (ED , SD or SM)''
    df_boardex['Variable Name'] = df_boardex['Variable Name'].str.replace('Director Type (ED or SD)', 'Director Type', regex=False)

    # Get unique list of excel workbook names
    unique_workbook_names = df_boardex['Excel Workbook'].unique()
    unique_workbook_names_smde = df_boardex['Excel Workbook (SMDEs)'].unique()

    # Remove NaN (float) from an array of valid file names (strings) and NaN (float).
    unique_workbook_names = unique_workbook_names[~pd.isnull(unique_workbook_names)]
    unique_workbook_names_smde = unique_workbook_names_smde[~pd.isnull(unique_workbook_names_smde)]

    return df_boardex, unique_workbook_names, unique_workbook_names_smde

df_boardex, unique_workbook_names, unique_workbook_names_smde = get_and_process_boardex_listofcols(df_listofcols)

# Load the list of company IDs
companyid_list = pd.read_excel(companyid_listpath, engine='openpyxl')['Boardex CompanyID'].dropna().astype('int64').tolist()

# Define functions for main loop
def get_colstokeep(unique_workbook_name, df_boardex, sheet_name):
    list_colstokeep = []
    
    # Filter by unique_workbook_name
    if 'SMDE' in unique_workbook_name:
        df_boardex = df_boardex[df_boardex['Excel Workbook (SMDEs)'] == unique_workbook_name]
    else:
        df_boardex = df_boardex[df_boardex['Excel Workbook'] == unique_workbook_name]
        
    # Filter by sheet
    df_boardex = df_boardex[df_boardex['Sheet'] == sheet_name]

    # Get list of unique columns to keep
    list_colstokeep = list(df_boardex['Variable Name'].unique())
    # print("List of cols to keep (before processing):", list_colstokeep)

    # Strip/trim columns in list_colstokeep to maintain consistency
    list_colstokeep = [col.strip() for col in list_colstokeep]
    print("List of cols to keep (after processing):", list_colstokeep)
    
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

def get_df(filepath, sheet_name):
    # Get % NaN values in first row
    # This is because some files have 2 rows as column headers. Row 1 indicates category, where cells in the same category are merged (and thus we interpolate using forward fill). Row 2 indicates the column name. We need both to uniquely identify columns.
    # Other files only have 1 row as the column header, which is the ideal case.
    # Note: We need to specify the sheet name and not just the sheet index (e.g. Sheet 0), because the order of the sheets is different across years for some workbooks. For example, Europe - SMDEs Compensation workbooks typically have the desired sheet 'Summary' in sheet 0, but Europe - SMDEs Compensation - 2001 has the desired sheet 'Summary' in sheet 2. If we read sheet 0, it reads the wrong sheet 'Direct'.
    row0 = pd.read_excel(filepath, sheet_name=sheet_name, header=None, nrows = 1, engine='openpyxl')
    pct_nan = round(pd.isna(row0).sum().mean() * 100, 1)
    if pct_nan > 0.3:
        print("% NaNs in first row:", pct_nan, "> 30%, taking category = row 0 and variable name = row 1")
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=None, engine='openpyxl')
        
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
        print("% NaNs in first row", pct_nan, "<= 30%, taking header = row 0 as usual")
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=0, engine='openpyxl')
    
    return df

# Process df columns
def process_df_cols(df):
    # print("df.columns (before processing):", df.columns)

    # Rename 'Director Type (...)' to 'Director Type', because different excel files name it differently, 
    # e.g. 'Director Type (ED or SD)' or Director Type (ED , SD or SM)''
    list_bools_colheaders = ['Director Type' in column_header for column_header in df.columns]
    if any(list_bools_colheaders):
        coltoreplace = list(compress(df.columns, list_bools_colheaders))[0]
        df = df.rename(columns = {coltoreplace: "Director Type"})
    
    # Strip/trim column headers of df to maintain consistency
    # Strip doesn't remove the excess spaces in '  - '. We remove these spaces using regex.
    columns_dict = {}
    for column_header in df.columns:
        columns_dict[column_header] = re.sub(pattern=' {2,}', repl=' ', string=column_header.strip())
    df = df.rename(columns = columns_dict)
    print("df.columns (after processing):", df.columns)

    return df

def find_first_column_containing_companyid(df):
    for column in df.columns:
        if "companyid" in column.lower():
            return column
    return None

# Main loop
# Go through each file in the directory and filter by columns and rows
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
            if 'SMDE' in name:
                list_bools_workbook_names = [workbook_name in name for workbook_name in unique_workbook_names_smde]
            else:
                list_bools_workbook_names = [workbook_name in name for workbook_name in unique_workbook_names]

            if(any(list_bools_workbook_names)):
                # Keep track of list of files kept
                list_files_kept.append(name)
                print("File name (kept):", name)
                
                # Get the unique workbook name
                if 'SMDEs' in name:
                    unique_workbook_name = list(compress(unique_workbook_names_smde, list_bools_workbook_names))[0]
                else:
                    unique_workbook_name = list(compress(unique_workbook_names, list_bools_workbook_names))[0]
                print("Unique workbook name:", unique_workbook_name)
                
                # Check how many sheets need to be opened for this file.
                list_sheetstoopen = get_sheetstoopen(unique_workbook_name, df_boardex) 
                print("List of sheets to open:", list_sheetstoopen)
                num_sheets = len(list_sheetstoopen)
                
                for sheet_index, sheet_name in enumerate(list_sheetstoopen):
                    # Convert sheet name to string as some sheet names are ints by default (e.g. 1999)
                    sheet_name = str(sheet_name)

                    # Open the specific sheet in file
                    # Most files (e.g. files that contain company ID) will only have 1 sheet.
                    # Some files (e.g. education & achievements) have multiple sheets. 
                    print("------")
                    print("Sheet", sheet_index, ":", sheet_name)
                    df = get_df(file, sheet_name)
                    print("df.shape:", df.shape)

                    # ------ PART 1 ------
                    print("---\nFiltering df by columns:\n---")

                    # Process df columns
                    df = process_df_cols(df)

                    # Get columns to keep
                    list_colstokeep = get_colstokeep(unique_workbook_name, df_boardex, sheet_name)

                    # Filter by the columns we want
                    df = df[list_colstokeep]
                    print("df.shape:", df.shape)
                    print("Done!")

                    # ------ PART 2 ------
                    print("---\nFiltering df by rows:\n---")

                    # Find the first variable that contains the word 'companyid', if there is one
                    companyid = find_first_column_containing_companyid(df)

                    # If a companyid variable is found, filter df by rows, based on list of company ids provided.
                    # Else, do nothing.
                    if companyid != None:
                        print("Found column that contains 'companyid', filtering by rows.")
                        df = df[df[companyid].isin(companyid_list)]
                    else:
                        print("No column found that contains 'companyid', not filtering by rows.")
                    print("df.shape:", df.shape)

                    # Save df if it is non-empty
                    if (df.shape[0] > 0) and (df.shape[1] > 0):
                        if len(list_sheetstoopen) > 1:
                            outputfilename = stem + '_' + sheet_name + '.xlsx'
                        else:
                            outputfilename = stem + '.xlsx'
                        outputfilepath = Path(outputfolder / outputfilename)
                        df.to_excel(outputfilepath, index=False)
                        print("df saved to:", str(outputfilepath))
                    else:
                        # Nothing to save
                        print("Note: df has no rows and/or columns!")
                    print("Done!")
                print("-----------------------------------------------------------")
                
            else:
                # Keep track of list of files not kept
                list_files_not_kept.append(name)      
        
        filenumber += 1

# Print list of files kept and not kept
print("List of files kept:", list_files_kept)
print("------")
print("List of files not kept:", list_files_not_kept)
