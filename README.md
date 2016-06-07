# riskmodels
Python risk models

## GAIL model
This model was ported from the C# code provided by NCI

Inputs to this model:

- age [20:25), [25:30), [30:35) .... [70:74), [75:80), [80:85), [85:90)

- race
    - 1 White, Other
    - 2 African American
    - 3 Hispanic
    - 4 Asian-American _- not used due to sub types_
    - 5 American Indian or Alaskan Native _- not used due to sub types_
    - 6 Unknown _- not used, default to #1_

- sub-race
    - 7 Chinese
    - 8 Japanese
    - 9 Filipino
    - 10 Hawaiian
    - 11 Other Pacific Islander
    - 12 Other Asian-American

- age at menarche
    - Unknown
    - 7 - 11
    - 12 - 13
    - 14+

- Age at first live birth
    - Unknown
    - No Births
    - < 20
    - 20 - 24
    - 25 - 29
    - 30+

- Relatives with breast cancer (1st deg relatives?)
    - Unknown
    - 0
    - 1
    - 2+

- Ever had a biopsy?
    - Unknown
    - Yes
    - No

- How many Biopsies?
    - 1
    - 2+

- At least one biopsy with atypical hyperplasia?
    - Unknown
    - No
    - Yes

---
Notes about indicators from withing original C# Calculate Risk:

	/* AgeIndicator: age ge 50 ind  0=[20, 50) */
	/*                    1=[50, 85) */
	/* MenarcheAge: age menarchy   0=[14, 39] U 99 (unknown) */
	/*                    1=[12, 14) */
	/*                    2=[ 7, 12) */
	/* NumberOfBiopsy: # biopsy       0=0 or (99 and ever had biopsy=99 */
	/*                    1=1 or (99 and ever had biopsy=1 y */
	/*                    2=[ 2, 30] */
	/* FirstLiveBirthAge: age 1st live   0=<20, 99 (unknown) */
	/*                    1=[20, 25) */
	/*                    2=[25, 30) U 0 */
	/*                    3=[30, 55] */
	/* FirstDegRelatives: 1st degree rel 0=0, 99 (unknown) */
	/*                    1=1 */
	/*                    2=[2, 31] */