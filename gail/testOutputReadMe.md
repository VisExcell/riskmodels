## Rows current produced by createGailTestCSV:

[Race, CurrentAge, MenarcheAge, FirstLiveBirthAge, FirsttDegRelatives, NumberOfBiopsies, EverHadBiopsy, iHyp, rHyp, 5YearRiskABS, 5YearRiskAVE, LifetimeRiskABS, LifetimeRiskAVE]

0. Race
1. Current Age
2. Menarche Age
3. First Live Birth Age
4. First Deg Relatives (History of Cancer)
5. NumberOfBiopsy
6. EverHadBiopsy
7. ihyp
8. rhyp
9. 5YearRiskABS
10. 5YearRiskAVE
11. LifetimeRiskABS
12. LifetimeRiskAVE

#### Race

Race is one of:


    1,  # White, other
    2,  # African American
    3,  # Hispanic
        # From BCPTConvert 4, 5 , and 6 are not used?
        # 4,  # Asian-American
        # 5,  # American Indian or Alaskan Native
        # 6,  # Unknown
    7,  # Chinese
    8,  # Japanese
    9,  # Filipino
    10,  # Hawaiian
    11,  # Other Pacific Islander
    12   # Other Asian-American

#### Current Age

Current age is an integer between 35 and 85 (inclusive)

#### Menarche Age

Menarche age is one of the following values:

    2: ages 7 to 11
    1: ages 12 and 13
    0: ages 14 and up (to 39) or Unknown (frequently signified by 99)

#### First Live Birth Age

Patient age at first live birth is one of the following:

    0: less than 20 years old, or *Unknown*
    1: 20 to 24 years old
    2: 25 to 29 years old, or *No Birth*
    3: 30 to 55 years old

#### First Deg Relatives

These are the number of first degree relatives that have had breast cancer

    0: Zero or unknown (99)
    1: One Relative
    2: More than one Relative

#### Number of Biopsies

    0: Zero  (Use this for never had biopsy)
    1: One or Unknown number of biopsies (But have had biopsy below)
    2: more than one biopsy

#### Ever Had Biopsy

    0:  No or Unknown
    1: Yes

#### ihyp

This is the integer value for hyperplasia, but we don't actually use it

From the web site:

    <option value="999">Select</option>
    <option value="99">Unknown</option>
    <option value="1">Yes</option>
    <option value="0">No</option>

#### rhyp

This is the real value for hyperplasia

    1.82: Yes
    0.93: No
    1.00: Unknown or Never Had Biopsy

#### 5YearRiskABS, 5YearRiskAVE, LifetimeRiskABS, LifetimeRiskAVE

These are the 5 year and Lifetime Absolute Risk (for this patient), and Average Risk (for similar patients)
It is reported as a decimal representing %.