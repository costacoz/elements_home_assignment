"""
Views for csv_proc app.
"""
import csv

import requests
from django.http import JsonResponse, HttpResponse

from csv_proc.helpers import ImageHelper
from elements_assignment.settings import CSV_URL, IMG_MOB_MAX_HEIGHT, IMG_MOB_MAX_WIDTH


def process_csv(request):
    """
    Fetches CSV file from CSV_URL specified in settings.py and converts it to JSON.

    Response: json array
    """

    try:
        csv_response = requests.get(CSV_URL)
    except requests.exceptions.RequestException as e:
        print(e)
        return HttpResponse('Incorrect CSV file URL', status=500)

    csv_data = csv_response.text.split('\r\n')
    csv_reader = csv.reader(csv_data, delimiter=',')

    header = next(csv_reader)

    def get_header_field_pos(field_name):
        """
        Returns the position of field in the header of CSV file.

        :int: index of field in the header.
        """
        return list(map(str.lower, header)).index(field_name)

    title_pos = get_header_field_pos('title')
    description_pos = get_header_field_pos('description')
    image_pos = get_header_field_pos('image')

    result = list()
    processed_images = dict()

    for row in csv_reader:
        record = dict()
        record['title'] = row[title_pos]
        record['description'] = row[description_pos]

        if row[image_pos] in processed_images:
            record['image'] = processed_images[row[image_pos]]
        else:
            processed_images[row[image_pos]] = ImageHelper.process_image(row[image_pos])
            record['image'] = processed_images[row[image_pos]]

        result.append(record)

    return JsonResponse({'result': result})
