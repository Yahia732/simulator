from django.test import TestCase
from rest_framework.response import Response
from timeseries.views import simulator
import simplejson

# Create your tests here.
class Testrequest(TestCase):

    def setUp(self):
        """initialize the Django test client"""
        self.ts = simulator()

    def test_200(self):
        json_string = u'{"start_date": "2021-01-01","end_date": "2022-01-01","use_case_name": "any","time_series_type": "additivie","producer_type":"csv","configuration": [{"Frequency": "1H","Trend_coefficient": 2,"Missing_percentage": 0.06,"Outlier_percentage": 10,"Noise_level": 10,"Cycle_amplitude": 3,"Cycle_frequency": 1,"seasonality": [{"frequency_type": "Weekly","frequency_multiplier": 1,"phase_shift": 0,"amplitude": 3},{"frequency": "Daily","multiplier": 2,"phase_shift": 90,"amplitude": 5}]}]}'
        json_data = simplejson.loads(json_string)
        self.response = self.ts.create('/pipeline-endpoint', json_data, content_type="application/json")
        self.assertEqual(self.response.status_code, "200")