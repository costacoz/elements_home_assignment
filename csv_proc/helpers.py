"""
Helper classes.
"""
import base64
import csv
import io
import logging
from multiprocessing import Pool

import requests
from PIL import Image

from elements_assignment.settings import IMG_MOB_MAX_HEIGHT, IMG_MOB_MAX_WIDTH


class CSVHelper:
    """
    Helper class that contains CSV file processing methods.
    """

    @staticmethod
    def get_csv_data(csv_url):
        """
        Retrieves CSV data using URL and returns CSV file's data list.
        """
        try:
            csv_data = CSVHelper.fetch_csv(csv_url)
        except CSVException as e:
            logging.exception(e)
            raise CSVException('Unable to fetch CSV file')

        csv_reader = csv.reader(csv_data, delimiter=',')

        return list(csv_reader)

    @staticmethod
    def fetch_csv(url):
        """
        Fetch CSV file from csv_url url.
        :str:
        """
        try:
            csv_response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logging.exception(e)
            raise CSVException('Incorrect CSV file URL')

        return csv_response.text.split('\r\n')

    @staticmethod
    def get_header_fields_pos(header, *fields):
        """
        Returns the position for each field in fields according to the header of CSV file.

        :int: position of field in the header.
        """
        positions = []
        for f in fields:
            positions.append(list(map(str.lower, header)).index(f))
        return positions


class CSVException(Exception):
    """
    Custom exception class for CSVHelper
    """

    def __init__(self, msg):
        super(self).__init__(msg)


class ImageHelper:
    """
    Helper class that contains image processing methods.
    """

    @staticmethod
    def convert_images(image_urls):
        """
        Takes set of images, converts them and returns dictionary with image_url: base64.

        Input: set of images
        Output: dict with image_url: base64
        """
        with Pool() as p:
            images_b64 = p.map(ImageHelper.fetch_and_convert_image, image_urls)
        return dict(zip(image_urls, images_b64))

    @staticmethod
    def fetch_and_convert_image(url):
        """
        Retrieves an image, makes sure it is mobile friendly and returns base64 string of the image.
        If URL is not an image, returns None.

        Input: image url string
        Output: image base64 string
        """

        img_file = ImageHelper.fetch_image_from_url(url)

        try:
            img = Image.open(img_file)
        except Exception as e:
            logging.exception(e)
            return None

        img_mobile = ImageHelper.make_img_mobile_friendly(img)
        img_base64 = ImageHelper.img_to_base64(img_mobile)

        return img_base64

    @staticmethod
    def fetch_image_from_url(url):
        """
        Fetches image from url.

        Input: url string.
        Output: image file.
        """
        try:
            img_response = requests.get(url)
        except requests.exceptions.RequestException as e:
            logging.exception(e)
            return None

        return io.BytesIO(img_response.content)

    @staticmethod
    def make_img_mobile_friendly(img):
        """
        Checks that image is mobile friendly and if not, then resize.

        Input: image file.
        Output: resized image file.
        """
        if img.width > IMG_MOB_MAX_WIDTH or img.height > IMG_MOB_MAX_HEIGHT:
            aspect_ratio = min(IMG_MOB_MAX_WIDTH / img.width, IMG_MOB_MAX_HEIGHT / img.height)
            new_width = int(img.width * aspect_ratio)
            new_height = int(img.height * aspect_ratio)
            resized_image = img.resize((new_width, new_height))
            resized_image.format = img.format
            return resized_image
        else:
            return img

    @staticmethod
    def img_to_base64(img):
        """
        Converts image to base64 string.

        Input: image file.
        Output: base64 string.
        """
        buffer = io.BytesIO()
        try:
            img.save(buffer, format=img.format)
        except ValueError as e:
            logging.exception(e)
            return None

        return base64.b64encode(buffer.getvalue()).decode('ascii')
