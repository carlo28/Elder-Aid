from django import forms 
from meetings.models import MeetingPost

class CreateMeetingForm(forms.ModelForm):

    class Meta:
        model = MeetingPost
        fields = [
            'title',
            'image',
            'location',
            'time',
            'activity'
        ]

class UpdateMeetingPostForm(forms.ModelForm):

    class Meta:
        model = MeetingPost
        fields = ['title', 'image', 'location', 'time', 'activity']

        def save(self, commit=True):
            meeting_post = self.instance
            meeting_post.title = self.cleaned_data['title']
            meeting_post.location = self.cleaned_data['location']
            meeting_post.time = self.cleaned_data['time']
            meeting_post.activity = self.cleaned_data['activity']     

            if self.cleaned_data['image']:
                meeting_post.image = self.cleaned_data['image']

            if commit:
                meeting_post.save()
            return meeting_post()   