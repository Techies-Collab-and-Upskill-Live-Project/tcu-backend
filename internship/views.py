from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema

from core.exception_handlers import ErrorEnum, ErrorResponse, response_schemas

from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

class InternshipApplicationView(APIView):
    serializer_class = InternshipApplicationSerializer

    @extend_schema(
            tags=['Internship Application'], summary='Submit an internship application',
            description='This endpoint is used to submit internship application'
        )
    def post(self, request, *args, **kwargs):
        serializer = InternshipApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print("e", e)
            return ErrorResponse(ErrorEnum.INTERNAL_SERVER_ERROR, e, response_schemas['500'])
class InternshipApplicationDetailView(RetrieveAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

    @extend_schema(tags=['Internship Application'], summary='Retrieve an internship application by ID')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class InternshipApplicationDeleteView(DestroyAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

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
            'Experience', 'About Skill', 'Certificate', 'Commitment', 'Birthdate'
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

        # Set the response content type to Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=internship_applications.xlsx'

        # Save the workbook to the response
        wb.save(response)

        return response