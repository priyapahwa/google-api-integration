from django.views.generic import TemplateView

from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class GoogleCalendarInitView(APIView):
    def get(self, request):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES, redirect_uri='http://localhost:8000/home/')
        auth_url, _ = flow.authorization_url(prompt='consent')
        return Response({'auth_url': auth_url}, status=status.HTTP_200_OK)