# riskmodels
Python risk models

## GAIL model
This model was ported from the C# code provided by NCI

Inputs to this model:

- age [20:25), [25:30), [30:35) .... [70:74), [75:80), [80:85), [85:90)

- race
	1. White, Other
	2. African American
	3. Hispanic
	4. Asian-American
	5. American Indian or Alaskan Native
	6. Unknown

- sub-race (Need to verify numbers for these)
	7. Chinese
	8. Japanese
	9. Filipino
	10. Hawaiian
	11. Other Pacific Islander
	12. Other Asian-American

- age at menarche
	- Unknown
	- 7 - 11
	- 12 - 13
	- >= 14

- Age at first live birth
	- Unknown
	- No Births
	- < 20
	- 20 - 24
	- 25 - 29
	- >= 30

- Relatives with breast cancer (1st deg relatives?)
	- Unknown
	- 0
	- 1
	- > 1

- Ever had a biopsy?
	- Unknown
	- Yes
	- No

- How many Biopsies?
	- 1
	- > 1

- At least one biopsy with atypical hyperplasia?
	- Unknown
	- No
	- Yes