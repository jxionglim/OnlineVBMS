import dbaccess
from django import forms


class allTripCondForm(forms.Form):
    PERIOD_CHOICES = (('m', 'month'), ('y', 'year'), ('a', 'entire period'))

    qty = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], widget=forms.Select(attrs={'class': 'span1'}))
    period = forms.ChoiceField(choices=PERIOD_CHOICES, widget=forms.Select(attrs={'class': 'span1'}))
    startLocation = forms.ChoiceField()
    endLocation = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        startLocationArr = dbaccess.getJobStartLoc()
        endLocationArr = dbaccess.getJobEndLoc()
        START_CHOICES = [(x[0], x[0]) for x in startLocationArr]
        END_CHOICES = [(x[0], x[0]) for x in endLocationArr]
        START_CHOICES.append(('a', 'anywhere'))
        END_CHOICES.append(('e', 'everywhere'))
        super(allTripCondForm, self).__init__(*args, **kwargs)
        self.fields['startLocation'] = forms.ChoiceField(choices=START_CHOICES, widget=forms.Select(attrs={'class': 'span2'}))
        self.fields['endLocation'] = forms.ChoiceField(choices=END_CHOICES, widget=forms.Select(attrs={'class': 'span2'}))



class numJobNAmtForm(forms.Form):
    PERIOD_CHOICES = (('m', 'month'), ('y', 'year'), ('a', 'entire period'))
    ORDER_CHOICES = (('DESC', 'decreasing'), ('ASC', 'increasing'))

    qty = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], widget=forms.Select(attrs={'class': 'span1'}))
    period = forms.ChoiceField(choices=PERIOD_CHOICES, widget=forms.Select(attrs={'class': 'span1'}))
    order = forms.ChoiceField(choices=ORDER_CHOICES, widget=forms.Select(attrs={'class': 'span1'}))


class custDistForm(forms.Form):
    ORDER_CHOICES = (('DESC', 'decreasing'), ('ASC', 'increasing'))

    order = forms.ChoiceField(choices=ORDER_CHOICES, widget=forms.Select(attrs={'class': 'span1'}))


class coyJoblessForm(forms.Form):
    PERIOD_CHOICES = (('m', 'month'), ('y', 'year'), ('a', 'entire period'))

    qty = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)], widget=forms.Select(attrs={'class': 'span1'}))
    period = forms.ChoiceField(choices=PERIOD_CHOICES, widget=forms.Select(attrs={'class': 'span1'}))