from rest_framework import serializers

class GoogleCalendarEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    summary = serializers.CharField()
    start = serializers.DictField()
    end = serializers.DictField()