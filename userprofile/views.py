import dbaccess
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from userprofile.models import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['email'], None, request.POST['passwd'])
            user.save()
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render_to_response('userprofile/viewProfile.html', {
        'form': 'asd',
        }, context_instance=RequestContext(request))


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login')