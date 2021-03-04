"""
    Django URLs paths.
"""

from django.contrib import admin
from django.urls import path

from csv_proc.views import process_csv

urlpatterns = [
    path('process_csv/', process_csv),
    path('admin/', admin.site.urls),
]
