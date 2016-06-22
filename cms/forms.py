from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.forms import extras
from django.db.models import Q
from django.utils.text import slugify
from django.core.validators import URLValidator


class SignupForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget = forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput,\
	 help_text = 'Should be same as Password')
	def clean_password2(self):
		data_password1 = self.cleaned_data['password1']
		data_password2 = self.cleaned_data['password2']
		if data_password1 and data_password2 and data_password2 != data_password1:
			raise forms.ValidationError("Passwords don't match")
		return data_password2
	
	def save(self,commit = True):
		user = super(SignupForm, self).save(commit = False)
		user.set_password(self.cleaned_data.get('password1'))
		user.is_active = False
		if commit:
			user.save()
		return user
	
	class Meta:
		model = MyUser
		fields = ['username', 'email']



class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'dumb',\
	 'placeholder' : 'Enter Password'}))
	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username and password:
			print("authenticated")
			self.user_cache = authenticate(username = username, password = password)

			if self.user_cache is None:
				raise forms.ValidationError('Invalid username or Password')
			elif not self.user_cache.is_active:
				raise forms.ValidationError('User is not active')
			return 	self.cleaned_data
	
	def get_user(self):
		return self.user_cache