# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 08:08
from __future__ import unicode_literals

import RawData.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RawData', '0006_auto_20171022_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partdatafile',
            name='file',
            field=models.FileField(upload_to=RawData.models.PartDataFile.content_file_name),
        ),
    ]
