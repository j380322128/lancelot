# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-30 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anchor', '0005_auto_20170728_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anchorinfo',
            name='image',
            field=models.ImageField(null=True, upload_to='static/image/'),
        ),
    ]
