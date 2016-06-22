from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

GENDER_CHOICES = (('NS', '--'), ('M', 'Male'), ('F', 'Female'))

class MyUser(AbstractUser):
	dob = models.DateField(
		blank = True,
		 null = True,
	)
	phone_number = PhoneNumberField(
		max_length = 15,
		unique = True,
		null = True,
		blank = True,
	)
	gender = models.CharField(
		max_length = 2,
		choices = GENDER_CHOICES,
		default = GENDER_CHOICES[0][0]
	)

