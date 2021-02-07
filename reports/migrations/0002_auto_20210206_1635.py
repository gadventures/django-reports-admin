# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2021-02-06 16:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="savedreport",
            name="report_file",
            field=models.FileField(upload_to="reports"),
        ),
        migrations.AlterField(
            model_name="savedreport",
            name="run_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]