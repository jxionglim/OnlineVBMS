import dbaccess
from django import forms
from django.db import models
from django.forms import ModelForm


class AnalysisForm(forms.Form):
    startLocationArr = dbaccess.getJobStartLoc()
    endLocationArr = dbaccess.getJobEndLoc()
    PERIOD_CHOICES = (('w', 'Week'), ('m', 'Month'), ('y', 'Year'), ('a', 'Entire Period'))
    START_CHOICES = [(x[0], x[0]) for x in startLocationArr]
    END_CHOICES = [(x[0], x[0]) for x in endLocationArr]

    qty = forms.ChoiceField(choices=[(x, x) for x in range(1, 12)])
    period = forms.ChoiceField(choices=PERIOD_CHOICES)
    startLocation = forms.ChoiceField(choices=START_CHOICES)
    endLocation = forms.ChoiceField(choices=END_CHOICES)