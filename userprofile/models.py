from django import forms
from django.db import models
from django.forms import ModelForm

class Customer(models.Model):
	cusId = models.IntegerField()
	firstName = models.CharField(max_length=256)
	lastName = models.CharField(max_length=256)
	contactNo = models.BigIntegerField()
	email = models.EmailField(max_length=256)
	zipcode = models.BigIntegerField()
	streetName = models.CharField(max_length=256)
	cExpDate = models.DateField()
	cSerialNo = models.BigIntegerField()
	password = models.CharField(max_length=256)
	
	class Meta:
		managed = False
		
class RegisterForm(ModelForm):
    class Meta:
		model = Customer
		exclude = ['cusId']
		widgets = {'password': forms.PasswordInput()}
		
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=256,label="Email")
    password = forms.CharField(max_length=256,widget=forms.PasswordInput)