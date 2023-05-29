from django.views.generic import TemplateView
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import GoogleCalendarEventSerializer

# Create your views here.


class GoogleCalendarInitView(APIView):
    def get(self, request):
        SCOPES = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
            "https://www.googleapis.com/auth/calendar",
        ]
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES,
            redirect_uri="http://localhost:8000/rest/v1/calendar/redirect/",
        )
        auth_url, state = flow.authorization_url(
            prompt="consent", access_type="offline", include_granted_scopes="true"
        )
        request.session["google_calendar_state"] = state
        print(request.session["google_calendar_state"])
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)


class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        SCOPES = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
            "https://www.googleapis.com/auth/calendar",
        ]
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES,
            redirect_uri="http://localhost:8000/rest/v1/calendar/redirect/",
        )
        code = request.GET.get("code")
        state = request.GET.get("state")
        print("Code " + code)
        flow.fetch_token(authorization_response=request.build_absolute_uri(), code=code)
        access_token = flow.credentials.token
        print("Access Token " + access_token)
        event = build("calendar", "v3", credentials=flow.credentials)
        events_result = (
            event.events()
            .list(
                calendarId="primary",
                maxResults=15,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        serializer = GoogleCalendarEventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
