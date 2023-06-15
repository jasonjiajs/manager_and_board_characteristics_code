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
| Initial identifiers | Year | Year | The applicable year of the company annual report to which the rest of the shown data corresponds (just the year, not year-month) |
| Initial identifiers | CompanyID* | CompanyID* | A unique identifier allocated to each company. |
| Initial identifiers | Company Name | Company Name | The full company name or the FT abbreviation in the case of quoted companies. If the company name has changed this will be shown in this field. |
| Initial identifiers | Sector | Sector | Sector classification of a company under FTSE International classification (In some cases designated by BoardEx) |
| Initial identifiers | Country | Country | The full country name in which the Head Office of the Company is located |
| Initial identifiers | ISIN | ISIN | An International Securities Identifying Number (ISIN) uniquely identifies a security. |
| Characteristics of Roles | Characteristics of Roles - Director Network Size |  | The number of individual’s with whom the selected individual overlaps while in employment, other activities, or education roles at the same company, organization, or institution |
| Characteristics of Roles | Characteristics of Roles - Time to Retirement |  | Time to Retirement for the individual at a selected Annual Report Date assuming a retirement age of 70 |
| Characteristics of Roles | Characteristics of Roles - Time in Role |  | Time in Role for the individual at a selected Annual Report Date |
| Characteristics of Roles | Characteristics of Roles - Time on Board |  | Time on Board for the individual at a selected Annual Report Date |
| Characteristics of Roles | Characteristics of Roles - Time in Company |  | Time in Company for the individual at a selected Annual Report Date |
| Director Experience | Director Experience - Total Number of Quoted Boards to Date |  | The total number of Quoted Boards that an individual has served to the Annual Report Date selected |
| Director Experience | Director Experience - Total Number of Private Boards to Date |  | The total number of Private Boards that an individual has served to the Annual Report Date selected |
| Director Experience | Director Experience - Total Number of Other Boards to Date |  | The total number of Other Boards that an individual has served to the Annual Report Date selected. |
| Director Experience | Director Experience - Total Number of Quoted Current Boards |  | The number of Quoted Boards that an individual serves on at the current Annual Report Date |
| Director Experience | Director Experience - Total Number of Private Current Boards |  | The number of Private Boards that an individual serves on at the current Annual Report Date |
| Director Experience | Director Experience - Total Number of Other Current Boards |  | The number of Other Boards that an individual serves on at the current Annual Report Date |
| Director Experience | Director Experience - Avg. Yrs on Other Quoted Boards |  | The Average Time that a Director sits on the Board of Quoted Companies |
| Director Experience | Director Experience - Age (Yrs) |  | Individual’s current age at the Annual Report Date selected |
| Director Experience | Director Experience - Number of Qualifications |  | Total number of Educational qualifications (undergraduate and above) for the individual at a selected Annual Report Date |
| Compensation Ratios | Ratios - Bonus/ (Bonus&Salary) |  | Ratio of bonus earned to bonus plus salary earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Equity Linked/ Total |  | Ratio of equity linked compensation earned to total compensation earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Performance/ Total |  | Ratio of performance based compensation earned to total compensation earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Wealth Delta |  | Change in the individual’s wealth in the company for each 1% change in the stock price |
| Director Count Totals | Director Count Totals - Number of Independent NED with past CFO/FD role |  | Number of independent Non-Executive Directors with past Chief Financial Officer or Financial Director experience at the Annual Report Date selected. |
| Compensation | Annual Direct Compensation - Salary |  | Base annual pay at the Annual Report Date selected |
| Compensation | Annual Direct Compensation - Bonus |  | An annual payment made in addition to salary at the Annual Report Date selected |
| Compensation | Annual Direct Compensation - D.C Pension |  | Employer’s contribution towards the individual’s direct compensation pension or retirement plan at the Annual Report Date selected |
| Compensation | Annual Direct Compensation - Other |  | Other annual ad hoc cash payments such as relocation costs and fringe benefits at the Annual Report Date selected |
| Compensation | Annual Direct Compensation - Total Salary+Bonus |  | Total salary plus bonus compensation at the Annual Report Date selected |
| Compensation | Annual Direct Compensation - Total Inc. D.C. Pension & Other |  | Total direct compensation at the Annual Report Date selected |
| Compensation | Annual- Equity Linked Options - Shares |  | Value of shares held at the end of the report for the individual. These are valued at the closing stock price of the Annual Report Date selected. |
| Compensation | Annual- Equity Linked Options - LTIPS(max) |  | Maximum potential value of shares held at the end of the report for the individual when exercised. |
| Compensation | Annual- Equity Linked Options - Intrinsic Options (excercisable) |  | The valuation of Exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. This shows by how much options awarded are in the money. This is equal to the gap between the Exercise Price of the Options and the stock price multiplied by the number of options. |
| Compensation | Annual- Equity Linked Options - Intrinsic Options (unexercisable) |  | The valuation of Un-exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. This shows by how much options awarded are in the money. This is equal to the gap between the Exercise Price of the Options and the stock price multiplied by the number of options. |
| Compensation | Annual- Equity Linked Options - Estimated Options (exercisable) |  | A valuation of Exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. Valuation uses a Generalized Black - Scholes option pricing model using the following variables: - Volatility is measured using 100 days of historic stock prices - Risk free rate is measured using the following: o UK = 6 months Libor rate, Europe = EURIBOR, US = 10 year T-Bill, otherwise = 6.5% It is assumed that exercise is on expiry date whether known or assumed. |
| Compensation | Annual- Equity Linked Options - Estimated Options (unexcercisable) |  | A valuation of Un-exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. Valuation uses a Generalized Black - Scholes option pricing model using the following variables: - Volatility is measured using 100 days of historic stock prices - Risk free rate is measured using the following: o UK = 6 months Libor rate, Europe = EURIBOR, US = 10 year T-Bill, otherwise = 6.5% It is assumed that exercise is on expiry date whether known or assumed. |
| Compensation | Annual- Equity Linked Options - Share Price |  | The closing stock price as of the Annual Report Date selected |
| Compensation | Annual- Equity Linked Options - Total Equity Linked Compensation |  |  |
| Compensation | Total - Total Annual Compensation |  | Total direct compensation plus total equity linked compensation for the period |
| Compensation | Accumulated Wealth - Shares |  | Value of shares held at the end of the report for the individual. These are valued at the closing stock price of the Annual Report Date selected. |
| Compensation | Accumulated Wealth - LTIPS(max) |  | Maximum potential value of shares held at the end of the report for the individual when exercised. |
| Compensation | Accumulated Wealth - Intrinsic Option |  | A valuation of Options held at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected. This shows by how much options awarded are in the money. This is equal to the gap between the Exercise Price of the Options and the stock price multiplied by the number of options. |
| Compensation | Accumulated Wealth - Estimated Option |  | A valuation of Options held at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected. Valuation uses a Generalized Black - Scholes option pricing model using the following variables: - Volatility is measured using 100 days of historic stock prices - Risk free rate is measured using the following: o UK = 6 months Libor rate, Europe = EURIBOR, US = 10 year T-Bill, otherwise = 6.5% It is assumed that exercise is on expiry date whether known or assumed. |
| Compensation | Accumulated Wealth - Liquid Wealth |  | A valuation of Liquid Wealth at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected |
| Compensation | Total Wealth - Total Wealth |  | A valuation of Total Wealth at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected |
| Education | Bachelors |  | This is originally an indicator variable that returns 1 if the director has at least one Bachelors degree, and 0 otherwise. So the mean is the % of directors in a (company, year) that has at least one Bachelors degree. |
| Education | Masters |  |  |
| Education | MBA |  |  |
| Education | PhD |  |  |
| Director Experience - Gender | Male  |  |  |
| Director Experience - Nationality Mix | American |  |  % of directors in a (company, year) who are of American nationality |
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
- Explanation of variables taken from `BoardEx Core Reports Data Dictionary 102020 (002).pdf`, which seems to be no longer available on WRDS.
- Current version on WRDS: [BoardEx WRDS Data Dictionary](https://wrds-www.wharton.upenn.edu/documents/798/BoardEx_WRDS_Data_Dictionary_102020.pdf) (login required)

### Saving this .md file as a .docx
- [Link to converter](https://cloudconvert.com/md-to-docx)

## Folder structure
- This repo contains the code and documentation for the Manager and Board Characteristics project. It is either saved under the folder `code` or `manager_and_board_characteristics_code`. The other folders are `data` and `output`. The full version of both folders is available in Mercury, and a subset is available in Dropbox.
- `manager_and_board_characteristics`
  - `code`
  - `data`
  - `output` 
