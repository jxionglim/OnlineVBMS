import re, dbaccess
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
    drivingClass = models.CharField(max_length=2)
    driverContactNo = models.BigIntegerField()

    class Meta:
        managed = False

class Vehicle(models.Model):
    carplateNo = models.CharField(max_length=8)
    iuNo = models.IntegerField()
    manufacturer = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    capacity = models.IntegerField()
    drivingClass = models.CharField(max_length=2)
    transType = models.CharField(max_length=6)
    vehType = models.CharField(max_length=1)
    coyId = models.IntegerField()

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
    coyContactNo = forms.IntegerField(label="Contact Number")
    faxNo = forms.IntegerField(label="Fax Number")
    streetName = forms.CharField(max_length=256, label="Street Name")
    zipcode = forms.IntegerField(label="Postal Code")

    class Meta:
        model = Company
        exclude = ['coyId', 'rating']

    def __init__(self, *args, **kw):
        super(ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'coyName',
            'email',
            'streetName',
            'zipcode',
            'coyContactNo',
            'faxNo']

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if dbaccess.checkUniqueEmail(email) is False:
            raise forms.ValidationError("Email already exist")
        return email

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
    drivingClass = forms.ChoiceField(choices=[('', "Please select an option"),('3', "3"),('3a','3a'),('4', '4'),('4a', '4a'),('5', '5')], label="Driving Class License")
    driverContactNo = forms.IntegerField(label="Contact Number")

    class Meta:
        model = Driver
        exclude = ['coyId', 'driverId']

    def clean_driverContactNo(self):
        driverContactNo = self.cleaned_data.get('driverContactNo', '')
        if re.search('^(9|8|6)\d{7}$',str(driverContactNo)) == None:
            raise forms.ValidationError("Contact number must be a 8 digit number starting with 8 or 9")
        return driverContactNo


class AddVehicleForm(forms.Form):
    vehType = forms.ChoiceField(choices=[('', "Please select an option"),('c', "Car"),('b','Bus'),('l', 'Lorry')], label="Type of Vehicle", widget=forms.Select(attrs={"onChange": 'handleSelection(value)'}))
    carplateNo = forms.CharField(max_length=8, label="Carplate Number", validators=[validateBlank])
    iuNo = forms.IntegerField(label="IU Number")
    manufacturer = forms.CharField(max_length=256, label="Manufacturer", validators=[validateBlank])
    model = forms.CharField(max_length=256, label="Model", validators=[validateBlank])
    capacity = forms.IntegerField(label="Sitting Capacity")
    transType = forms.CharField(max_length=6, label="Transmission Type", help_text="Note: For lorry type vehicles, Transmission Type is Manual by default.")
    category = forms.CharField(max_length=9, label="Category", validators=[validateBlank], required=False)
    tons = forms.IntegerField(label="Tons", required=False)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(AddVehicleForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'vehType',
            'carplateNo',
            'iuNo',
            'manufacturer',
            'model',
            'capacity',
            'transType',
            'category',
            'tons']

    def clean_carplateNo(self):
        carplateNo = self.cleaned_data.get('carplateNo', '')
        if dbaccess.checkUniqueCarplateNo(carplateNo) is False:
            raise forms.ValidationError("Carplate Number already exist")
        return carplateNo

    def clean_iuNo(self):
        iuNo = self.cleaned_data.get('iuNo', '')
        if dbaccess.checkUniqueIuNo(iuNo) is False:
            raise forms.ValidationError("IU Number already exist")
        return iuNo

    def clean(self):
        cleaned_data = super(AddVehicleForm, self).clean()
        vehType = self.cleaned_data.get('vehType')
        category = self.cleaned_data.get('category')
        tons = self.cleaned_data.get('tons')

        if (vehType == 'c' and category != "sedan") and (vehType == 'c' and category != "mpv") and (vehType == 'c' and category != 'luxury'):
            msg = "Format: sedan/mpv/luxury"
            self._errors["category"] = self.error_class([msg])
        elif (vehType == 'b' and category != "bus") and (vehType == 'b' and category != "mini") and (vehType == 'b' and category != 'coach'):
            msg = "Format: mini/bus/coach"
            self._errors["category"] = self.error_class([msg])
        elif (vehType == 'l' and tons != 1) and (vehType == 'l' and tons != 3) and (vehType == 'l' and tons != 5):
            msg = "Format: 1/3/5"
            self._errors["tons"] = self.error_class([msg])
        return cleaned_data

    def clean_transType(self):
        transType = self.cleaned_data.get('transType', '')
        if transType != "manual" and transType != "auto":
            raise forms.ValidationError("Format: manual/auto")
        return transType
