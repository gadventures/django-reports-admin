# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedReport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("report", models.CharField(max_length=255, null=True)),
                ("report_file", models.FileField(upload_to=b"dynamic/admin/reports")),
                ("run_by", models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
    ]
