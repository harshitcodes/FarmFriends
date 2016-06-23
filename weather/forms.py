
from django import forms
# from django.contrib.auth import authenticate
from .models import *
from django.forms import extras
from django.db.models import Q
from django.utils.text import slugify
# from django.core.validators import URLValidator


class LocationForm(forms.Form):
	location = forms.CharField(
			max_length = 200,
			label = 'Enter location to know weather',
			widget = forms.TextInput(
					attrs = {
						'placeholder' : 'Please Enter your complete location',
						'class' : 'form-control typeahead'
					}))


