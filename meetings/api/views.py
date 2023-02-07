from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

from users.models import Account
from meetings.models import MeetingPost
from meetings.api.serializers import MeetingPostSerializer

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_meeting_view(request, slug):
    try:
        meeting_post = MeetingPost.objects.get(slug=slug)
    except MeetingPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MeetingPostSerializer(meeting_post)
        return Response(serializer.data)

@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_meeting_view(request, slug):
    try:
        meeting_post = MeetingPost.objects.get(slug=slug)
    except MeetingPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if meeting_post.author != user:
        return Response({'response': "You don't have permission to edit that."})

    if request.method == "PUT":
        serializer = MeetingPostSerializer(meeting_post, data=request.data)
        data= {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_meeting_view(request, slug):
    try:
        meeting_post = MeetingPost.objects.get(slug=slug)
    except MeetingPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if meeting_post.author != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == "DELETE":
        operation= meeting_post.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_meeting_view(request):
    account = request.user

    meeting_post = MeetingPost(creator=account)

    if request.method == "POST":
        serializer = MeetingPostSerializer(meeting_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiMeetingView(ListAPIView):
    queryset = MeetingPost.objects.all()
    serializer_class = MeetingPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'location', 'time', 'activity', 'creator__username')