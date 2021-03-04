"""
Views for csv_proc app.
"""

from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page

from csv_proc.helpers import ImageHelper, CSVHelper, CSVException
from elements_assignment.settings import CSV_URL


@cache_page(60 * 15)
def process_csv(request):
    """
    Fetches CSV file from CSV_URL specified in settings.py and converts it to JSON.

    Response: json array
    """
    try:
        csv_data = CSVHelper.get_csv_data(CSV_URL)
    except CSVException as e:
        return HttpResponse(e, status=500)

    title_h_pos, desc_h_pos, img_h_pos = CSVHelper.get_header_fields_pos(csv_data[0], 'title', 'description', 'image')

    result = list()
    images_to_convert = set()

    for row in csv_data[1:]:
        images_to_convert.add(row[img_h_pos])

    converted_images = ImageHelper.convert_images(images_to_convert)

    for row in csv_data[1:]:
        json_object = dict()
        json_object['title'] = row[title_h_pos]
        json_object['description'] = row[desc_h_pos]

        if row[img_h_pos] in converted_images:
            json_object['image'] = converted_images[row[img_h_pos]]

        result.append(json_object)

    return JsonResponse({'result': result})
