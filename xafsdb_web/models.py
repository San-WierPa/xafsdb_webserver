"""
@author: Sebastian Paripsa
"""

import uuid

from django.db import models

from webserver.backends import PrivateMediaStorage


def upload_to(instance, filename):
    return f"{uuid.uuid4()}/{filename}"


class Files(models.Model):
    dataset_id = models.CharField(max_length=255, null=False, blank=False)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        null=False, blank=False, storage=PrivateMediaStorage(), upload_to=upload_to
    )

    def __str__(self):
        return f"{self.file_name}"

    def save(self, *args, **kwargs):
        self.file_name = self.file.name
        super(Files, self).save(*args, **kwargs)
