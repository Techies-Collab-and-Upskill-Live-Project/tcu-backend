from rest_framework import serializers
from .models import ContactUs

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'email', 'name', 'message', 'enquiry_type', 'subject']
        read_only_fields = ['id']

class MessageSerializer(serializers.Serializer):
    detail = serializers.CharField()
    statusCode = serializers.IntegerField()
