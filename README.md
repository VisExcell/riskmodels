# riskmodels
Python risk models

'master' is autodeployed to Heroku

## GAIL model
This model was ported from the C# code provided by NCI
[API Documentation](gail/README.md) 

###API Info
API endpoint: /api/v1.0/gail

POST JSON to perform calculation
make sure to set the HTTP header:

_Content-Type: application/json_

###Input JSON:

    {
      "age":48,
      "menarch_age":2,
      "live_birth_age":3,
      "ever_had_biopsy":1,
      "num_biopsy":2,
      "first_deg_relatives":2,
      "ihyp":1,
      "race":1
    }

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

###Output JSON

    {
      "date": "2016-06-10",
      "results": {
        "five_year_abs": 0.058523657523393072,
        "five_year_ave": 0.011606210299941746,
        "lifetime_abs": 0.5743854504918563,
        "lifetime_ave": 0.1148439582786286
      }
    }

Currently this model only supports a basic output format.

####"date"
Date that the calculation was performed in the format YYYY-MM-DD

####"results"
there are four results produced. All values are in decimal format (i.e. 0.0585... for a 5.8% value)

*five_year_abs* - This is the 5 year risk value for the specified patient.

*five_year_ave* - This is the 5 year risk value for an average patient of the same age/race.

*lifetime_abs* - This is the lifetime risk value for the specified patient. (This is calculated with a projection age of 90)

*lifetime_ave* - This is the lifetime risk value for an average patient of the same age/race. (This is calculated with a projection age of 90)
