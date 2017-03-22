import gail as gail_calc
from RiskAssessment import BasicRiskAssessment as assessment
import numpy as np
import json

class questionaire_obj:
    def __init__(self, name="", desc="", type="generic"):
        self.name = name
        self.description = desc
        self.type = type

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


class questionaire_enum(questionaire_obj):
    def __init__(self, name="", desc=""):
        questionaire_obj.__init__(self, name, desc, "enum")
        self.options = {}
        self.option_descriptions = {}
        self.option_descriptions = {}

    def add_option(self, value, input_str, desc):
        self.options[input_str] = value
        self.option_descriptions[input_str] = desc





class GailAPI:
    def __init__(self):
        self.fields = {"age": {"description": "Patient Current Age between 35 and 85",
                               "type": "range",
                               "maximum": 85,
                               "minimum": 35},
                       "num_biopsy": {"description": "How many breast biopsies has the patient had?",
                                      "type": "enum",
                                      "values": [0, 1, 2],
                                      "option_descriptions": {"0": "No Breast Biopsies",
                                                              "1": "One, or Unknown number of biopsies",
                                                              "2": "More than one biopsy"}},
                       "menarch_age": {"description": "Patient's age at the time of her first menstrual period?",
                                       "type": "enum",
                                       "values": [0, 1, 2],
                                       "option_descriptions": {"0": "Unknown or greater than 14",
                                                               "1": "12 or 13 years old",
                                                               "2": "Between 7 to 11 years old"}},
                       "live_birth_age": {
                           "description": "Patient's age at the time of her first live birth of a child?",
                           "type": "enum",
                           "values": [0, 1, 2, 3],
                           "option_descriptions": {"0": "Unknown or less than 20",
                                                   "1": "20 to 24 years old",
                                                   "2": "No Births or 25 to 29 years old",
                                                   "3": "30 years old or older"}},
                       "ever_had_biopsy": {"description": "Has the patient ever had a breast biopsy?",
                                           "type": "enum",
                                           "values": [0, 1],
                                           "option_descriptions": {"0": "No",
                                                                   "1": "Unknown or Yes"}},
                       "first_deg_relatives": {
                           "description": "How many of the patient's first-degree relatives - mother, sisters, daughters - have had breast cancer?",
                           "type": "enum",
                           "values": [0, 1, 2],
                           "option_descriptions": {"0": "Unknown or None",
                                                   "1": "One relative",
                                                   "2": "More than one relative"}},
                       "ihyp": {
                           "description": "Has the patient had at least one breast biopsy with atypical hyperplasia?",
                           "type": "enum",
                           "values": [0, 1, 99],
                           "option_descriptions": {"0": "No or No Biopsies",
                                                   "1": "Yes",
                                                   "99": "Unknown, or Unknown for \"Ever had biopsy?\""}},
                       "ethnicity": {"description": "What is the patient's race/ethnicity?",
                                     "type": "enum",
                                     "input_mappings": {"white": 1,
                                                        "africanAmerican": 2,
                                                        "hispanic": 3,
                                                        "chinese": 7,
                                                        "japanese": 8,
                                                        "filipino": 9,
                                                        "otherAsianAmerican": 12,
                                                        "americanIndian": 1,
                                                        "hawaiian": 10,
                                                        "pacificIslander": 11,
                                                        "unknown": 1},
                                     "values": [1, 2, 3, 7, 8, 9, 10, 11, 12],
                                     "option_descriptions": {"1": "White, American Indian, Alaskan Native, Unknown",
                                                             "2": "African American",
                                                             "3": "Hispanic",
                                                             "7": "Chinese",
                                                             "8": "Japanese",
                                                             "9": "Filipino",
                                                             "10": "Hawaiian",
                                                             "11": "Other Pacific Islander",
                                                             "12": "Other Asian-American", }}}
        self.calc = gail_calc.GailRiskCalculator()
        self.calc.Initialize()

    def get_input_fields_json(self):
        return json.dumps(self.fields)

    def get_intput_field_names_json(self):
        return json.dumps(self.fields.keys())

    def get_input_field_names(self):
        return self.fields.keys()

    def valid_input_field(self, field_name):
        return field_name in self.fields.keys()

    def validate_inputs(self, inputs):
        in_keys = inputs.keys()
        missing = list(filter(lambda x: x not in in_keys, self.get_input_field_names()))
        extra = list(filter(lambda x: x not in self.get_input_field_names(), in_keys))
        valid = list(filter(lambda x: x in self.get_input_field_names(), in_keys))
        out_of_bounds = []
        for k in valid:
            if self.fields[k]["type"] is "enum":
                if inputs[k] not in self.fields[k]["input_mappings"].keys():
                    out_of_bounds.append(k)
            elif self.fields[k]["type"] is "range":
                if not (self.fields[k]["minimum"] <= inputs[k] <= self.fields[k]["maximum"]):
                    out_of_bounds.append(k)
        errors = {}
        if len(missing) > 0:
            errors["missing"] = missing
        if len(extra) > 0:
            errors["extra"] = extra
        if len(out_of_bounds) > 0:
            errors["out_of_bounds"] = out_of_bounds
        return errors

    def run(self, inputs):
        errors = self.validate_inputs(inputs)
        return_obj = {"code": 200}
        ra_obj = None
        if len(errors.keys()) > 0:
            return_obj["code"] = 400
            return_obj["errors"] = errors
        if len(errors.keys()) == 0 or "out_of_bounds" not in errors.keys():
            # if none of the inputs are 'wrong', go ahead and run the risk calculation anyway
            ra_obj = self.do_calculation(inputs)
        return_obj["assessment"] = ra_obj.getJson()
        return json.dumps(return_obj)

    # Run the risk assesment on inputs that have been previously validated
    # Return a 'RiskAssesment' object
    def do_calculation(self, inputs):
        age_indicator = 0 if inputs['age'] < 50 else 1
        rhyp = np.float64(1.0)
        if inputs['ever_had_biopsy'] == 1:
            if inputs['ihyp'] == 0:
                rhyp = np.float64(0.93)
            elif inputs['ihyp'] == 1:
                rhyp = np.float(1.82)

        fiveYearABS = self.calc.CalculateAbsoluteRisk(inputs['age'],
                                                      inputs['age'] + 5,
                                                      age_indicator,
                                                      inputs['num_biopsy'],
                                                      inputs['menarch_age'],
                                                      inputs['live_birth_age'],
                                                      inputs['ever_had_biopsy'],
                                                      inputs['first_deg_relatives'],
                                                      inputs['ihyp'],
                                                      rhyp,
                                                      inputs['race'])
        fiveYearAVE = self.calc.CalculateAeverageRisk(inputs['age'],
                                                      inputs['age'] + 5,
                                                      age_indicator,
                                                      inputs['num_biopsy'],
                                                      inputs['menarch_age'],
                                                      inputs['live_birth_age'],
                                                      inputs['ever_had_biopsy'],
                                                      inputs['first_deg_relatives'],
                                                      inputs['ihyp'],
                                                      rhyp,
                                                      inputs['race'])
        lifetimeABS = self.calc.CalculateAbsoluteRisk(inputs['age'],
                                                      90,
                                                      age_indicator,
                                                      inputs['num_biopsy'],
                                                      inputs['menarch_age'],
                                                      inputs['live_birth_age'],
                                                      inputs['ever_had_biopsy'],
                                                      inputs['first_deg_relatives'],
                                                      inputs['ihyp'],
                                                      rhyp,
                                                      inputs['race'])
        lifetimeAve = self.calc.CalculateAeverageRisk(inputs['age'],
                                                      90,
                                                      age_indicator,
                                                      inputs['num_biopsy'],
                                                      inputs['menarch_age'],
                                                      inputs['live_birth_age'],
                                                      inputs['ever_had_biopsy'],
                                                      inputs['first_deg_relatives'],
                                                      inputs['ihyp'],
                                                      rhyp,
                                                      inputs['race'])

        results = assessment()
        results.setRiskScores(fiveYearABS, fiveYearAVE, lifetimeABS, lifetimeAve)

        return results
