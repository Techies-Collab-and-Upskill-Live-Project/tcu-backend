from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.exception_handlers import ErrorEnum, ErrorResponse, response_schemas

from .models import ContactUs
from .serializers import ContactUsSerializer, MessageSerializer
from drf_spectacular.utils import extend_schema

class ContactUsView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()

    @response_schemas(
        response_model=MessageSerializer, code=201, schema_response_codes=[400]
    )
    @extend_schema(tags=['Contact Us'], summary='Contact Us using email')
    def contactus(self, request, **kwargs):
        try:
            # Use default values if enquiry_type or subject is not supplied
            enquiry_type = request.data.get('enquiry_type', 'General Inquiry')
            subject = request.data.get('subject', 'Enquiry')

            serializer = ContactUsSerializer(data={
                "email": request.data['email'],
                "name": request.data['name'],
                "message": request.data['message'],
                "enquiry_type": enquiry_type,
                "subject": subject
            })

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                data={"detail": "Enquiry successfully sent. Please check your mail for update shortly", "statusCode": 201},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print("e", e)
            return ErrorResponse(ErrorEnum.INVALID_DATA, detail=str(e)).response()

    @extend_schema(tags=['Contact Us'], summary='Get all Contact Messages')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=['Contact Us'], summary='Get a single Contact Message')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=['Contact Us'], summary='Delete a Contact Message')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
