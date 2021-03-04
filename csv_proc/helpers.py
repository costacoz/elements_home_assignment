"""
Helper classes.
"""
import base64
import io

import requests
from PIL import Image, UnidentifiedImageError

from elements_assignment.settings import IMG_MOB_MAX_HEIGHT, IMG_MOB_MAX_WIDTH


class ImageHelper:
    """
    Helper class that contains image processing methods.
    """

    @staticmethod
    def process_image(url):
        """
        Retrieves an image, makes sure it is mobile friendly and returns base64 string of the image.
        If URL is not an image, returns None.

        Input: image url string
        Output: image base64 string
        """
        try:
            img_response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        img_file = io.BytesIO(img_response.content)

        try:
            img = Image.open(img_file)
            img_mobile = ImageHelper.make_img_mobile_friendly(img)
            img_base64 = ImageHelper.img_to_base64(img_mobile)
        except UnidentifiedImageError as e:
            print(e)
            return None

        return img_base64

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
        img.save(buffer, format=img.format)
        return base64.b64encode(buffer.getvalue()).decode('ascii')
