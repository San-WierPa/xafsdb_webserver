"""
@author: Sebastian Paripsa
"""

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
        data["file"] = instance.file.url
        return data
