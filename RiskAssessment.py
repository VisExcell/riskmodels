import datetime
import numpy as np
"""
Class to define a 'RiskAssessment' from FHIR.
Currently only produces JSON.
{
    "date": date assesment was made in ISO format yyyy-mm-dd,
    "results": {
                    "five_year_abs": Five year Absolute Risk for this patient as decimal
                    "five_year_ave": Five year Risk for an average patient
                    "lifetime_abs": Lifetime Absolute Risk for this patient as decimal
                    "lifetime_ave": Lifetime Risk for an average patient
    }
}
"""


class BasicRiskAssessment:
    def __init__(self):
        self.resourceType = "RiskAssessment"
        #self.date = datetime.datetime.now().isoformat()
        self.date = datetime.date.today().isoformat()
        self.fiveyearABS = np.float64(-1)
        self.fiveyearAVE = np.float64(-1)
        self.lifetimeABS = np.float64(-1)
        self.lifetimeAVE = np.float64(-1)

    def setRiskScores(self, fiveABS, fiveAVE, lifeABS, lifeAVE):
        self.fiveyearABS = fiveABS
        self.fiveyearAVE = fiveAVE
        self.lifetimeABS = lifeABS
        self.lifetimeAVE = lifeAVE

    def getJson(self):
        return {"date":self.date,
                "results": {
                    "five_year_abs": self.fiveyearABS,
                    "five_year_ave": self.fiveyearAVE,
                    "lifetime_abs": self.lifetimeABS,
                    "lifetime_ave": self.lifetimeAVE
                }}