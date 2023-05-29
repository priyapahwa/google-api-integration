from django.urls import path, include
from api.views import HomeView, GoogleCalendarInitView

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='google_calendar_init'),
]