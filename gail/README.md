####"age"
Age of the patient values:

    35 - 85

####"menarch_age"
Age at Menarch

    0: Age 14 and up, or Unknown
    1: 12 - 13
    2: 7 - 11

####"live_birth_age"
Patient age at first live birth

    0: Less than 20 or Unknown
    1: 20 - 24
    2: 25 - 29, or No Birth
    3: 30 - 55

####"ever_had_biopsy"
Has the patient had a biopsy of the breast?

    0: No
    1: Yes

####"num_biopsy"
Number of biopsies the patient has had

    0: Zero / Never had a biopsy
    1: One / Unknown number of biopsies
    2: More than one biopsy

####"first_deg_relatives"
Number of first degree relatives that have had breast cancer

    0: Zero or Unknown
    1: One Relative
    2: More than one Relative

####"ihyp"
Had at least one breast biopsy with atypical hyperplasia

    0: No
    1: Yes
    99: Unknown

####"race"
Patient's Race

    1:   White, Other
    2:   African American
    3:   Hispanic
        4:   Asian-American                     UNUSED!!!
        5:   American Indian or Alaskan Native  UNUSED!!!
        6:   Unknown                            UNUSED!!! default to #1 for unknown
    7:   Chinese
    8:   Japanese
    9:   Filipino
    10:  Hawaiian
    11:  Other Pacific Islander
    12:  Other Asian-American


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