from rest_framework import serializers

class DocumentUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=True)
    file = serializers.FileField(required=True)