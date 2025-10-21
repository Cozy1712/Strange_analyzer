from rest_framework import serializers
from .models import AnalyzedString

class AnalyzeSerializer(serializers.Serializer):
    value = serializers.CharField()

class AnalyzedStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedString
        fields = ["id", "value", "properties", "created_at"]
