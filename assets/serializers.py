from rest_framework import serializers
from .models import MetadataEntry, DocumentEntry


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataEntry
        fields = (
            'id',
            'name',
            'string',
            'owner',
        )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentEntry
        fields = (
            'id',
            'name',
            'file',
            'owner',
        )
