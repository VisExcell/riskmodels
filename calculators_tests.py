import json
import calculators
import unittest


class CalculatorsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = calculators.app.test_client()

    # No special tearDown?
    # def tearDown(self):

    def test_bad_calc_name(self):
        print "Testing Unknown Calculator Name"
        # test getting the docs for a bad calc
        rv = self.app.get('/api/v2.0/bad_calc')
        assert rv.status_code == 501
        rv = self.app.get('/api/v2.0/bad_calc/json')
        assert rv.status_code == 501
        rv = self.app.post('/api/v2.0/bad_calc', data="[Doesn't matter]")
        assert rv.status_code == 501

    def test_gail_calc_doc(self):
        print "Testing GAIL Doc URLs"
        rv = self.app.get('/api/v2.0/gail')
        assert rv.status_code == 200
        assert "VisExcell API For GAIL - version 2.0" in rv.get_data()
        rv = self.app.get('/api/v2.0/gail/json')
        assert rv.status_code == 200
        assert rv.mimetype == "application/json"

    def test_gail_calc_post(self):
        print "Testing getting GAIL results"
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


if __name__ == '__main__':
    unittest.main()
