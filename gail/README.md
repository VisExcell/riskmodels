##Patient Age
cancer.gov question 3: 
> "What is the woman's age?
> *This tool only calculates risk for women 35 years of age or older.*"

VE calculator field name: `age`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 99               |
| < 35        | N/A           | 34               |
| 35..85      | 35..85        | 35..85

 - Note: there is a single entry per age for 35..85
 - Note: cancer.org does a JS check on age when selecting. 

##Age at Menarch
cancer.gov question 4: 
> "What was the woman's age at the time of her first menstrual period?"

VE calculator field name: `menarch_age`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 999              |
| Unknown     | 0             | 99               |
| 7 to 11     | 2             | 10               |
| 12 to 13    | 1             | 13               |
| > =14       | 0             | 14               |

##Age at first live brith
cancer.gov question 5:
> What was the woman's age at the time of her first live birth of a child?

VE calculator field name: `live_birth_age`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 999              |
| Unknown     | 0             | 99               |
| No Births   | 2             | 0                |
| < 20        | 0             | 15               |
| 20 to 24    | 1             | 22               |
| 25 to 29    | 2             | 27               |
| > =30       | 3             | 30               |

##Has the patient had a bread biopsy
cancer.gov question 7:
> Has the woman ever had a breast biopsy? 

VE calculator field name: `ever_had_biopsy`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 999              |
| Unknown     | 1             | 99               |
| No          | 0             | 0                |
| Yes         | 1             | 1                |

###How many biopsies
cancer.gov question 7a:
> How many breast biopsies (positive or negative) has the woman had?

VE calculator field name: `num_biopsy`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 999              |
| (Unknown)   | 1             | 99               |
| (Zero)      | 0             | 0                |
| 1           | 1             | 1                |
| > 1         | 2             | 2                |

 - Note: The cancer.org site doesn't have options for 'Unknown' or 'Zero'.
 	- Use (Unknown) if answer to 7 is 'Unknown'
 	- Use (Zero) if answer to 7 is 'No'

###Atypical Hyperplasia?
cancer.org question 7b:
> Has the woman had at least one breast biopsy with atypical hyperplasia? 

VE calculator field name: `ihyp`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 999              |
| Unknown     | 99            | 99               |
| No          | 0             | 0                |
| Yes         | 1             | 1                |

- Use Unknown if answer to 7 is 'Unknown'
- Use Zero if answer to 7 is 'No'

##First Degree relatives with Breast Cancer
cancer.gov question 6:
> How many of the woman's first-degree relatives - mother, sisters, daughters - have had breast cancer?

VE calculator field name: `first_deg_relatives`

| Option Text | VE Calc Value | cancer.gov Value |
| ----------- | ------------- | ---------------- |
| Select      | N/A           | 999              |
| Unknown     | 0             | 99               |
| Zero        | 0             | 0                |
| 1           | 1             | 1                |
| > 1         | 2             | 2                |

##Patient's Race
cancer.gov questions 8 and 8a:
> 8: What is the woman's race/ethnicity?
> 
> 8a: What is the sub race/ethnicity?

VE calculator field name: `race`

| Option Text #8   | Option Text #8a | VE Calc Value | cancer.gov #8 Value | cancer.gov #8a Value |
| --------------   | --------------- | ------------- | ------------------- | -------------------- |
| Select           | Select          | N/A           | 999                 | 999                  |
| White            | 'n/a'           | 1             | 1                   | 99                   |
| African American | 'n/a'           | 2             | 2                   | 99                   |
| Hispanic         | 'n/a'           | 3             | 3                   | 99                   |
| Asian   American | '(select)'      | N/A           | 4                   | 999                  |
| Asian   American | Chinese         | 7             | 4                   | 7                    |
| Asian   American | Japanese        | 8             | 4                   | 8                    |
| Asian   American | Filipino        | 9             | 4                   | 9                    |
| Asian   American | Hawaiian        | 10            | 4                   | 10                   |
| Asian   American | Other Pacific Islander | 11            | 4                   | 11                   |
| Asian   American | Other Asian-American   | 12            | 4                   | 12                   |
| American Indian or Alaskan Native | 'n/a' | 1             | 5                   | 99                   |
| Unknown                           | 'n/a' | 1             | 6                    | 99                   |

- Note: for 'Hispanic' and cancaer.gov gives a pop up saying "Assessments for Hispanic women are subject to greater uncertainty than those for white and African American women. Researchers are conducting additional studies, including studies with minority populations, to gather more data and to increase the accuracy of the tool for women in these populations."
- Note: for 'Unknown' and 'American Indian or Alaskan Native' cancer.gov gives a pop up note "Assessments for American Indian or Alaskan Native women are uncertain and are based on data for **white women**. Researchers are conducting additional studies, including studies with minority populations, to gather more data and to increase the accuracy of the tool for women in these populations." (Emphasis is added by SRM)


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
