from django.urls import path
from meetings.views import(
    create_meeting_view,
    detail_meeting_view,
    edit_meeting_view
)

app_name = 'meetings'

urlpatterns = [
    path('create/', create_meeting_view, name="create"),
    path('<slug>/', detail_meeting_view, name="detail"),
    path('<slug>/edit', edit_meeting_view, name="edit"),
]