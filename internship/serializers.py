from rest_framework import serializers
from .models import InternshipApplication
import cloudinary.uploader

class InternshipApplicationSerializer(serializers.ModelSerializer):
    certificate = serializers.FileField(required=False)

    class Meta:
        model = InternshipApplication
        fields = '__all__'

    def validate_certificate(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Certificate file size should be less than 5MB")
        return value

    def create(self, validated_data):
        certificate = validated_data.pop('certificate', None)
        if certificate:
            upload_result = cloudinary.uploader.upload(certificate, resource_type="raw")
            validated_data['certificate'] = upload_result['url']
        return super().create(validated_data)
