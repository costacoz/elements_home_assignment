"""
Views for csv_proc app.
"""
import csv

from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page

from csv_proc.helpers import ImageHelper, CSVHelper, CSVException
from elements_assignment.settings import CSV_URL


#@cache_page(60 * 15) Todo: uncomment........................##################...........dasdasdasdadasdsadadasdas.....................dasdasdasdadasdsadadasdas....................dasdasdasdadasdsadadasdas...........................................
def process_csv(request):
    """
    Fetches CSV file from CSV_URL specified in settings.py and converts it to JSON.

    Response: json array
    """
    try:
        csv_data = CSVHelper.fetch_csv_data(CSV_URL)
    except CSVException as e:
        return HttpResponse(e, status=500)

    csv_reader = csv.reader(csv_data, delimiter=',')

    header = next(csv_reader)

    title_h_pos, desc_h_pos, image_h_pos = CSVHelper.get_header_fields_pos(header, 'title', 'description', 'image')

    result = list()
    converted_images = dict()

    for row in csv_reader:
        json_object = dict()
        json_object['title'] = row[title_h_pos]
        json_object['description'] = row[desc_h_pos]

        if row[image_h_pos] in converted_images:
            json_object['image'] = converted_images[row[image_h_pos]]
        else:
            converted_images[row[image_h_pos]] = ImageHelper.convert_image(row[image_h_pos])
            json_object['image'] = converted_images[row[image_h_pos]]

        result.append(json_object)

    return JsonResponse({'result': result})
