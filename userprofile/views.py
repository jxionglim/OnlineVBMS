import dbaccess
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from userprofile.models import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.utils.datastructures import SortedDict


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['email'], None, request.POST['passwd'])
            user.save()
            print dbaccess.getMaxCustomerId()
            cusId = dbaccess.getMaxCustomerId()+1
            params = [
                cusId,
                request.POST['firstName'],
                request.POST['lastName'],
                request.POST['email'],
                request.POST['contactNo'],
                request.POST['zipcode'],
                request.POST['streetName'],
                request.POST['cExpDate'],
                request.POST['cSerialNo'],
                request.POST['passwd'],
                user.id
            ]
            dbaccess.insertCustomer(params)
            return HttpResponseRedirect('/register')
    else:
        form = RegisterForm()

    return render_to_response('userprofile/register.html', {
        'form': form
    }, context_instance=RequestContext(request))


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/home')
    else:
        form = LoginForm(request)

    return render_to_response('userprofile/login.html', {
        'form': form,
        }, context_instance=RequestContext(request))


def viewProfile(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
        return HttpResponseRedirect('/')
    cusId = dbaccess.getCustIdByUserId(request.user.id)
    custRow = dbaccess.getCustInfoById(cusId)
    custInfo = SortedDict([
        ('Email', custRow[3]),
        ('First Name', custRow[1]),
        ('Last Name', custRow[2]),
        ('Street Name', custRow[6]),
        ('Postal Code', custRow[5]),
        ('Contact Number', custRow[4]),
        ])
    custCredit = SortedDict([
        ('Serial Number', custRow[8]),
        ('Expiry Date', custRow[7])
        ])
    return render_to_response('userprofile/viewProfile.html', {
        'custInfo': custInfo.iteritems(),
        'custCredit': custCredit.iteritems(),
        }, context_instance=RequestContext(request))


def editProfile(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
        return HttpResponseRedirect('/')
    cusId = dbaccess.getCustIdByUserId(request.user.id)
    custRow = dbaccess.getCustInfoById(cusId)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            params = [
                request.POST['firstName'],
                request.POST['lastName'],
                request.POST['contactNo'],
                request.POST['zipcode'],
                request.POST['streetName'],
                request.POST['cExpDate'],
                request.POST['cSerialNo'],
                cusId
            ]
            dbaccess.updateCustomer(params)
            return HttpResponseRedirect('/user')
    else:
        form = ProfileForm(initial={
            'firstName': custRow[1],
            'lastName': custRow[2],
            'contactNo': custRow[4],
            'streetName': custRow[6],
            'zipcode': custRow[5],
            'cSerialNo': custRow[8],
            'cExpDate': custRow[7],
        })
    return render_to_response('userprofile/editProfile.html', {
        'form': form,
        }, context_instance=RequestContext(request))


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login')