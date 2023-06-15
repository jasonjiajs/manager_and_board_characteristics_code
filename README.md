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
| Initial identifiers | Year | year | The applicable year of the company annual report to which the rest of the shown data corresponds (just the year, not year-month) |
| Initial identifiers | CompanyID* | company_id | A unique identifier allocated to each company. |
| Initial identifiers | Company Name | company_name | The full company name or the FT abbreviation in the case of quoted companies. If the company name has changed this will be shown in this field. |
| Initial identifiers | Sector | sector | Sector classification of a company under FTSE International classification (In some cases designated by BoardEx) |
| Initial identifiers | Country | country | The full country name in which the Head Office of the Company is located |
| Initial identifiers | ISIN | isin | An International Securities Identifying Number (ISIN) uniquely identifies a security. |
| Characteristics of Roles | Characteristics of Roles - Director Network Size | director_network_size | The number of individual’s with whom the selected individual overlaps while in employment, other activities, or education roles at the same company, organization, or institution. (I interpret this to be the total number of individuals, which either increases or stays the same from one year to the next.) |
| Characteristics of Roles | Characteristics of Roles - Time to Retirement | time_to_retirement | Time to Retirement for the individual at a selected Annual Report Date assuming a retirement age of 70 (in years) |
| Characteristics of Roles | Characteristics of Roles - Time in Role | time_in_role | Time in Role for the individual at a selected Annual Report Date (in years) |
| Characteristics of Roles | Characteristics of Roles - Time on Board | time_on_board | Time on Board for the individual at a selected Annual Report Date (in years) |
| Characteristics of Roles | Characteristics of Roles - Time in Company | time_in_company | Time in Company for the individual at a selected Annual Report Date (in years) |
| Director Experience | Director Experience - Total Number of Quoted Boards to Date | total_quoted_boards_to_date | The total number of Quoted Boards that an individual has served to the Annual Report Date selected |
| Director Experience | Director Experience - Total Number of Private Boards to Date | total_private_boards_to_date | The total number of Private Boards that an individual has served to the Annual Report Date selected |
| Director Experience | Director Experience - Total Number of Other Boards to Date | total_other_boards_to_date | The total number of Other Boards that an individual has served to the Annual Report Date selected. |
| Director Experience | Director Experience - Total Number of Quoted Current Boards | total_quoted_boards_current | The number of Quoted Boards that an individual serves on at the current Annual Report Date |
| Director Experience | Director Experience - Total Number of Private Current Boards | total_private_boards_current | The number of Private Boards that an individual serves on at the current Annual Report Date |
| Director Experience | Director Experience - Total Number of Other Current Boards | total_other_boards_current | The number of Other Boards that an individual serves on at the current Annual Report Date |
| Director Experience | Director Experience - Avg. Yrs on Other Quoted Boards | avg_years_other_quoted_boards | The Average Time that a Director sits on the Board of Quoted Companies |
| Director Experience | Director Experience - Age (Yrs) | age | Individual’s current age at the Annual Report Date selected |
| Director Experience | Director Experience - Number of Qualifications | num_qualifications | Total number of Educational qualifications (undergraduate and above) for the individual at a selected Annual Report Date |
| Compensation Ratios | Ratios - Bonus/ (Bonus&Salary) | bonus_over_bonus_and_salary | Ratio of bonus earned to bonus plus salary earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Equity Linked/ Total | equity_linked_over_total | Ratio of equity linked compensation earned to total compensation earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Performance/ Total | performance_over_total | Ratio of performance based compensation earned to total compensation earned at a selected Annual Report Date |
| Compensation Ratios | Ratios - Wealth Delta | wealth_delta | Change in the individual’s wealth in the company for each 1% change in the stock price |
| Director Count Totals | Director Count Totals - Number of Independent NED with past CFO/FD role | num_ind_ned_w_past_cfo_fd_role | Number of independent Non-Executive Directors with past Chief Financial Officer or Financial Director experience at the Annual Report Date selected. |
| Compensation | Annual Direct Compensation - Salary | annual_dir_comp_salary | Base annual pay at the Annual Report Date selected (in '000s) |
| Compensation | Annual Direct Compensation - Bonus | annual_dir_comp_bonus | An annual payment made in addition to salary at the Annual Report Date selected (in '000s) |
| Compensation | Annual Direct Compensation - D.C Pension | annual_dir_comp_dc_pension | Employer’s contribution towards the individual’s direct compensation pension or retirement plan at the Annual Report Date selected (in '000s) |
| Compensation | Annual Direct Compensation - Other | annual_dir_comp_other | Other annual ad hoc cash payments such as relocation costs and fringe benefits at the Annual Report Date selected (in '000s) |
| Compensation | Annual Direct Compensation - Total Salary+Bonus | annual_dir_comp_salary_and_bonus | Total salary plus bonus compensation at the Annual Report Date selected (in '000s) |
| Compensation | Annual Direct Compensation - Total Inc. D.C. Pension & Other | annual_dir_comp_total | Total direct compensation at the Annual Report Date selected (in '000s) |
| Compensation | Annual- Equity Linked Options - Shares | annual_eq_opt_shares | Value of shares held at the end of the report for the individual. These are valued at the closing stock price of the Annual Report Date selected. (in '000s) |
| Compensation | Annual- Equity Linked Options - LTIPS(max) | annual_eq_opt_ltips | Maximum potential value of shares held at the end of the report for the individual when exercised. (in '000s) |
| Compensation | Annual- Equity Linked Options - Intrinsic Options (excercisable) | annual_eq_opt_intrinsic_exer | The valuation of Exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. This shows by how much options awarded are in the money. This is equal to the gap between the Exercise Price of the Options and the stock price multiplied by the number of options. (in '000s) |
| Compensation | Annual- Equity Linked Options - Intrinsic Options (unexercisable) | annual_eq_opt_intrinsic_unexer | The valuation of Un-exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. This shows by how much options awarded are in the money. This is equal to the gap between the Exercise Price of the Options and the stock price multiplied by the number of options. (in '000s) |
| Compensation | Annual- Equity Linked Options - Estimated Options (exercisable) | annual_eq_opt_est_exer | A valuation of Exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. Valuation uses a Generalized Black - Scholes option pricing model using the following variables: - Volatility is measured using 100 days of historic stock prices - Risk free rate is measured using the following: o UK = 6 months Libor rate, Europe = EURIBOR, US = 10 year T-Bill, otherwise = 6.5% It is assumed that exercise is on expiry date whether known or assumed. (in '000s) |
| Compensation | Annual- Equity Linked Options - Estimated Options (unexcercisable) | annual_eq_opt_est_unexer | A valuation of Un-exercisable Options awarded in the period. These are valued at the closing stock price of the Annual Report Date selected. Valuation uses a Generalized Black - Scholes option pricing model using the following variables: - Volatility is measured using 100 days of historic stock prices - Risk free rate is measured using the following: o UK = 6 months Libor rate, Europe = EURIBOR, US = 10 year T-Bill, otherwise = 6.5% It is assumed that exercise is on expiry date whether known or assumed. (in '000s) |
| Compensation | Annual- Equity Linked Options - Share Price | annual_eq_opt_share_price | The closing stock price as of the Annual Report Date selected |
| Compensation | Annual- Equity Linked Options - Total Equity Linked Compensation | annual_eq_opt_total_comp | (in '000s) |
| Compensation | Total - Total Annual Compensation | total_annual_comp | Total direct compensation plus total equity linked compensation for the period (in '000s) |
| Compensation | Accumulated Wealth - Shares | acc_wealth_shares | Value of shares held at the end of the report for the individual. These are valued at the closing stock price of the Annual Report Date selected. (in '000s) |
| Compensation | Accumulated Wealth - LTIPS(max) | acc_wealth_ltips | Maximum potential value of shares held at the end of the report for the individual when exercised. (in '000s) |
| Compensation | Accumulated Wealth - Intrinsic Option | acc_wealth_intrinsic_opt | A valuation of Options held at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected. This shows by how much options awarded are in the money. This is equal to the gap between the Exercise Price of the Options and the stock price multiplied by the number of options. (in '000s) |
| Compensation | Accumulated Wealth - Estimated Option | acc_wealth_est_opt | A valuation of Options held at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected. Valuation uses a Generalized Black - Scholes option pricing model using the following variables: - Volatility is measured using 100 days of historic stock prices - Risk free rate is measured using the following: o UK = 6 months Libor rate, Europe = EURIBOR, US = 10 year T-Bill, otherwise = 6.5% It is assumed that exercise is on expiry date whether known or assumed. (in '000s) |
| Compensation | Accumulated Wealth - Liquid Wealth | acc_wealth_liquid_wealth | A valuation of Liquid Wealth at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected (in '000s) |
| Compensation | Total Wealth - Total Wealth | total_wealth | A valuation of Total Wealth at the end of the period for the individual. These are valued at the closing stock price of the Annual Report Date selected (in '000s) |
| Education | Bachelors | bachelors | This is originally an indicator variable that returns 1 if the director has at least one Bachelors degree, and 0 otherwise. So the mean is the % of directors in a (company, year) that has at least one Bachelors degree. |
| Education | Masters | masters |  |
| Education | MBA | mba |  |
| Education | PhD | phd |  |
| Director Experience - Gender | Male  | share_males |  |
| Director Experience - Nationality Mix | Most Common Nationality | most_common_nationality | Most common nationality of directors in a (company, year) |
| Director Experience - Nationality Mix | American | share_american |  % of directors in a (company, year) who are of American nationality |
| Director Experience - Nationality Mix | Canadian | share_canadian |  |
| Director Experience - Nationality Mix | British | share_british |  |
| Director Experience - Nationality Mix | European | share_european | Excludes British, includes Swiss |
| Director Experience - Nationality Mix | Asian | share_asian |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Bonus/ (Bonus&Salary) | ceo_bonus_over_bonus_and_salary |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Equity Linked/ Total | ceo_equity_linked_over_total |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Performance/ Total | ceo_performance_over_total |  |
| CEO/CFO - Compensation Ratios | CEO - Ratios - Wealth Delta | ceo_wealth_delta |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - Institution Name | ceo_degree_institution_name |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - InstitutionID* | ceo_degree_institution_id |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - Qualification | ceo_degree_qualification |  |
| CEO/CFO - Education | CEO - Highest Ranked Degree - Country | ceo_degree_country | Degrees are ranked in the order: PhD > MBA > Masters > Bachelors. The highest ranked degree here is the degree in the highest rank. If there are multiple degrees in the highest rank, the first row is chosen. |
| CEO/CFO - Characteristics of Roles | CEO - Characteristics of Roles - Time in Role | ceo_time_in_role |  |
| CEO/CFO - Characteristics of Roles | CEO - Characteristics of Roles - Time on Board | ceo_time_on_board |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Bonus/ (Bonus&Salary) | cfo_bonus_over_bonus_and_salary |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Equity Linked/ Total | cfo_equity_linked_over_total |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Performance/ Total | cfo_performance_over_total |  |
| CEO/CFO - Compensation Ratios | CFO - Ratios - Wealth Delta | cfo_wealth_delta |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - Institution Name | cfo_degree_institution_name |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - InstitutionID* | cfo_degree_institution_id |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - Qualification | cfo_degree_qualification |  |
| CEO/CFO - Education | CFO - Highest Ranked Degree - Country | cfo_degree_country |  |
| CEO/CFO - Characteristics of Roles | CFO - Characteristics of Roles - Time in Role | cfo_time_in_role |  |
| CEO/CFO - Characteristics of Roles | CFO - Characteristics of Roles - Time on Board | cfo_time_on_board |  |
| Firm identifiers | CIK Code | cik_code | The CIK Code used within SEC filings for American companies - relevant only for companies incorporated within the U.S. and who are required to make a filing |
| Firm identifiers | Auditors | auditors | Organization name that provides audit services to the company |
| Firm identifiers | Latest AR | latest_ar | Latest Annual Report date (in month-year) |
| Firm identifiers | Bankers | bankers | Organization name that provides financial services to the company |
| Firm identifiers | Index | index | Index classification(s) of a company according to FT index classifications |
| Firm identifiers | Ticker | ticker | Shorthand code used to uniquely identify shares of a publicly-traded corporation on a particular stock market. |
| Firm identifiers | Market Cap | market_cap | The total value of a company's securities at Current prices as quoted on a stock exchange. Market capitalization is calculated by multiplying the total number of shares by the market price. |
| Firm identifiers | HOCountryName | ho_country_name | The full country name the Head Office of the Company is located in. |


## Folder structure
- This repo contains the code and documentation for the Manager and Board Characteristics project. It is either saved under the folder `code` or `manager_and_board_characteristics_code`. The other folders are `data` and `output`. The full version of both folders is available in Mercury, and a subset is available in Dropbox.
- `manager_and_board_characteristics`
  - `code`
  - `data`
  - `output` 

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

### Institution ID to Institution Name Crosswalk
- 

### BoardEx variables documentation
- Explanation of variables taken from `BoardEx Core Reports Data Dictionary 102020 (002).pdf`, which seems to be no longer available on WRDS.
- Current version on WRDS: [BoardEx WRDS Data Dictionary](https://wrds-www.wharton.upenn.edu/documents/798/BoardEx_WRDS_Data_Dictionary_102020.pdf) (login required)

### Saving this .md file as a .docx
- [Link to converter](https://cloudconvert.com/md-to-docx) 
