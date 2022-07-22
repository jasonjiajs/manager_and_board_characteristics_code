import pandas as pd
from pathlib import Path

'''
Idea:

- go through all the files
- Get everything except the number part (the "big file type"), and remove duplicates to get a list of unique big file types. E.g. Everything before the second '-' is the big file type, and everything after is the file number_filtered.
- Start with one "big file type"
    - Count the number of fragments (# of numbers), and add the fragments to a list
    - If = 1, just copy over. [new]: [old]
    - If > 1, do a function to combine and copy across all elements of the list
- Big function (big file type, list of all elements):
    - new fragment count = 1
    - Iterate through the fragments in the list
    - Get the first fragment, load into combined_df, and get number of rows
    - Get the next df, load into a df, and get number of rows.
    - Add to cumulative numrows. 
        - If < 1,000,000, ok. Append to combined_df
        - If >= 1,000,000, reject. Save previous df with suffix _combined_[new fragment count]. Replace with new df. Add old frag number to list, e.g. [old 1 3] -> [old 1 3 5]
        - But we also want to know what old fragments the new fragment possess. So we need to copy the e.g. [new 1] : [old 1 3 5] into a df of sorts.
        - Reset cumulative count.
        - new fragment count + 1
    - There will always be rows unsaved after this loop, so save the final combined_df.
- Then go to next file type.
'''
