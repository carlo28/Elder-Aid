from django.shortcuts import  render, redirect
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from meetings.views import get_meeting_queryset
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from operator import attrgetter
from meetings.models import MeetingPost

MEETING_POST_PER_PAGE = 10

def register_request(request):
	context = {}
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, "Registration successful." )
			return redirect("/")
		else:
			context['registration_form'] = form
			messages.error(request, "Unsuccessful registration. Invalid information.")
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render (request, 'register.html', context)

def login_request(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("home")
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				messages.info(request, f"You are now logged in using {email}.")
				return redirect("dashboard")
	else:
		form = AccountAuthenticationForm()
		messages.error(request,"Invalid username or password.")
	context['form'] = form
	return render(request, 'login.html', context)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

def home_view(request, *args, **kwargs):

	context  = {}

	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)
		
	meeting_posts = sorted(get_meeting_queryset(query), key=attrgetter('time'), reverse=True)

	page = request.GET.get('page', 1 )
	meeting_posts_paginator = Paginator(meeting_posts, MEETING_POST_PER_PAGE)

	try:
		meeting_posts = meeting_posts_paginator.page(page)
	except PageNotAnInteger:
		meeting_posts = meeting_posts_paginator.page(MEETING_POST_PER_PAGE)
	except EmptyPage:
		meeting_posts = meeting_posts_paginator.page(meeting_posts_paginator.num_pages)

	context['meeting_posts'] = meeting_posts

	return render(request, "home.html", context)

def account_view(request):

	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user )
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(
			initial = {
				"email": request.user.email,
				"username": request.user.username,
			}
		)
	context['account_form'] = form

	meeting_posts = MeetingPost.objects.filter(creator=request.user)
	context['meeting_posts'] = meeting_posts

	return render(request, "account.html", context)

def dashboard_view(request):
	return render(request, "dashboard.html")

def must_athenticate_view(request):
	return render(request, 'users/must_authenticate.html', {})
