from meetings.api.views import (
    api_detail_meeting_view,
    api_delete_meeting_view,
    api_update_meeting_view,
    api_create_meeting_view,
    ApiMeetingView
)

from django.urls import path

app_name = "meetings"

urlpatterns = [
    path('<slug>/', api_detail_meeting_view, name="detail"),
    path('<slug>/update', api_update_meeting_view, name="update"),
    path('<slug>/delete', api_delete_meeting_view, name="delete"),
    path('create', api_create_meeting_view, name="create"),
    path('list', ApiMeetingView.as_view(), name="list"),


]