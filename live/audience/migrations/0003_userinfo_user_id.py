# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-03 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audience', '0002_auto_20170803_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
