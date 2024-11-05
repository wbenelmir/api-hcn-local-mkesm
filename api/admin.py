from django.contrib import admin

from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(GetRequest)
class GetRequestImportExport(ImportExportModelAdmin):
    fields = [
        'code',
        'nin',
    ]
    list_display = [
        'code',
        'nin',
        'status',
        'user',
        'date_req',
        'update_in',
    ]

