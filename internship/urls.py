from django.urls import path
from .views import (
    InternshipApplicationView,
    InternshipApplicationListView,
    InternshipApplicationDetailView,
    InternshipApplicationDeleteView,
    InternshipApplicationExportView,
    InternshipApplicationSendMailView,
    InternshipApplicationRejectionMailView
)

urlpatterns = [
    path('register/entry/', InternshipApplicationView.as_view(), name='internship-application'),
    path('applications/', InternshipApplicationListView.as_view(), name='internship-application-list'),
    path('applications/<uuid:pk>', InternshipApplicationDetailView.as_view(), name='internship-application-detail'),
    path('applications/delete/<uuid:pk>', InternshipApplicationDeleteView.as_view(), name='internship-application-delete'),
    path('applications/export/', InternshipApplicationExportView.as_view(), name='internship-application-export'),
    path('send-mail/', InternshipApplicationSendMailView.as_view(), name='internship-application-send-acceptance-mail'),
    path('send-rejection-mail/', InternshipApplicationRejectionMailView.as_view(), name='internship-application-send-rejection-mail'),
]
