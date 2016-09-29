from flask import Flask, jsonify, request
from flask import abort
from gail import gail
import numpy as np
import datetime
from RiskAssessment import BasicRiskAssessment as assessment

app = Flask(__name__)


@app.route('/')
def index():
    return "VisExcell Calculators"

@app.route('/api/v1.0/gail', methods=['POST'])
def doGailCalc():
    """
    {
     "age":48,
     "num_biopsy":2,
     "menarch_age":2,
     "live_birth_age":3,
     "ever_had_biopsy":1,
     "first_deg_relatives":2,
     "ihyp":1,
     "race":1
    }
    """
    if not request.json: # TODO add more validation
        abort(400)
    else:
        # print request.json
        calc = gail.GailRiskCalculator()
        calc.Initialize()  # TODO: look into moving this into the instantion of the object

        # TODO: move the rhyp and age indicator logic into the gail calculator, all it's logic should live in there.
        age_indicator = 0 if request.json['age'] < 50 else 1
        rhyp = np.float64(1.0)
        if request.json['ever_had_biopsy'] == 1:
            if request.json['ihyp'] == 0:
                rhyp = np.float64(0.93)
            elif request.json['ihyp'] == 1:
                rhyp = np.float(1.82)

        fiveYearABS = calc.CalculateAbsoluteRisk(request.json['age'],
                                                 request.json['age'] + 5,
                                                 age_indicator,
                                                 request.json['num_biopsy'],
                                                 request.json['menarch_age'],
                                                 request.json['live_birth_age'],
                                                 request.json['ever_had_biopsy'],
                                                 request.json['first_deg_relatives'],
                                                 request.json['ihyp'],
                                                 rhyp,
                                                 request.json['race'])
        fiveYearAVE = calc.CalculateAeverageRisk(request.json['age'],
                                                 request.json['age'] + 5,
                                                 age_indicator,
                                                 request.json['num_biopsy'],
                                                 request.json['menarch_age'],
                                                 request.json['live_birth_age'],
                                                 request.json['ever_had_biopsy'],
                                                 request.json['first_deg_relatives'],
                                                 request.json['ihyp'],
                                                 rhyp,
                                                 request.json['race'])
        lifetimeABS = calc.CalculateAbsoluteRisk(request.json['age'],
                                                 90,
                                                 age_indicator,
                                                 request.json['num_biopsy'],
                                                 request.json['menarch_age'],
                                                 request.json['live_birth_age'],
                                                 request.json['ever_had_biopsy'],
                                                 request.json['first_deg_relatives'],
                                                 request.json['ihyp'],
                                                 rhyp,
                                                 request.json['race'])
        lifetimeAve = calc.CalculateAeverageRisk(request.json['age'],
                                                 90,
                                                 age_indicator,
                                                 request.json['num_biopsy'],
                                                 request.json['menarch_age'],
                                                 request.json['live_birth_age'],
                                                 request.json['ever_had_biopsy'],
                                                 request.json['first_deg_relatives'],
                                                 request.json['ihyp'],
                                                 rhyp,
                                                 request.json['race'])

        results = assessment()
        results.setRiskScores(fiveYearABS,fiveYearAVE,lifetimeABS,lifetimeAve)

        return jsonify(results.getJson())


if __name__ == "__main__":
    app.run(debug=False)
