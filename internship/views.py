from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import InternshipApplication
from .serializers import InternshipApplicationSerializer

class InternshipApplicationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InternshipApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Application submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InternshipApplicationListView(ListAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        total_applications = queryset.count()
        response_data = {
            "total_applications": total_applications,
            "applications": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class InternshipApplicationDetailView(RetrieveAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

class InternshipApplicationDeleteView(DestroyAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

    def delete(self, request, *args, **kwargs):
        application = self.get_object()
        application.delete()
        return Response({"detail": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
