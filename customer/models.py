import re
from django import forms
from django.db import models
from django.forms import ModelForm
from admin import models as adminModel
import datetime


def validateDelimitComma(value):
    if re.search('^(([0-9a-zA-Z][0-9a-zA-Z_]*)([,][0-9a-zA-Z][0-9a-zA-Z_]*)*)$',value) == None:
        raise forms.ValidationError("Please enter values delimited by commas.")
    return value


def validateDateFormat(value):
    if re.search('^(((((0[1-9])|(1\d)|(2[0-8]))-((0[1-9])|(1[0-2])))|((31-((0[13578])|(1[02])))|((29|30)-((0[1,3-9])|(1[0-2])))))-((20[0-9][0-9]))|(29-02-20(([02468][048])|([13579][26]))))$', value) == None:
        raise forms.ValidationError("Please enter a proper date format.")
    return value


def validateTimeFormat(value):
    if re.search('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',value) == None:
        raise forms.ValidationError("Please enter a proper time format.")
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
    startDate = models.CharField(max_length=10)
    startTime = models.CharField(max_length=5)
    endDate = models.CharField(max_length=10)
    endTime = models.CharField(max_length=5)
    startLocation = models.CharField(max_length=256)
    endLocation = models.CharField(max_length=256)
    comments = models.CharField(max_length=256)

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
        exclude = ['cusId', 'jobId', 'dateCreated']

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


class TripForm(ModelForm):
    ROUND_TRIP_SELECTION = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )

    startDate = forms.CharField(label="Start Date", max_length=10, help_text="Format: DD-MM-YYYY", validators=[validateDateFormat])
    startTime = forms.CharField(label="Start Time", max_length=5, help_text="Format: 08:30, 16:45", validators=[validateTimeFormat])
    endDate = forms.CharField(label="End Date", max_length=10, help_text="Format: DD-MM-YYYY", validators=[validateDateFormat])
    endTime = forms.CharField(label="End Time", max_length=5, help_text="Format: 08:30, 16:45", validators=[validateTimeFormat])
    startLocation = forms.CharField(label="Starting Location", max_length=256)
    endLocation = forms.CharField(label="Ending Location", max_length=256)
    roundTrip = forms.ChoiceField(choices=ROUND_TRIP_SELECTION, widget=forms.RadioSelect())
    sedanAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of sedan cars needed", widget=forms.Select(attrs={'class': 'span2'}))
    mpvAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of mpv cars needed", widget=forms.Select(attrs={'class': 'span2'}))
    luxuryAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of luxury cars needed", widget=forms.Select(attrs={'class': 'span2'}))
    busAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of buses needed", widget=forms.Select(attrs={'class': 'span2'}))
    miniAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of mini buses needed", widget=forms.Select(attrs={'class': 'span2'}))
    coachAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of coach buses needed", widget=forms.Select(attrs={'class': 'span2'}))
    oneTonAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of 1-ton lorries needed", widget=forms.Select(attrs={'class': 'span2'}))
    threeTonAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of 3-ton lorries needed", widget=forms.Select(attrs={'class': 'span2'}))
    fiveTonAmt = forms.ChoiceField(choices=[(x, x) for x in range(0, 11)], label="No of 5-ton lorries needed", widget=forms.Select(attrs={'class': 'span2'}))
    comments = forms.CharField(label="Comments", max_length=256)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(TripForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Trip
        exclude = ['cusId', 'jobId', 'tripId']

    #check that startDate/endDate > todays date
    def clean_startDate(self):
        startDate = self.cleaned_data.get('startDate', '')
        startingDate = datetime.datetime.strptime(startDate, "%d-%m-%Y").date()
        now = datetime.datetime.now().date()
        if startingDate < now:
            raise forms.ValidationError("Enter a valid starting date")
        return startingDate


    def clean_endDate(self):
        endDate = self.cleaned_data.get('endDate', '')
        endingDate = datetime.datetime.strptime(endDate, "%d-%m-%Y").date()
        now = datetime.datetime.now().date()
        if endingDate < now:
            raise forms.ValidationError("Enter a valid ending date")
        return endingDate

    def clean(self):
        cleaned_data = super(TripForm, self).clean()
        startDate = self.cleaned_data.get('startDate')
        endDate = self.cleaned_data.get('endDate')
        startTime = self.cleaned_data.get('startTime')
        endTime = self.cleaned_data.get('endTime')
        if startDate is not None and endDate is not None and startTime is not None and endTime is not None:
            changedStartDateTimeString = str(startDate)+" "+str(startTime)+":00"
            changedEndDateTimeString = str(endDate)+" "+str(endTime)+":00"
            changedStartDateTime = datetime.datetime.strptime(changedStartDateTimeString, "%Y-%m-%d %H:%M:%S")
            changedEndDateTime = datetime.datetime.strptime(changedEndDateTimeString, "%Y-%m-%d %H:%M:%S")
            if changedEndDateTime < changedStartDateTime:
                msg = "End Date should be later than Start Date"
                self._errors["endDate"] = self.error_class([msg])
        return cleaned_data





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