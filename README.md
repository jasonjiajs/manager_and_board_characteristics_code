# manager_and_board_characteristics_code
Process Boardex files to get a relevant manager-level and firm-level dataset.

## Manager-level dataset documentation
- Level of aggregation: (Year x Company ID)
- We start with a (Year x Company ID x Director) - level dataset, then we aggregate across directors to get a (Year x Company ID) - level dataset.
- Initial identifiers:
  - ['Year',	'CompanyID*',	'Company Name',	'Sector', 'Country',	'ISIN',	'region']
- Quantitative variables are aggregated by taking the mean across directors for each (Year x Company ID) pair. NaN values occur when every director in that (Year x Company ID) pair has a NaN value
  - Variables: ['Characteristics of Roles - Director Network Size', 'Characteristics of Roles - Time to Retirement', 
                 'Characteristics of Roles - Time in Role', 'Characteristics of Roles - Time on Board', 
                 'Characteristics of Roles - Time in Company',
                 'Director Experience - Total Number of Quoted Boards to Date', 'Director Experience - Total Number of Private Boards to Date', 
                 'Director Experience - Total Number of Other Boards to Date', 
                 'Director Experience - Total Number of Quoted Current Boards', 'Director Experience - Total Number of Private Current Boards', 
                 'Director Experience - Total Number of Other Current Boards', 
                 'Director Experience - Avg. Yrs on Other Quoted Boards', 'Director Experience - Age (Yrs)', 
                 'Director Experience - Number of Qualifications',
                 'Ratios - Bonus/ (Bonus&Salary)','Ratios - Equity Linked/ Total', 
                 'Ratios - Performance/ Total', 'Ratios - %Change from Last Period', 'Ratios - Wealth Delta',
                 'Director Count Totals - Number of Independent NED with past CFO/FD role',
                 'Annual Direct Compensation - Salary',  'Annual Direct Compensation - Bonus', 
                 'Annual Direct Compensation - D.C Pension', 'Annual Direct Compensation - Other', 
                 'Annual Direct Compensation - Total Salary+Bonus', 
                 'Annual Direct Compensation - Total Inc. D.C. Pension & Other',
                 'Annual- Equity Linked Options - Shares', 'Annual- Equity Linked Options - LTIPS(max)',
                 'Annual- Equity Linked Options - Intrinsic Options (excercisable)',  
                 'Annual- Equity Linked Options - Intrinsic Options (unexercisable)',
                 'Annual- Equity Linked Options - Estimated Options (unexcercisable)',
                 'Annual- Equity Linked Options - Estimated Options (exercisable)',
                 'Annual- Equity Linked Options - Share Price', 'Annual- Equity Linked Options - Total Equity Linked Compensation', 
                 'Total - Total Annual Compensation',
                 'Accumulated Wealth - Shares', 'Accumulated Wealth - LTIPS(max)', 
                 'Accumulated Wealth - Intrinsic Option', 'Accumulated Wealth - Estimated Option', 
                 'Accumulated Wealth - Liquid Wealth', 
                 'Total Wealth - Total Wealth']
- Categorical variables are aggregated by taking shares of counts across directors for each (Year x Company ID) pair. For example, the % of male and female directors in a particular (year, company).
  - Variables: [Director Experience - Gender,	Director Experience - Nationality Mix]
- Firm identifiers are added on by merging on Company ID.
  - Variables: ['CIK Code', 'HOAddress2', 'HOAddress1', 'HOAddress4',
               'Auditors', 'Latest AR', 'HO TelNumber', 'Bankers', 'Index', 'Ticker',
               'Market Cap', 'HO FaxNumber',
               'HOAddress5', 'HOCountryName', 'HO URL', 'HOAddress3']   


