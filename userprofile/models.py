import re
import dbaccess
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def validateBlank(value):
    if len(value.strip()) == 0:
        raise forms.ValidationError("This field is required.")
    return value


class Customer(models.Model):
    cusId = models.BigIntegerField()
    email = models.EmailField(max_length=256)
    passwd = models.CharField(max_length=256)
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    contactNo = models.BigIntegerField()
    streetName = models.CharField(max_length=256)
    zipcode = models.BigIntegerField()
    cSerialNo = models.BigIntegerField()
    cExpDate = models.CharField(max_length=5)
    user = models.OneToOneField(User)

    class Meta:
        managed = False

    """@classmethod
    def create(cls, cusId, firstName, lastName, email, contactNo, zipcode, streetName, cExpDate, cSerialNo, passwd, user):
        cust = cls(cusId=cusId,
                   email=email,
                   passwd=passwd,
                   firstName=firstName,
                   lastName=lastName,
                   contactNo=contactNo,
                   streetName=streetName,
                   zipcode=zipcode,
                   cSerialNo=cSerialNo,
                   cExpDate=cExpDate,
                   user=user)
        return cust"""


class RegisterForm(ModelForm):
    email = forms.EmailField(max_length=256, label="Email")
    passwd = forms.CharField(widget=forms.PasswordInput(), max_length=256, label="Password", min_length=8)
    firstName = forms.CharField(max_length=256, label="First Name", validators=[validateBlank])
    lastName = forms.CharField(max_length=256, label="Last Name", validators=[validateBlank])
    contactNo = forms.IntegerField(label="Contact Number")
    streetName = forms.CharField(max_length=256, label="Street Name", required=False)
    zipcode = forms.IntegerField(label="Postal Code", required=False)
    cSerialNo = forms.IntegerField(label="Serial Number")
    cExpDate = forms.CharField(max_length=5, label="Expiry Date", help_text="Format: mm/yy")

    class Meta:
        model = Customer
        exclude = ('user', 'cusId')

    def clean_cExpDate(self):
        cExpDate = self.cleaned_data.get('cExpDate', '')
        if re.search('^(0[1-9]|1[012])/\d\d$',cExpDate) == None:
            raise forms.ValidationError("Enter a valid expiry date")
        return cExpDate

    def clean_contactNo(self):
        contactNo = self.cleaned_data.get('contactNo', '')
        if re.search('^(9|8|6)\d{7}$',str(contactNo)) == None:
            raise forms.ValidationError("Contact number must be a 8 digit number starting with 8 or 9")
        return contactNo

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode', '')
        if zipcode is not None:
            if re.search('^\d{6}$',str(zipcode)) == None:
                raise forms.ValidationError("Postal code must be a 6 digit number")
        return zipcode


class ProfileForm(ModelForm):
    firstName = forms.CharField(max_length=256, label="First Name", validators=[validateBlank])
    lastName = forms.CharField(max_length=256, label="Last Name", validators=[validateBlank])
    contactNo = forms.IntegerField(label="Contact Number")
    streetName = forms.CharField(max_length=256, label="Street Name", required=False)
    zipcode = forms.IntegerField(label="Postal Code", required=False)
    cSerialNo = forms.IntegerField(label="Serial Number")
    cExpDate = forms.CharField(max_length=5, label="Expiry Date", help_text="Format: mm/yy")

    class Meta:
        model = Customer
        exclude = ('user', 'cusId', 'passwd', 'email')

    def clean_cExpDate(self):
        cExpDate = self.cleaned_data.get('cExpDate', '')
        if re.search('^(0[1-9]|1[012])/\d\d$',cExpDate) == None:
            raise forms.ValidationError("Enter a valid expiry date")
        return cExpDate

    def clean_contactNo(self):
        contactNo = self.cleaned_data.get('contactNo', '')
        if re.search('^(9|8|6)\d{7}$',str(contactNo)) == None:
            raise forms.ValidationError("Contact number must be a 8 digit number starting with 8 or 9")
        return contactNo

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode', '')
        if zipcode is not None:
            if re.search('^\d{6}$',str(zipcode)) == None:
                raise forms.ValidationError("Postal code must be a 6 digit number")
        return zipcode


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=256, label="Email")
    password = forms.CharField(max_length=256, widget=forms.PasswordInput, label="Password", min_length=8)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            valid = dbaccess.validateCustomer([email, password])
            if valid:
                user = authenticate(username=email, password=password)
                login(self.request, user)
            else:
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(self.request, user)
                else:
                    raise forms.ValidationError("Invalid credientials")
        return cleaned_data