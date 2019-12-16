from rest_framework import serializers
from .models import MetadataEntry, DocumentEntry


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataEntry
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentEntry
        fields = '__all__'
