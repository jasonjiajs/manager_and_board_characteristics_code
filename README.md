# manager_and_board_characteristics_code
Process Boardex files to get a relevant firm-level dataset.

## Manager-level dataset overview
- Level of aggregation: (Year x Company ID)
- We start with a (Year x Company ID x Director) - level dataset, then we aggregate across directors to get a (Year x Company ID) - level dataset.
- Initial identifiers:
  - 'Year'
  - 'CompanyID*'
  - 'Company Name'
  - 'Sector'
  - 'Country'
  - 'ISIN'
  - 'region'
- The following quantitative variables are aggregated by taking the **mean** across directors for each (Year x Company ID) pair. NaN values occur when every director in that (Year x Company ID) pair has a NaN value.
  - Characteristics of Roles Variables: 
    - 'Characteristics of Roles - Director Network Size'
    - 'Characteristics of Roles - Time to Retirement'
    - 'Characteristics of Roles - Time in Role'
    - 'Characteristics of Roles - Time on Board'
    - 'Characteristics of Roles - Time in Company'
  - Director Experience Variables:
    - 'Director Experience - Total Number of Quoted Boards to Date'
    - 'Director Experience - Total Number of Private Boards to Date'
    - 'Director Experience - Total Number of Other Boards to Date'
    - 'Director Experience - Total Number of Quoted Current Boards'
    - 'Director Experience - Total Number of Private Current Boards'
    - 'Director Experience - Total Number of Other Current Boards'
    - 'Director Experience - Avg. Yrs on Other Quoted Boards'
    - 'Director Experience - Age (Yrs)'
    - 'Director Experience - Number of Qualifications'
  - Compensation Ratios Variables: 
    - 'Ratios - Bonus/ (Bonus&Salary)': Ratio of bonus earned to bonus plus salary earned at a selected Annual Report Date
    - 'Ratios - Equity Linked/ Total': Ratio of equity linked compensation earned to total compensation earned at a selected Annual Report Date
    - 'Ratios - Performance/ Total': Ratio of performance based compensation earned to total compensation earned at a selected Annual Report Date
    - 'Ratios - Wealth Delta': Change in the individual’s wealth in the company for each 1% change in the stock price
  - Director Count Totals Variables:
    - 'Director Count Totals - Number of Independent NED with past CFO/FD role'
  - Compensation Variables: 
    - 'Annual Direct Compensation - Salary'
    - 'Annual Direct Compensation - Bonus'
    - 'Annual Direct Compensation - D.C Pension'
    - 'Annual Direct Compensation - Other'
    - 'Annual Direct Compensation - Total Salary+Bonus'
    - 'Annual Direct Compensation - Total Inc. D.C. Pension & Other'
    - 'Annual- Equity Linked Options - Shares'
    - 'Annual- Equity Linked Options - LTIPS(max)'
    - 'Annual- Equity Linked Options - Intrinsic Options (excercisable)'
    - 'Annual- Equity Linked Options - Intrinsic Options (unexercisable)'
    - 'Annual- Equity Linked Options - Estimated Options (unexcercisable)'
    - 'Annual- Equity Linked Options - Estimated Options (exercisable)'
    - 'Annual- Equity Linked Options - Share Price'
    - 'Annual- Equity Linked Options - Total Equity Linked Compensation'
    - 'Total - Total Annual Compensation'
    - 'Accumulated Wealth - Shares'
    - 'Accumulated Wealth - LTIPS(max)'
    - 'Accumulated Wealth - Intrinsic Option'
    - 'Accumulated Wealth - Estimated Option'
    - 'Accumulated Wealth - Liquid Wealth'
    - 'Total Wealth - Total Wealth'
  - Education Variables:
    - 'Bachelors': This is originally an indicator variable that returns 1 if the director has at least one Bachelor's degree, and 0 otherwise. So the mean is the % of directors in a (company, year) that has at least one Bachelors degree.
    - 'Masters'
    - 'MBA'
    - 'PhD'
- Categorical variables are aggregated by taking shares of counts across directors for each (Year x Company ID) pair. For example, the % of male and female directors in a particular (year, company).
  - Variables:
    - 'Director Experience - Gender'
      - Male 
    - 'Director Experience - Nationality Mix'
      - American
      - Canadian
      - British
      - European (excludes British, includes Swiss))
      - Asian
- CEO and CFO-specific variables. In a few cases, there are 2 CEOs or 2 CFOs in one (company, year). For now, we choose the first one that appears in the table.
  - Compensation Ratios Variables:
    - 'CEO - Ratios - Bonus/ (Bonus&Salary)'
    - 'CEO - Ratios - Equity Linked/ Total'
    - 'CEO - Ratios - Performance/ Total'
    - 'CEO - Ratios - Wealth Delta'
    - 'CFO - Ratios - Bonus/ (Bonus&Salary)'	
    - 'CFO - Ratios - Equity Linked/ Total'
    - 'CFO - Ratios - Performance/ Total'
    - 'CFO - Ratios - Wealth Delta'
  - Education Variables:
    - 'CEO - Highest Ranked Degree - Institution Name': Degrees are 'ranked' in the order: PhD > MBA > Masters > Bachelors. The highest ranked degree here is the degree in the highest rank. If there are multiple degrees in the highest rank, the first row is chosen.
    - 'CEO - Highest Ranked Degree - InstitutionID*'	
    - 'CEO - Highest Ranked Degree - Qualification'	
    - 'CEO - Highest Ranked Degree - Country'	
    - 'CFO - Highest Ranked Degree - Institution Name'	
    - 'CFO - Highest Ranked Degree - InstitutionID*'	
    - 'CFO - Highest Ranked Degree - Qualification'	
    - 'CFO - Highest Ranked Degree - Country'
- Firm identifiers are added on by merging on Company ID.
  - Variables: 
    - 'CIK Code'
    - 'Auditors'
    - 'Latest AR'
    - 'Bankers'
    - 'Index'
    - 'Ticker'
    - 'Market Cap'
    - 'HOCountryName'

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
