import os

from django.db import models
from project import settings

PART_DATA_FILE = 'static/csv/upload/pdata.csv'
PART_FAIL_FILE = 'static/csv/upload/pfail.csv'


class PartDataFile(models.Model):

    class Meta:
        db_table = 'part_data_file'

    def content_file_name(instance, filename):
        return PART_DATA_FILE

    file = models.FileField(upload_to=content_file_name)
    uploaded = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print("[Debug] Upload part data file begin")
        upload_path = os.path.join(settings.BASE_DIR, PART_DATA_FILE)
        if os.path.isfile(upload_path):
            os.remove(upload_path)
        super(PartDataFile, self).save(*args, **kwargs)
        print("[Debug] Save part data file completed")


class PartFailFile(models.Model):
    class Meta:
        db_table = 'part_fail_file'

    def content_file_name(instance, filename):
        return PART_FAIL_FILE

    file = models.FileField(upload_to=content_file_name)
    uploaded = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print("[Debug] Upload part fail file begin")
        upload_path = os.path.join(settings.BASE_DIR, PART_FAIL_FILE)
        if os.path.isfile(upload_path):
            os.remove(upload_path)
        super(PartFailFile, self).save(*args, **kwargs)
        print("[Debug] Save part fail file completed")
