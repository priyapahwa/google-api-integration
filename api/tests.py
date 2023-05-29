from unittest.mock import MagicMock, patch

from django.urls import reverse
from oauthlib.oauth2 import InsecureTransportError
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import GoogleCalendarEventSerializer


class GoogleCalendarInitViewTest(APITestCase):
    """Test case for the GoogleCalendarInitView."""

    def test_get(self):
        """
        Test the behavior of the GoogleCalendarInitView.

        This test ensures that the view handles the GET request correctly
        and returns the expected response. It also verifies the presence of
        the auth_url in the response data.
        """
        url = reverse("google_calendar_init")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("auth_url", response.data)
        self.assertTrue(
            response.data["auth_url"].startswith(
                "https://accounts.google.com/o/oauth2/auth"
            )
        )

    def test_get_session_state(self):
        """
        Test the behavior of the GoogleCalendarInitView for session state.

        This test ensures that the view sets the "google_calendar_state"
        session key appropriately.
        """
        url = reverse("google_calendar_init")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("google_calendar_state", self.client.session)
        self.assertIsNotNone(self.client.session["google_calendar_state"])


class GoogleCalendarRedirectViewTest(APITestCase):
    """Test case for the GoogleCalendarRedirectView."""

    @patch("api.views.build")
    @patch("api.views.InstalledAppFlow")
    def test_get(self, mock_flow, mock_build):
        """
        Test the behavior of the GoogleCalendarRedirectView.

        This test ensures that the view handles the GET request correctly,
        mocks the Google Calendar API flow and build methods to return a
        mock event object. It then asserts the validity of the response and
        the data returned by the view.
        """
        mock_flow.return_value.from_client_secrets_file.return_value = MagicMock()
        mock_flow.return_value.fetch_token.side_effect = InsecureTransportError()
        mock_event = MagicMock()
        mock_event.events.return_value.list.return_value.execute.return_value = {
            "items": []
        }
        mock_build.return_value = mock_event

        url = reverse("google_calendar_redirect")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class GoogleCalendarEventSerializerTest(APITestCase):
    """Test case for the GoogleCalendarEventSerializer."""

    def test_serializer(self):
        """
        Test the behavior of the GoogleCalendarEventSerializer.

        This test creates a sample data dictionary and instance
        of the serializer with the sample data. It then asserts
        the validity of the serializer, the validated data, and
        the serialized data.
        """
        data = {
            "id": "test_id",
            "summary": "test_summary",
            "start": {"test_start": "test_start"},
            "end": {"test_end": "test_end"},
        }
        serializer = GoogleCalendarEventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)
        self.assertEqual(serializer.data, data)
