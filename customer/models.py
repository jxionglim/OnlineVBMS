import re
from django import forms
from django.db import models
from django.forms import ModelForm
from admin import models as adminModel


def validateDelimitComma(value):
    if re.search('^(([0-9a-zA-Z][0-9a-zA-Z_]*)([,][0-9a-zA-Z][0-9a-zA-Z_]*)*)$',value) == None:
        raise forms.ValidationError("Please enter values delimited by commas.")
    return value

# Create your models here.
class Job(models.Model):
    cusId = models.BigIntegerField()
    coyId = models.IntegerField()
    jobId = models.IntegerField()
    dateCreated = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=3)
    paidStatus = models.CharField(max_length=8)

    class Meta:
        managed = False


class Trip(models.Model):
    cusId = models.IntegerField()
    jobId = models.IntegerField()
    tripId = models.IntegerField()
    dateReq = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    startLocation = models.CharField(max_length=256)
    endLocation = models.CharField(max_length=256)
    comments = models.TextField()

    class Meta:
        managed = False

class reqResources(models.Model):
    coyId = models.IntegerField()
    driverId = models.IntegerField()
    cusId = models.IntegerField()
    jobId = models.IntegerField()
    tripId = models.IntegerField()
    roundTrip = models.CharField(max_length=1)

    class Meta:
        managed = False


class JobForm(ModelForm):
    coyId = forms.IntegerField(label="Company")
    amount = forms.DecimalField(label="Amount")
    paidStatus = forms.CharField(label="Paid Status",max_length=1, min_length=1)

    class Meta:
        model = Job
        exclude = ['cusId','jobId','dateCreated']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount', '')
        if amount <= 0:
            raise forms.ValidationError("Enter a valid payment amount")
        return amount

    def clean_paidStatus(self):
        paidStatus = self.cleaned_data.get('paidStatus', '')
        if paidStatus != 'N' and paidStatus != 'Y':
            raise forms.ValidationError("Enter a valid paid status")
        return paidStatus


class companySearchForm(ModelForm):
    coyName = forms.CharField(max_length=256, label="Company Name:", validators=[validateDelimitComma])
    streetName = forms.CharField(max_length=256, label="Street Name:", validators=[validateDelimitComma])

    class Meta:
        model = adminModel.Company
        exclude = ['coyId', 'email', 'faxNo', 'coyContactNo', 'zipcode', 'rating']


class vehicleSearchForm(ModelForm):
    coyName = forms.CharField(max_length=256, label="Company Name:", validators=[validateDelimitComma])
    streetName = forms.CharField(max_length=256, label="Street Name:", validators=[validateDelimitComma])

    class Meta:
        model = adminModel.Company
        exclude = ['coyId', 'email', 'faxNo', 'coyContactNo', 'zipcode', 'rating']