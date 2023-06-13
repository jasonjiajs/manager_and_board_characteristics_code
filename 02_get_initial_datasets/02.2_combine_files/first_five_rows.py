import pandas as pd, numpy as np
from pathlib import Path
import os, sys, glob, re
from itertools import compress

input_folder = Path(sys.argv[1])
output_folder = Path(sys.argv[2])

# Get a list of all Excel files in the input folder
input_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx') or f.endswith('.xls')]

# Iterate through each Excel file
for index, file_name in enumerate(input_files):
    # Read the Excel file and extract the first 5 rows
    first_5_rows = pd.read_excel(os.path.join(input_folder, file_name), nrows=5)
    
    # Create the output file path
    output_file_path = os.path.join(output_folder, file_name)
    
    # Save the first 5 rows to a new Excel file
    first_5_rows.to_excel(output_file_path, index=False)
    
    print(f"File {index}: Saved the first 5 rows of '{file_name}'")

print("Done!")