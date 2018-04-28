# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pipe',
            fields=[
                ('part_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('part_year', models.IntegerField()),
                ('diameter', models.IntegerField()),
                ('length', models.IntegerField()),
                ('material', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'pipes',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failure_year', models.IntegerField()),
                ('failure_type', models.CharField(max_length=50)),
                ('pipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipe.Pipe')),
            ],
            options={
                'db_table': 'records',
            },
        ),
    ]