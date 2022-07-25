Log of steps taken:
1. First ran filter_output_by_columns.sh / filter_output_by_columns.py
    - Looked at data/output_filtered_by_columns, realised that "Director Profile - Characteristics.xlsx" and "Director Profile - Education & Achievements.xlsx" were missing, because they did not have an ISIN column, and so did not appear in /data/output.
    - So we need to run the filter specifically on the two files above 
2. Then ran filter_output_by_columns_characteristics_educationandachievements.sh / filter_output_by_columns_characteristics_educationandachievements.sh
    - Checked data/output_filtered_by_columns, looks good (?)
