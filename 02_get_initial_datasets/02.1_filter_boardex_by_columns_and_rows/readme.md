# filter_boardex_by_columns_and_rows

This step filters out relevant columns and rows in Boardex using `filter_boardex_by_columns_and_rows.py` and `filter_boardex_by_columns_and_rows.sh`.

- Columns: only keep columns indicated in `List_of_Variables_for_Boardex_and_Execucomp_[ddmmyy].xlsx`. This file is contains the desired corresponding file/workbook names, sheet names, and columns, so that we can get the correct output.
- Rows: only keep rows where company ID is in a provided list of company IDs, `companyids_to_search_for.xlsx`. If the file does not contain company IDs, just keep the file.

Notes:

- Input: Raw Boardex files, list of company IDs, list of columns
- Output: Filtered Boardex files in an separate folder, out files in `/out`.
- Since there are many files, we speed up the processing time using arrays. The code is set up to split the Boardex files into 64 groups, and each of the 64 CPUs in the array will process 1 group.
- There are many types of workbooks and edge cases. A lot of complexities are covered by the table in `List_of_Variables_for_Boardex_and_Execucomp_[ddmmyy].xlsx`.
- Area for Improvement: Divide the files across N CPUs more equally. Currently, say if there are 199 files and 100 CPUs, CPU 1 to 99 will get 1 file, while CPU 100 will get 100 files. A much better solution will be to give CPU 1 to 99 2 files, and CPU 100 1 file.
