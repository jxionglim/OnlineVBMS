import re
from django import forms
from django.db import models
from django.forms import ModelForm

def validateBlank(value):
    if len(value.strip()) == 0:
        raise forms.ValidationError("This field is required.")
    return value

class Company(models.Model):
	coyId = models.IntegerField()
	coyName = models.CharField(max_length=256)
	email = models.EmailField(max_length=256)
	faxNo = models.BigIntegerField()
	coyContactNo = models.BigIntegerField()
	zipcode = models.BigIntegerField()
	streetName = models.CharField(max_length=256)
	rating = models.DecimalField(max_digits=3, decimal_places=2)

	class Meta:
		managed = False

class Driver(models.Model):
	coyId = models.IntegerField()
	driverId = models.IntegerField()
	firstName = models.CharField(max_length=256)
	lastName = models.CharField(max_length=256)
	driverClass = models.CharField(max_length=2)
	driverContactNo = models.BigIntegerField()

	class Meta:
		managed = False

class Vehicle(models.Model):
	coyId = models.IntegerField()
	carplateNo = models.CharField(max_length=8)
	iuNo = models.IntegerField()
	manufacturer = models.CharField(max_length=256)
	model = models.CharField(max_length=256)
	transType = models.CharField(max_length=6)
	driverClass = models.CharField(max_length=2)
	capacity = models.IntegerField()

	class Meta:
		managed = False

class Lorry(models.Model):
	carplateNo = models.CharField(max_length=8)
	tons = models.IntegerField()

	class Meta:
		managed = False

class Car(models.Model):
	carplateNo = models.CharField(max_length=8)
	category = models.CharField(max_length=9)

	class Meta:
		managed = False

class Bus(models.Model):
	carplateNo = models.CharField(max_length=8)
	category = models.CharField(max_length=9)

	class Meta:
		managed = False

class AddCompanyForm(ModelForm):
	coyName = forms.CharField(max_length=256, label="Company Name", validators=[validateBlank])
	email = forms.EmailField(max_length=256, label="Email")
	faxNo = forms.IntegerField(label="Fax Number")
	coyContactNo = forms.IntegerField(label="Contact Number")
	zipcode = forms.IntegerField(label="Postal Code")
	streetName = forms.CharField(max_length=256, label="Street Name")

	class Meta:
		model = Company
		exclude = ['coyId', 'rating']

	def clean_coyContactNo(self):
		coyContactNo = self.cleaned_data.get('coyContactNo', '')
		if re.search('^(9|8|6)\d{7}$',str(coyContactNo)) == None:
			raise forms.ValidationError("Contact number must be a 8 digit number starting with 8 or 9")
		return coyContactNo

	def clean_faxNo(self):
		faxNo = self.cleaned_data.get('faxNo', '')
		if re.search('^(6)\d{7}$',str(faxNo)) == None:
			raise forms.ValidationError("Fax number must be a 8 digit number starting with 6")
		return faxNo

	def clean_zipcode(self):
		zipcode = self.cleaned_data.get('zipcode', '')
		if zipcode is not None:
			if re.search('^\d{6}$',str(zipcode)) == None:
				raise forms.ValidationError("Postal code must be a 6 digit number")
		return zipcode

class AddDriverForm(ModelForm):
	firstName = forms.CharField(max_length=256, label="First Name", validators=[validateBlank])
	lastName = forms.CharField(max_length=256, label="Last Name", validators=[validateBlank])
	driverClass = forms.CharField(max_length=2, label="Driving Class License", help_text="Format: 3, 3A ...")
	driverContactNo = forms.IntegerField(label="Contact Number")

	class Meta:
		model = Driver
		exclude = ['coyId', 'driverId']

	def clean_driverContactNo(self):
		driverContactNo = self.cleaned_data.get('driverContactNo', '')
		if re.search('^(9|8|6)\d{7}$',str(driverContactNo)) == None:
			raise forms.ValidationError("Contact number must be a 8 digit number starting with 8 or 9")
		return driverContactNo

class AddVehicleForm(ModelForm):
	carplateNo = forms.CharField(max_length=8, label="Carplate Number", validators=[validateBlank])
	iuNo = forms.IntegerField(label="IU Number")
	manufacturer = forms.CharField(max_length=256, label="Manufacturer", validators=[validateBlank])
	model = forms.CharField(max_length=256, label="Model", validators=[validateBlank])
	transType = forms.CharField(max_length=6, label="Transmission Type", help_text="Format: Manual/Auto")
	driverClass = forms.CharField(max_length=2, label="Driving Class needed", help_text="Format: 3, 3A ...")
	capacity = forms.IntegerField(label="Sitting Capacity")

	class Meta:
		model = Vehicle
		exclude = ['coyId']