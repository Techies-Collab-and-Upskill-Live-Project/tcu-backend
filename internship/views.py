from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
import cloudinary.uploader
import logging
import threading
from core.exception_handlers import ErrorEnum, ErrorResponse, response_schemas

from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer
from .signals import internship_application_submitted

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

logger = logging.getLogger(__name__)

def upload_certificate(application_id, certificate_content, certificate_name):
    try:
        upload_result = cloudinary.uploader.upload(certificate_content, resource_type="raw", public_id=certificate_name)
        application = InternshipApplication.objects.get(id=application_id)
        application.certificate = upload_result['url']
        application.save()
    except Exception as e:
        logging.error(f"Failed to upload certificate: {e} for application id {application_id}")

class InternshipApplicationView(APIView):
    serializer_class = InternshipApplicationSerializer

    @extend_schema(
            tags=['Internship Application'], summary='Submit an internship application',
            description='This endpoint is used to submit internship application'
        )
    def post(self, request, *args, **kwargs):
        serializer = InternshipApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            certificate = request.FILES.get('certificate', None)
            if certificate:
                certificate_content = certificate.read()
                certificate_name = certificate.name
                thread = threading.Thread(target=upload_certificate, args=(application.id, certificate_content, certificate_name))
                thread.start()
            return Response({"detail": "Application submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InternshipApplicationListView(ListAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

    @extend_schema(tags=['Internship Application'], summary='List all internship applications')
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            total_applications = queryset.count()
            response_data = {
                "total_applications": total_applications,
                "applications": serializer.data
            }
            logging.info("All applications retrieved successfully")
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error("An error occured")
            return ErrorResponse(ErrorEnum.ERR_003, e, response_schemas['500'])
class InternshipApplicationDetailView(RetrieveAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

    @extend_schema(tags=['Internship Application'], summary='Retrieve an internship application by ID')
    def get(self, request, *args, **kwargs):
        logging.info("Application retrieved successfully")
        return super().get(request, *args, **kwargs)

class InternshipApplicationDeleteView(DestroyAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer
    permission_classes = [IsAuthenticated]


    @extend_schema(tags=['Internship Application'], summary='Delete an internship application by ID')
    def delete(self, request, *args, **kwargs):
        application = self.get_object()
        application.delete()
        return Response({"detail": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class InternshipApplicationExportView(APIView):

    @extend_schema(
        tags=['Internship Application'],
        summary='Export all internship applications to Excel',
        description='This endpoint exports all internship applications to an Excel file.',
        responses={200: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
    )
    def get(self, request, *args, **kwargs):
        # Create a workbook and select the active worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Internship Applications"

        # Define the headers
        headers = [
            'No', 'Email', 'Full Name', 'Twitter Handle', 'LinkedIn', 'Skill',
            'Experience', 'About Skill', 'Certificate', 'Commitment', 'Birthdate', 'Application Date'
        ]

        # Write the headers to the first row
        for col_num, header in enumerate(headers, 1):
            col_letter = get_column_letter(col_num)
            ws[f'{col_letter}1'] = header

        # Get all applications and write to the worksheet
        applications = InternshipApplication.objects.all()
        for row_num, application in enumerate(applications, 2):
            ws[f'A{row_num}'] = row_num - 1  # Numbering
            ws[f'B{row_num}'] = application.email
            ws[f'C{row_num}'] = application.full_name
            ws[f'D{row_num}'] = application.twitter_handle
            ws[f'E{row_num}'] = application.linkedin
            ws[f'F{row_num}'] = application.skill
            ws[f'G{row_num}'] = application.experience
            ws[f'H{row_num}'] = application.about_skill
            ws[f'I{row_num}'] = application.certificate.url if application.certificate else ''
            ws[f'J{row_num}'] = 'Yes' if application.commitment else 'No'
            ws[f'K{row_num}'] = application.birthdate
            ws[f'L{row_num}'] = str(application.date_created)

        # Set the response content type to Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=internship_applications.xlsx'

        # Save the workbook to the response
        wb.save(response)

        return response

class InternshipApplicationSendMailView(APIView):

    @extend_schema(
        tags=['Internship Application'],
        summary='Send email to some Intern applications',
        description='This endpoint sends an email to some Intern applications.',
        responses={200: 'Email sent successfully'}
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        print("data", data)
        recipients = data.get('recipients', [])
        print("recipients", recipients)
        
        for recipient in recipients:
            name = recipient.get('name')
            email = recipient.get('email')
            internship_application_submitted.send(sender=self.__class__, name=name, email=email)
        return Response({'detail': 'Email sent successfully'}, status=status.HTTP_200_OK)