from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True, help_text='Required. Add a valid email address')
	name = forms.CharField(max_length=120)
	phone = forms.CharField(max_length=120)
	birthdate = forms.CharField(max_length=120)

	class Meta:
		model = Account
		fields = ("username", "name", "email", "password1", "password2", "phone", "birthdate")

	# def save(self, commit=True):
	# 	user = super(RegistrationForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user

class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
	
	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():	
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email = email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.'% email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username = username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.'% username)

		
