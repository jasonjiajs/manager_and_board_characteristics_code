import pandas as pd, numpy as np
from pathlib import Path
import os, sys, glob, re
from itertools import compress
 
inputfolder = Path(sys.argv[1])
outputfolder = Path(sys.argv[2])
director_smde_map_filepath = Path(sys.argv[3])

print("Input Folder:", str(inputfolder))
print("Output Folder:", str(outputfolder))
print("Filepath of map between director and SMDE workbook names:", str(director_smde_map_filepath))

# ------ PART 1: GET IDENTIFIERS ------
print("\n-----------------------------------------------------------")
print("PART 1: GET IDENTIFIERS")
print("-----------------------------------------------------------")

# Get identifiers of file
def get_identifiers(inputfilepath):
    '''
    General format (no .xlsx as we are just taking the filestem):
    - [geographic region] - [director/SMDE + workbook name] - [fragment number]_[sheet name] 
    - not all files have a fragment number or sheet name.

    Breaking down the regex pattern:
    - ^ asserts the start of the string.
    - (.*?) is the first capturing group and captures any characters (non-greedy) before and after the hyphens. This group captures the region.
    - \- matches the literal hyphen surrounded by spaces.
    - (.*?) is the second capturing group and captures any characters (non-greedy) between the hyphens. This group captures the name.
    - (?: - (\d+))? is a non-capturing group that matches an optional hyphen followed by one or more digits. The (?: ... ) denotes a non-capturing group. The ? makes the hyphen and digits optional. This group captures the fragment.
    - (?:_(.*))? is another non-capturing group that matches an optional underscore followed by any characters. Again, (?: ... ) denotes a non-capturing group. The ? makes the underscore and characters optional. This group captures the sheet.
    - $ asserts the end of the string.

    Capturing groups:
    - Group 1: (.*?) captures the region. It includes any characters (non-greedy) before and after the hyphens.
    - Group 2: (.*?) captures the name. It includes any characters (non-greedy) between the hyphens.
    - Group 3: (?: - (\d+))? captures the fragment. It matches an optional hyphen followed by one or more digits.
    - Group 4: (?:_(.*))? captures the sheet. It matches an optional underscore followed by any characters.

    Here's an example breakdown using the string "UK - Board Characteristics - 10_version 1":
    - Group 1: UK (region)
    - Group 2: Board Characteristics (name)
    - Group 3: 10 (fragment)
    - Group 4: version 1 (sheet)
    '''
    # Get filestem (filename without the extension, e.g. 'UK - Board Characteristics - 10_version 1')
    inputfilestem = inputfilepath.stem
    
    # Do regex matching and get identifiers
    pattern = r'^(.*?) - (.*?)(?: - (\d+))?(?:_(.*))?$'
    match = re.match(pattern, inputfilestem)
    region = match.group(1).strip()
    workbook_name = match.group(2).strip()
    fragment_number = match.group(3).strip() if match.group(3) else None
    sheet_name = match.group(4).strip() if match.group(4) else None
    mgmt_type = 'SMDE' if 'SMDE' in workbook_name else 'Director'

    print(f"Filestem: {inputfilestem}")
    print(f"Identifiers: region={region}, mgmt_type={mgmt_type}, workbook_name={workbook_name}, fragment_number={fragment_number}, sheet_name={sheet_name}")
    print("------")
    
    # Combine identifiers together with filepath and filestem into a single-row df
    inputfile_identifiers = pd.DataFrame({'inputfilepath': inputfilepath, 'inputfilestem': inputfilestem, 'region': region, 'mgmt_type': mgmt_type, 'workbook_name': workbook_name, 'fragment_number': fragment_number, 'sheet_name': sheet_name}, index=[0])

    return inputfile_identifiers

# Get list of files in input folder (no recursive walk)
inputfilenames = [f for f in os.listdir(inputfolder) if f.endswith('.xlsx') or f.endswith('.xls')]
inputfilenames.sort()

df_identifiers = pd.DataFrame(columns=['inputfilepath', 'inputfilestem', 'region', 'mgmt_type', 'workbook_name', 'fragment_number', 'sheet_name'])

# Iterate over the files, get the identifiers and add them as a row to the df
for inputfilename in inputfilenames:
    inputfilepath = Path(inputfolder / inputfilename)

    # Get identifiers
    inputfile_identifiers = get_identifiers(inputfilepath)

    # Add row to df
    df_identifiers = pd.concat([df_identifiers, inputfile_identifiers], axis=0, ignore_index=True)

# Convert workbook names into workbook root names for consistency across director and SMDE files.
'''
- The director-smde-rootname map has 3 columns: director, smde and root_name.
- We want to be able to directly merge the workbook name (either director or smde) to the root name, so we split the mapping into 2 tables (director + root name, smde + root name) and join them together.
- There are N/As in the smde (workbook name) column of the director-smde-rootname map, which we remove since they cannot be an actual workbook name. Removing NaNs also allows for m:1 validation when merging later on.
'''
director_smde_map = pd.read_excel(director_smde_map_filepath)
director_map = director_smde_map[['director', 'root_name']].rename(columns={'director': 'workbook_name'})
smde_map = director_smde_map[['smde', 'root_name']].rename(columns={'smde': 'workbook_name'})
workbook_name_root_name_map = pd.concat([director_map, smde_map], axis=0).dropna(subset=['workbook_name'])

# Add root name to identifiers by merging on workbook name
df_identifiers = df_identifiers.merge(workbook_name_root_name_map, on='workbook_name', how='inner', validate='m:1')
df_identifiers = df_identifiers.reindex(columns=['inputfilepath', 'inputfilestem', 'region', 'mgmt_type', 'workbook_name', 'root_name', 'fragment_number', 'sheet_name'])

# Save identifiers for future reference
df_identifiers_filepath = Path(outputfolder / 'df_identifiers/df_identifiers.csv')
df_identifiers.to_csv(df_identifiers_filepath, index=False)
print("Saved df_identifiers to:", df_identifiers_filepath)

# ------ PART 2: AGGREGATE FILES ------
print("\n-----------------------------------------------------------")
print("PART 2: AGGREGATE FILES")
print("-----------------------------------------------------------")

'''
Aggregation: 
We will create one file for each workbook root name. In other words, we aggregate across regions, management types, fragments and sheets. 

- Aggregating across regions and fragments: Direct, no complications. We add region and fragment as additional columns when we aggregate.
- Aggregating across management types: If the same variable is present in both director and SMDE datasets, the variable name has been processed to be guaranteed to be the same. The complication left is that a variable may not be present in both datasets, but is a variable we want to collect. In this case, we add a np.NaN column to the dataset without the variable. We also add management type as an additional column when we aggregate.
- Aggregating across sheets: Not immediately obvious how it can be done because it depends on how the sheets differ. There are 3 workbook root names with multiple sheets: Committee Details (1999, 2000, ..., 2021, Current), Profile - Education & Achievements (Education, Achievements) and Profile - Other Activities (Current Other Activities Tab, Historic Current Other Activities Tab). It turns out that we can also use the same method as aggregating across management types (i.e. combine rows and add np.NaN for missing variables). We also add sheet name as an additional column when we aggregate.
- Note: Since workbook name = management type + root name, we also by definition aggregate across workbook names.
'''

# Get the complete set of variables, that includes every unique variable across all files with the same workbook root name
def get_list_variables_root_name(df_identifiers_root_name):
    set_variables_root_name = set()
    list_num_variables = []

    # For each file,
    for index, row in df_identifiers_root_name.iterrows():
        # Get the variable names. 
        set_variables_file = set(pd.read_excel(row['inputfilepath'], nrows=0).columns.astype('str'))
        # Update set of unique variable names.
        set_variables_root_name = set_variables_root_name.union(set_variables_file)
        # Add to the list of number of variables
        list_num_variables.append(len(set_variables_file))
    
    # Convert set to list
    list_variables_root_name = list(set_variables_root_name)
    num_variables_root_name = len(list_variables_root_name)

    # Get % of files that do not contain all variable names.
    count = sum(1 for num_variables_file in list_num_variables if num_variables_file < num_variables_root_name)
    share = round(count / df_identifiers_root_name.shape[0] * 100, 1)

    print('\n--- List of variables: ---')
    print("List of all variable names:", list_variables_root_name)
    print(f"% of files that do not contain all variable names: {share}")

    return list_variables_root_name, num_variables_root_name

# Get list of unique workbook root names
root_names = df_identifiers['root_name'].unique().tolist()

# Drop big files for now
for name in ['Board Summary', 'Committee Details', 'Company Announcements', 'Company Details', 'Company Network', 'Compensation', 'Details Mapping File', 'Network']:
    root_names.remove(name)
print('Root names covered:', root_names)

# Main loop
# Get a combined df for each workbook root name
for index, root_name in enumerate(root_names):
    print(f"Root Name {index}: {root_name}")

    # Get all files that should be aggregated to the workbook root name
    df_identifiers_root_name = df_identifiers[df_identifiers['root_name'] == root_name]

    # Get the complete set of variables, that includes every unique variable across all files with the same workbook root name
    list_variables_root_name, num_variables_root_name = get_list_variables_root_name(df_identifiers_root_name)
    
    # Initialize df, which combines all files with the same workbook root name
    df = pd.DataFrame(columns=list_variables_root_name)

    # Process each file so that it has the same set of columns
    print('\n--- Combining files with the same root name: ---')
    for index, row in df_identifiers_root_name.iterrows():
        inputfilepath, inputfilestem, region, mgmt_type, workbook_name, root_name, fragment_number, sheet_name = row

        # Read in file
        df_file = pd.read_excel(inputfilepath)
        df_file_cols = df_file.columns.astype('str')

        # Add missing columns, if there are any
        if len(df_file_cols) < num_variables_root_name:
            missing_cols = list(set(list_variables_root_name) - set(df_file_cols))
            df_file[missing_cols] = np.NaN
            print(f"{inputfilestem} is missing the columns: {missing_cols}")

        # Add in identifiers
        df_file[['inputfilestem', 'region', 'mgmt_type', 'workbook_name', 'fragment_number', 'sheet_name']] = inputfilestem, region, mgmt_type, workbook_name, fragment_number, sheet_name

        # Add to combined df
        df = pd.concat([df, df_file], axis=0)
    
    # Convert 'n.a' to np.NaN
    df = df.replace('n.a', np.NaN)

    # Save combined df
    outputfilename = root_name + '.csv'
    df_filepath = Path(outputfolder / outputfilename)
    df.to_csv(df_filepath, index=False)
    print("Saved combined df to:", df_filepath)
    print("\n------------")

print("Done!")
