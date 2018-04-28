from django.contrib import admin
from .models import PartDataFile, PartFailFile


# Register your models here.
class PartDataFileAdmin(admin.ModelAdmin):  # customize how the admin work
    list_display = ['file', 'uploaded']


class PartFailFileAdmin(admin.ModelAdmin):  # customize how the admin work
    list_display = ['file', 'uploaded']


admin.site.register(PartDataFile, PartDataFileAdmin)
admin.site.register(PartFailFile, PartFailFileAdmin)