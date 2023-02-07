from rest_framework import serializers

from meetings.models import MeetingPost



class MeetingPostSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_creator')

    class Meta:
        model = MeetingPost
        fields = ['title', 'location', 'image', 'time', 'activity', 'username']

    def get_username_from_creator(self, meeting_post):
        username = meeting_post.creator.username
        return username