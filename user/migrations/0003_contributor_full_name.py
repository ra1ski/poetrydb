# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-04 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_contributor_activation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='full_name',
            field=models.CharField(default='Test name', max_length=255),
            preserve_default=False,
        ),
    ]
