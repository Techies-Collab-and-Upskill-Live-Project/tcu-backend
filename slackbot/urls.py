from django.urls import path
from .views import SlackEventsView

urlpatterns = [
    path('events/', SlackEventsView.as_view(), name='slackApp')
]