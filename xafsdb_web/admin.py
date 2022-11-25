from django.contrib import admin

from xafsdb_web.models import Files


class FilesAdmin(admin.ModelAdmin):
    list_display = (
        "dataset_id",
        "file_name",
        "file",
    )


admin.site.register(Files, FilesAdmin)
