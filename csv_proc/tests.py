import csv
import json

import requests
from PIL import Image
from django.test import Client
from django.test import TestCase
from requests import RequestException

from csv_proc.helpers import ImageHelper, CSVHelper
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


class ImageHelperTests(TestCase):

    def test_fetch_image_from_url(self):
        """
        Checks that method correctly fetches image.
        """
        img_file = ImageHelper.fetch_image_from_url('https://docs.python.org/3/_static/py.png')
        self.assertTrue(img_file is not None)

        try:
            img = Image.open(img_file)
            return self.assertTrue(img.format == "PNG")
        except Exception as e:
            return self.fail(e)

    def test_make_img_mobile_friendly(self):
        """
        Tests that method returns unmodified image
        """
        img = Image.new('RGB', (60, 30), color='red')
        img_result = ImageHelper.make_img_mobile_friendly(img)
        self.assertTrue(img_result == img)
        self.assertTrue(img_result.width == 60)
        return self.assertTrue(img_result.height == 30)

    def test_make_img_mobile_friendly2(self):
        """
        Tests that method returns downsized image and not the same as initial image.
        """
        img = Image.new('RGB', (600, 900), color='red')
        img_result = ImageHelper.make_img_mobile_friendly(img)
        self.assertTrue(img_result != img)
        self.assertTrue(img_result.width <= 500)
        return self.assertTrue(img_result.height <= 500)

    def test_img_to_base64(self):
        img = Image.new('RGB', (60, 30), color='red')
        print(ImageHelper.img_to_base64(img))
        return self.assertTrue(True)


class CSVHelperTests(TestCase):

    def test_fetch_csv_data(self):
        csv_data = CSVHelper.get_csv_data(CSV_URL)
        return self.assertIsNotNone(csv_data)

    def test_get_header_fields_pos(self):
        csv_data = CSVHelper.get_csv_data(CSV_URL)
        header = csv_data[0]
        description, = CSVHelper.get_header_fields_pos(header, 'description')
        print(description)
        self.assertTrue(description == 1)
