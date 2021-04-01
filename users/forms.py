from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, UserToken


# DOCS - https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/

'''
Form that uses built-in UserCreationForm to handel user creation
'''
class UserForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Your first name..'}))
	last_name = forms.CharField(max_length=30, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Your last name..'}))
	username = forms.EmailField(max_length=254, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password..','class':'password'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )




'''
Form that uses built-in AuthenticationForm to handel user auth
'''
class AuthForm(AuthenticationForm):
	
	username = forms.EmailField(max_length=254, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))

	class Meta:
		model = User
		fields = ('username','password', )




'''
Basic model-form for our user profile that extends Django user model.
'''
class UserProfileForm(forms.ModelForm):

	telephone = forms.CharField(max_length=15, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Telephone..'}))
	address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
	town = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
	county = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
	post_code = forms.CharField(max_length=8, required=True, widget = forms.HiddenInput())
	country = forms.CharField(max_length=40, required=True, widget = forms.HiddenInput())
	longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
	latitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())


	class Meta:
		model = UserProfile
		fields = ('telephone', 'address', 'town', 'county', 'post_code', 'country', 'longitude', 'latitude')




'''
Form that uses built-in PasswordResetForm to handel a request to reset password
'''
class RequestPasswordForm(PasswordResetForm):
	
	email = forms.EmailField(max_length=254, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
	
	class Meta:
		model = User
		fields = ('email',)




'''
Form that uses built-in SetPasswordForm to handel resetting passwords
'''
class ForgottenPasswordForm(SetPasswordForm):
	
	new_password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))
	new_password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password..','class':'password'}))

	class Meta:
		model = User
		fields = ('password1', 'password2', )


