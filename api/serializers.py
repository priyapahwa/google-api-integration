from rest_framework import serializers


class GoogleCalendarEventSerializer(serializers.Serializer):
    """
    Serializer for Google Calendar event data.

    Attributes:
        id (serializers.CharField): The ID of the event.
        summary (serializers.CharField): The summary or title of the event.
        start (serializers.DictField): The start date and time of the event.
        end (serializers.DictField): The end date and time of the event.
    """

    id = serializers.CharField()
    summary = serializers.CharField()
    start = serializers.DictField()
    end = serializers.DictField()
