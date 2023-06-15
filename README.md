# manager_and_board_characteristics_code
Process Boardex files to get a relevant firm-level dataset.

## Manager-level dataset overview
- Level of aggregation: (Year x Company ID)
- We start with a (Year x Company ID x Director) - level dataset, then we aggregate across directors to get a (Year x Company ID) - level dataset.

### Categories of variables
- Initial identifiers: variables that identify the observation, specifically year and company.
- Quantitative variables in the following categories are aggregated by taking the **mean** across directors for each (Year x Company ID) pair. NaN values occur when every director in that (Year x Company ID) pair has a NaN value.
  - Characteristics of Roles
  - Director Experience
  - Compensation Ratios
  - Director Count Totals
  - Compensation
  - Education
- Categorical variables in the following categories are aggregated by taking shares of counts across directors for each (Year x Company ID) pair. For example, the % of male and female directors in a particular (year, company).
  - Director Experience - Gender
  - Director Experience - Nationality Mix
- CEO and CFO-specific variables in the following categories answer questions like 'What's the compensation of the CEO/CFO?'. In a few cases, there are 2 CEOs or 2 CFOs in one (company, year). For now, we choose the first one that appears in the table.
  - CEO/CFO - Compensation Ratios
  - CEO/CFO - Education
- Firm identifiers: variables that provide details on the company. They are added on by merging on Company ID.

### Full list of variables

| Category | Original Variable Name | Stata Variable Name | Explanation |
|---|---|---|---|
| Initial identifiers | Year | Year |  |
| Initial identifiers | CompanyID* | CompanyID* |  |
| Initial identifiers | Company Name | Company Name |  |
| Initial identifiers | Sector | Sector |  |
| Initial identifiers | Country | Country |  |
| Initial identifiers | ISIN | ISIN |  |
| Characteristics of Roles | Characteristics of Roles - Director Network Size |  |  |
| Characteristics of Roles | Characteristics of Roles - Time to Retirement |  |  |
| Characteristics of Roles | Characteristics of Roles - Time in Role |  |  |
| Characteristics of Roles | Characteristics of Roles - Time on Board |  |  |
| Characteristics of Roles | Characteristics of Roles - Time in Company |  |  |
| Director Experience | Director Experience - Total Number of Quoted Boards to Date |  |  |
| Director Experience | Director Experience - Total Number of Private Boards to Date |  |  |
| Director Experience | Director Experience - Total Number of Other Boards to Date |  |  |
| Director Experience | Director Experience - Total Number of Quoted Current Boards |  |  |
| Director Experience | Director Experience - Total Number of Private Current Boards |  |  |
| Director Experience | Director Experience - Total Number of Other Current Boards |  |  |
| Director Experience | Director Experience - Avg. Yrs on Other Quoted Boards |  |  |
| Director Experience | Director Experience - Age (Yrs) |  |  |
| Director Experience | Director Experience - Number of Qualifications |  |  |
| Compensation Ratios | Ratios - Bonus/ (Bonus&Salary) |  | Ratio of bonus earned to bonus plus salary earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Equity Linked/ Total |  | Ratio of equity linked compensation earned to total compensation earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Performance/ Total |  | Ratio of performance based compensation earned to total compensation earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Wealth Delta |  | Change in the individual’s wealth in the company for each 1% change in the stock price |
| Director Count Totals | Director Count Totals - Number of Independent NED with past CFO/FD role |  |  |
| Compensation | Annual Direct Compensation - Salary |  |  |
| Compensation | Annual Direct Compensation - Bonus |  |  |
| Compensation | Annual Direct Compensation - D.C Pension |  |  |
| Compensation | Annual Direct Compensation - Other |  |  |
| Compensation | Annual Direct Compensation - Total Salary+Bonus |  |  |
| Compensation | Annual Direct Compensation - Total Inc. D.C. Pension & Other |  |  |
| Compensation | Annual- Equity Linked Options - Shares |  |  |
| Compensation | Annual- Equity Linked Options - LTIPS(max) |  |  |
| Compensation | Annual- Equity Linked Options - Intrinsic Options (excercisable) |  |  |
| Compensation | Annual- Equity Linked Options - Intrinsic Options (unexercisable) |  |  |
| Compensation | Annual- Equity Linked Options - Estimated Options (unexcercisable) |  |  |
| Compensation | Annual- Equity Linked Options - Estimated Options (exercisable) |  |  |
| Compensation | Annual- Equity Linked Options - Share Price |  |  |
| Compensation | Annual- Equity Linked Options - Total Equity Linked Compensation |  |  |
| Compensation | Total - Total Annual Compensation |  |  |
| Compensation | Accumulated Wealth - Shares |  |  |
| Compensation | Accumulated Wealth - LTIPS(max) |  |  |
| Compensation | Accumulated Wealth - Intrinsic Option |  |  |
| Compensation | Accumulated Wealth - Estimated Option |  |  |
| Compensation | Accumulated Wealth - Liquid Wealth |  |  |
| Compensation | Total Wealth - Total Wealth |  |  |
| Education | Bachelors |  | This is originally an indicator variable that returns 1 if the director has at least one Bachelors degree, and 0 otherwise. So the mean is the % of directors in a (company, year) that has at least one Bachelors degree. |
| Education | Masters |  |  |
| Education | MBA |  |  |
| Education | PhD |  |  |
| Director Experience - Gender | Male  |  |  |
| Director Experience - Nationality Mix | American |  |  |
| Director Experience - Nationality Mix | Canadian |  |  |
| Director Experience - Nationality Mix | British |  |  |
| Director Experience - Nationality Mix | European |  | Excludes British, includes Swiss |
| Director Experience - Nationality Mix | Asian |  |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Bonus/ (Bonus&Salary) |  |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Equity Linked/ Total |  |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Performance/ Total |  |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Wealth Delta |  |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Bonus/ (Bonus&Salary) |  |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Equity Linked/ Total |  |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Performance/ Total |  |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Wealth Delta |  |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - Institution Name |  | Degrees are ranked in the order: PhD > MBA > Masters > Bachelors. The highest ranked degree here is the degree in the highest rank. If there are multiple degrees in the highest rank, the first row is chosen. |
| CEO/CFO - Education | CEO - Highest Ranked Degree - InstitutionID* |  |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - Qualification |  |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - Country |  |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - Institution Name |  |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - InstitutionID* |  |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - Qualification |  |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - Country |  |  |
| Firm identifiers | CIK Code |  |  |
| Firm identifiers | Auditors |  |  |
| Firm identifiers | Latest AR |  |  |
| Firm identifiers | Bankers |  |  |
| Firm identifiers | Index |  |  |
| Firm identifiers | Ticker |  |  |
| Firm identifiers | Market Cap |  |  |
| Firm identifiers | HOCountryName |


## Misc

### Additional description for select variables not kept in firm-level dataset
- Compensation Ratios Variables: 
  - 'Ratios - %Change from Last Period': Percentage change of performance to total ratio over the same ratio from the previous annual report year  

### Nationalities
- Countries in Europe: Albania, Andorra, Austria, Belarus, Belgium, Bosnia and Herzegovina, Bulgaria, Croatia, Cyprus, 
Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Republic of Ireland, 
Italy, Kosovo, Latvia, Liechtenstein, Lithuania, Luxembourg, North Macedonia, Malta, Moldova, Monaco, 
Montenegro, Netherlands, Norway, Poland, Portugal, Romania, Russia, San Marino, Serbia, Slovakia, 
Slovenia, Spain, Sweden, Switzerland, Turkey, Ukraine, Vatican City

- Countries in Asia: Afghanistan, Armenia, Azerbaijan, Bahrain, Bangladesh, Bhutan, Brunei, Cambodia, China, East Timor, Georgia, India, Indonesia, Iran,
Iraq, Israel, Japan, Jordan, Kazakhstan, Kuwait, Kyrgyzstan, Laos, Lebanon, Malaysia, The Maldives, Mongolia,
Myanmar (Burma), Nepal, North Korea, Oman, Pakistan, Palestine, The Philippines, Qatar, Saudi Arabia,
Singapore, South Korea, Sri Lanka, Syria, Taiwan, Tajikistan, Thailand, Turkmenistan, United Arab Emirates, Uzbekistan, Vietnam, Yemen

- European nationalities in dataset: 'Austrian', 'Belarusian', 'Belgian', 'Bosnian', 'Bulgarian', 'Croatian', 'Cypriot', 'Czech', 'Danish', 
'Dutch',  'Finnish', 'French', 'German', 'Greek', 'Hungarian', 'Icelander', 'Irish', 'Italian', 
'Luxembourger', 'Maltese', 'Monacan', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 
'Slovak', 'Slovene', 'Spanish', 'Swedish', 'Swiss', 'Turkish', 'Ukrainian'

- Asian nationalities in dataset: 'Armenian', 'Bahraini', 'Burmese', 'Chinese', 'Chinese (Taiwan)', 'Emirian', 'Filipino', 'Georgian', 
'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Israeli', 'Japanese', 'Jordanian', 'Kazakhstani',
'Kuwaiti', 'Malaysian', 'Omani', 'Pakistani', 'Qatari', 'Saudi', 'Singaporean',
'South Korean', 'Sri Lankan', 'Syrian', 'Thai'

### BoardEx variables documentation
- [BoardEx WRDS Data Dictionary](https://wrds-www.wharton.upenn.edu/documents/798/BoardEx_WRDS_Data_Dictionary_102020.pdf) (login required)

### Saving this .md file as a .docx
- [Link to converter](https://cloudconvert.com/md-to-docx)

## Folder structure
- This repo contains the code and documentation for the Manager and Board Characteristics project. It is either saved under the folder `code` or `manager_and_board_characteristics_code`. The other folders are `data` and `output`. The full version of both folders is available in Mercury, and a subset is available in Dropbox.
- `manager_and_board_characteristics`
  - `code`
  - `data`
  - `output` 
