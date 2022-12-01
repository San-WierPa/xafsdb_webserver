# Generated by Django 4.0.6 on 2022-11-09 14:25

from django.db import migrations, models

import webserver.backends
import xafsdb_web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Files",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dataset_id", models.CharField(max_length=255)),
                ("file_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "file",
                    models.FileField(
                        storage=webserver.backends.PrivateMediaStorage(),
                        upload_to=xafsdb_web.models.upload_to,
                    ),
                ),
            ],
        ),
    ]
