from rest_framework import serializers

from api.models import Deal


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"
