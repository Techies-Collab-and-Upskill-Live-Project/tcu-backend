from rest_framework import serializers
from .models import InternshipApplication
from .utils import format_date

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
        application = super().create(validated_data)
        return application

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        birthdate = representation.get('birthdate')
        if birthdate:
            representation['birthdate'] = format_date(birthdate)
        return representation