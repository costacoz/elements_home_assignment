import json

import requests
from django.test import Client
from django.test import TestCase
from requests import RequestException

from elements_assignment.settings import CSV_URL


class ProcessCSVTests(TestCase):

    def test_csv_file_exists(self):
        """
        Check that CSV file URL is accessible.
        """
        try:
            csv_response = requests.get(CSV_URL)
        except RequestException:
            return self.fail(msg="Exception while accessing CSV_URL")
        self.assertTrue(csv_response is not None)

    def test_response_is_json(self):
        """
        Tests that process_csv endpoint returns response in JSON format.
        """
        client = Client()
        response = client.get('/process_csv/')
        try:
            json.loads(response.content)
            return self.assertTrue(True)
        except ValueError:
            return self.fail(msg="Response is not JSON")
