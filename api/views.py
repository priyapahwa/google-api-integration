from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import GoogleCalendarEventSerializer

# Create your views here.


class GoogleCalendarInitView(APIView):
    """
    API view for initializing Google Calendar integration.

    Generates the authorization URL and stores the state value in the session.
    URL: /rest/v1/calendar/init/
    """

    def get(self, request):
        """
        Handles the GET request and prompt the user to initiate
        the OAuth process.

        Returns:
        - auth_url (str): The authorization URL for Google
        Calendar integration.
        """
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
            prompt="consent", access_type="offline", include_granted_scopes="true")
        request.session["google_calendar_state"] = state
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)


class GoogleCalendarRedirectView(APIView):
    """
    API view for handling the redirect request from Google Calendar.

    Retrieves the access token and fetches a list of events
    from the user's calendar.
    URL: /rest/v1/calendar/redirect/
    """

    def get(self, request):
        """
        Handles the GET request and retrieves the access token
        from the redirect URL.

        Returns:
        - events (list): A list of events from the user's calendar.
        """
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
        flow.fetch_token(
            authorization_response=request.build_absolute_uri(),
            code=code)

        access_token = flow.credentials.token
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
