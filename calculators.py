from flask import Flask, jsonify, request
from flask import abort, render_template
from flask_bootstrap import Bootstrap
from gail import gail, gail_api
import numpy as np
from RiskAssessment import BasicRiskAssessment as assessment


app = Flask(__name__)
Bootstrap(app)


def get_calculator(calculator_name):
    if calculator_name.lower() == "gail":
        return gail_api.GailAPI()
    return None

@app.route('/')
def index():
    return "VisExcell Calculators"

@app.route('/api/v2.0/<calculator>', methods=['POST'])
def doGailCalcv2(calculator):
    calc = get_calculator(calculator)
    if calc is None:
        abort(501)  # Not Implemented
    if not request.json: # TODO add more validation
        abort(400)
    else:
        # gailapi = gail_api.GailAPI()
        calculation = calc.run(request.json)
        if calculation["code"] != 200:
            # abort(calculation["code"])
            # print "Errors were found in input!"
            return jsonify(calculation)
        else:
            return jsonify(calculation)

@app.route('/api/v2.0/<calculator>/json', methods=['GET'])
def getFieldDescrptionsJson(calculator):
    calc = get_calculator(calculator)
    if calc is None:
        abort(501)  # Not Implemented
    # gailapi = gail_api.GailAPI()
    return jsonify(calc.get_input_fields_json())


@app.route('/api/v2.0/<calculator>', methods=['GET'])
def getFieldDescrptions(calculator):
    calc = get_calculator(calculator)
    if calc is None:
        abort(501)  # Not Implemented
    # gailapi = gail_api.GailAPI()
    return render_template("api_doc.html", name=calc.get_name(), version="2.0", apidef=calc.get_input_fields_json())


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
