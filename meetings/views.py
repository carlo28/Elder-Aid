from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from meetings.models import MeetingPost
from meetings.forms import CreateMeetingForm, UpdateMeetingPostForm
from users.models import Account

def create_meeting_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateMeetingForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        creator = Account.objects.filter(email=user.email).first()
        obj.creator = creator
        obj.save()
        form = CreateMeetingForm()

    context['form'] = form

    return render(request, "meetings/create_meeting.html", {})

def detail_meeting_view(request, slug):

    context = {}

    meeting_post = get_object_or_404(MeetingPost, slug=slug)
    context['meeting_post'] = meeting_post

    return render(request, 'meetings/detail_meeting.html', context)

def edit_meeting_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    meeting_post = get_object_or_404(MeetingPost, slug=slug)
    
    if meeting_post.creator != user:
        return HttpResponse("You are not the creator of that meeting.")
    
    if request.POST:
        form = UpdateMeetingPostForm(request.POST or None, request.FILES or None, instance=meeting_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            meeting_post = obj
    form = UpdateMeetingPostForm(
        initial= {
            "title": meeting_post.title,
            "location": meeting_post.location,
            "time": meeting_post.time,
            "activity": meeting_post.activity,
            "image": meeting_post.image,
        }
    )
    
    context['form'] = form
    return render(request, 'meetings/edit_meeting.html', context)

def get_meeting_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = MeetingPost.objects.filter(
            Q(title__icontains=q)|
            Q(location__icontains=q)|
            Q(time__icontains=q)|
            Q(activity__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))

