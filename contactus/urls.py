from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContactUsView

router = DefaultRouter()
router.register(r'', ContactUsView, basename='contactus')

urlpatterns = [
    path('', ContactUsView.as_view({'post': 'contactus'}), name='contactus-send'),
]

urlpatterns += router.urls
