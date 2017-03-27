import json
import calculators
import unittest
import utils
import urllib
from bs4 import BeautifulSoup
# import ssl
import time
from gail.gail import GailRiskCalculator

class CalculatorsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = calculators.app.test_client()

    # No special tearDown?
    # def tearDown(self):

    def get_NCI(self,
                genetics=0,
                current_age=48,
                age_at_menarche=2,
                age_at_first_live_birth=3,
                ever_had_biopsy=0,
                previous_biopsies=0,
                biopsy_with_hyperplasia=0,
                related_with_breast_cancer=0,
                race=0):

        serviceurl = "http://www.cancer.gov/bcrisktool/RiskAssessment.aspx?"
        scontext = None
        cgvfiveyearRiskABS = -1.1
        cgvfiveyearRiskAVE = -1.1
        cgvLifetimeRiskABS = -1.1
        cgvLifetimeRiskAVE = -1.1
        explainer = ""

        if age_at_menarche == 0:
            age_at_menarche = 14
        elif age_at_menarche == 1:
            age_at_menarche = 13
        elif age_at_menarche == 2:
            age_at_menarche = 10

        if age_at_first_live_birth == 3:
            age_at_first_live_birth = 30
        elif age_at_first_live_birth == 1:
            age_at_first_live_birth = 22
        elif age_at_first_live_birth == 0:
            # encode once at 15
            age_at_first_live_birth = 15
        elif age_at_first_live_birth == 2:
            # encode once at 27
            age_at_first_live_birth = 27

        url = serviceurl + urllib.urlencode(
            {"genetics": genetics, "current_age": current_age, "age_at_menarche": age_at_menarche,
             "age_at_first_live_birth": age_at_first_live_birth, "ever_had_biopsy": ever_had_biopsy,
             "previous_biopsies": previous_biopsies, "biopsy_with_hyperplasia": biopsy_with_hyperplasia,
             "related_with_breast_cancer": related_with_breast_cancer,
             "race": race})

        time.sleep(0.1)  # delays for 1 seconds
        myhtml = urllib.urlopen(url, context=scontext).read()
        soup = BeautifulSoup(myhtml, "lxml")

        tags = soup.find_all('p')
        explainer = explainer + str(tags[7]) + str(tags[8])

        tags = soup('span', {'id': 'ctl00_cphMain_lbl5YrAbsoluteRisk'})
        for x in tags: cgvfiveyearRiskABS = (float(x.get_text()[:-1]) / 100)

        tags = soup('span', {'id': 'ctl00_cphMain_lbl5YrAveragRisk'})
        for x in tags: cgvfiveyearRiskAVE = (float(x.get_text()[:-1]) / 100)

        tags = soup('span', {'id': 'ctl00_cphMain_lblLifetimeAbsoluteRisk90'})
        for x in tags: cgvLifetimeRiskABS = (float(x.get_text()[:-1]) / 100)

        tags = soup('span', {'id': 'ctl00_cphMain_lblLifeTimeAverageRisk90'})

        for x in tags: cgvLifetimeRiskAVE = (float(x.get_text()[:-1]) / 100)

        return (utils.roundLikeNCI(cgvfiveyearRiskABS),
                utils.roundLikeNCI(cgvfiveyearRiskAVE),
                utils.roundLikeNCI(cgvLifetimeRiskABS),
                utils.roundLikeNCI(cgvLifetimeRiskAVE))

    def test_bad_calc_name(self):
        print "Testing Unknown Calculator Name (For v2.0)"
        # test getting the docs for a bad calc
        rv = self.app.get('/api/v2.0/bad_calc')
        assert rv.status_code == 501
        rv = self.app.get('/api/v2.0/bad_calc/json')
        assert rv.status_code == 501
        rv = self.app.post('/api/v2.0/bad_calc', data="[Doesn't matter]")
        assert rv.status_code == 501

    def test_gail_calc_doc(self):
        print "Testing GAIL Doc URLs (For v2.0)"
        rv = self.app.get('/api/v2.0/gail')
        assert rv.status_code == 200
        assert "VisExcell API For GAIL - version 2.0" in rv.get_data()
        rv = self.app.get('/api/v2.0/gail/json')
        assert rv.status_code == 200
        assert rv.mimetype == "application/json"

    def test_gail_calc_post(self):
        print "Testing getting GAIL results for (v2.0)"
        post_data = {
            "age": 48,
            "menarch_age": 2,
            "live_birth_age": 3,
            "ever_had_biopsy": 1,
            "num_biopsy": 2,
            "first_deg_relatives": 2,
            "ihyp": 1,
            "race": 1
        }

        expected_results = {
            "five_year_abs": 0.10708078148151635,
            "five_year_ave": 0.011606210299941746,
            "lifetime_abs": 0.59497901225876715,
            "lifetime_ave": 0.1148439582786286
        }
        rv = self.app.post('/api/v2.0/gail',data=json.dumps(post_data),content_type='application/json')
        response_obj = json.loads(rv.get_data())
        self.assertEqual(response_obj["code"],200)
        self.assertEqual(len(response_obj["assessment"]["results"].keys()), 4)
        for ex_result in expected_results:
            self.assertEqual(response_obj["assessment"]["results"][ex_result],expected_results[ex_result])

    # TODO: Add bad post data to check error responses

    def test_unknown_biopsies(self):
        print "Testing for unknown biopsy bug (using v1.0)"
        post_data = {
            "age": 40,
            "menarch_age": 2,
            "live_birth_age": 0,
            "ever_had_biopsy": 0,
            "num_biopsy": 0,
            "first_deg_relatives": 0,
            "ihyp": 99,
            "race": 3
        }

        ever_had_vals = [0,99]
        num_vals = [0,1,2]
        hyp_vals = [0,1,99]

        for nv in num_vals:
            post_data["num_biopsy"] = nv
            for ehv in ever_had_vals:
                post_data["ever_had_biopsy"] = ehv
                for hv in hyp_vals:
                    post_data["ihyp"] = hv
                    # print "-------"
                    # print post_data
                    rv = self.app.post('/api/v1.0/gail', data=json.dumps(post_data), content_type="application/json")
                    output = json.loads(rv.get_data())
                    fyr =  utils.roundLikeNCI(output["results"]["five_year_abs"])
                    fyra = utils.roundLikeNCI(output["results"]["five_year_ave"])
                    ltr =  utils.roundLikeNCI(output["results"]["lifetime_abs"])
                    ltra = utils.roundLikeNCI(output["results"]["lifetime_ave"])
                    # print "Ours:\t5yr: %.4f\t5ave: %.4f\tLTR: %.4f\tLTA: %.4f" % (fyr,fyra,ltr,ltra)
                    cleaned_ever_had, cleaned_number, cleaned_hyp = GailRiskCalculator.clean_biopsy_inputs(post_data["ever_had_biopsy"], post_data["num_biopsy"],post_data["ihyp"])
                    (nci_fyr,nci_fyra,nci_ltr,nci_ltra) = self.get_NCI(current_age=post_data["age"],
                                                       age_at_menarche=post_data["menarch_age"],
                                                       age_at_first_live_birth=post_data["live_birth_age"],
                                                       ever_had_biopsy=cleaned_ever_had,  # post_data["ever_had_biopsy"],
                                                       previous_biopsies=cleaned_number,  # post_data["num_biopsy"],
                                                       biopsy_with_hyperplasia=cleaned_hyp,  # post_data["ihyp"],
                                                       related_with_breast_cancer=post_data["first_deg_relatives"],
                                                       race=post_data["race"])
                    # print "NCIs:\t5yr: %.4f\t5ave: %.4f\tLTR: %.4f\tLTA: %.4f" % (fyr, fyra, ltr, ltra)
                    self.assertEqual((fyr, fyra, ltr, ltra),(nci_fyr,nci_fyra,nci_ltr,nci_ltra), "Inputs: %r" % post_data)

    def test_calculations_valid_inputs(self):
        print "Testing for valid inputs (using v1.0)"
        test_inputs = [{"age": 42, "menarch_age": 2, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 1},
                       {"age": 50, "menarch_age": 2, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 1},
                       {"age": 68, "menarch_age": 2, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 1},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 1, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 2, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 1, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 2, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 3, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 1, "ihyp": 99, "race": 3},
                       {"age": 42, "menarch_age": 0, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 2, "ihyp": 99, "race": 3},]
        races_to_test = [1,2,7,8,9,10,11,12]  # (3 is tested in above)
        for r in races_to_test:
            test_inputs.append({"age": 42, "menarch_age": 2, "live_birth_age": 0, "ever_had_biopsy": 0, "num_biopsy": 0, "first_deg_relatives": 0, "ihyp": 99, "race": r})

        for post_data in test_inputs:
            # print post_data
            rv = self.app.post('/api/v1.0/gail', data=json.dumps(post_data), content_type="application/json")
            output = json.loads(rv.get_data())
            fyr = utils.roundLikeNCI(output["results"]["five_year_abs"])
            fyra = utils.roundLikeNCI(output["results"]["five_year_ave"])
            ltr = utils.roundLikeNCI(output["results"]["lifetime_abs"])
            ltra = utils.roundLikeNCI(output["results"]["lifetime_ave"])
            (nci_fyr, nci_fyra, nci_ltr, nci_ltra) = self.get_NCI(current_age=post_data["age"],
                                                                  age_at_menarche=post_data["menarch_age"],
                                                                  age_at_first_live_birth=post_data["live_birth_age"],
                                                                  ever_had_biopsy=post_data["ever_had_biopsy"],
                                                                  previous_biopsies=post_data["num_biopsy"],
                                                                  biopsy_with_hyperplasia=post_data["ihyp"],
                                                                  related_with_breast_cancer=post_data[
                                                                      "first_deg_relatives"],
                                                                  race=post_data["race"])
            self.assertEqual((fyr, fyra, ltr, ltra), (nci_fyr, nci_fyra, nci_ltr, nci_ltra), "Inputs: %r" % post_data)

if __name__ == '__main__':
    unittest.main()
