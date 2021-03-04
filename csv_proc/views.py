"""
Views for csv_proc app.
"""
import csv
import io
import base64

import requests
from django.http import JsonResponse
from PIL import Image, UnidentifiedImageError

from elements_assignment.settings import CSV_URL, IMG_MOB_MAX_HEIGHT, IMG_MOB_MAX_WIDTH


def process_csv(request):
    """
    Fetches CSV file from CSV_URL specified in settings.py and converts it to JSON.

    GET parameters:
    GET['csv_url']: URL to CSV file

    Returns: json array
    """

    result = list()
    images = dict()

    csv_response = requests.get(CSV_URL)
    csv_data = csv_response.text.split('\r\n')
    csv_reader = csv.reader(csv_data, delimiter=',')

    header = next(csv_reader)

    def get_header_field_pos(field_name):
        """
        Output: the position of field in the header.
        """
        return list(map(str.lower, header)).index(field_name)

    def make_mobile_friendly(img):
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

    def img_to_base64(img):
        """
        Converts image to base64 string.

        Input: image file.
        Output: base64 string.
        """
        buffer = io.BytesIO()
        img.save(buffer, format=img.format)
        return base64.b64encode(buffer.getvalue()).decode('ascii')

    def process_image(url):
        """
        Retrieves an image, makes sure it is mobile friendly and returns base64 string of the image.
        If URL is not an image, returns None.

        Input: image url string
        Output: image base64 string
        """
        try:
            img_response = requests.get(url)
        except:
            return ''

        img_file = io.BytesIO(img_response.content)

        try:
            img = Image.open(img_file)
            img_mobile = make_mobile_friendly(img)
            img_base64 = img_to_base64(img_mobile)
        except UnidentifiedImageError:
            return None

        return img_base64

    title_pos = get_header_field_pos('title')
    description_pos = get_header_field_pos('description')
    image_pos = get_header_field_pos('image')

    for row in csv_reader:
        record = dict()
        record['title'] = row[title_pos]
        record['description'] = row[description_pos]

        if row[image_pos] in images:
            record['image'] = images[row[image_pos]]
        else:
            images[row[image_pos]] = process_image(row[image_pos])
            record['image'] = images[row[image_pos]]

        result.append(record)

    return JsonResponse({'result': result})
