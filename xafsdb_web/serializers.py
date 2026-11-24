"""
@author: Sebastian Paripsa
"""

from django.conf import settings
from rest_framework import serializers

from xafsdb_web.models import Files


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = "__all__"


class FileCreateUpdateSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(write_only=True)

    class Meta:
        model = Files
        fields = "__all__"
        extra_kwargs = {
            "file_name": {"read_only": True},
            "id": {"read_only": True},
        }

    def to_representation(self, instance):
        data = super(FileCreateUpdateSerializer, self).to_representation(instance)
        # instance.file.url is MEDIA_URL-relative for local storage (unlike S3's
        # absolute URLs); build an absolute URL so short_url()/TinyURL can use it.
        data["file"] = f"{settings.PUBLIC_BASE_URL}{instance.file.url}"
        return data
