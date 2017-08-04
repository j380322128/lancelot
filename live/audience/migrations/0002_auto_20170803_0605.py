# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-03 06:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('audience', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='tel',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
