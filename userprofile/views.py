from django.db import connection, transaction
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from userprofile.models import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            query = 'SELECT MAX(cusId) FROM customer'
            cursor.execute(query)
            row = cursor.fetchone()
            cusId = row[0]+1 if row[0] is not None else 1
            query = "INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
                request.POST['password']
            ]
            cursor.execute(query, params)
            transaction.commit_unless_managed()
            return HttpResponseRedirect('/register')
    else:
        form = RegisterForm()

    return render_to_response('userprofile/register.html', {
        'form': form
    }, context_instance=RequestContext(request))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            query = "SELECT count(*) FROM customer WHERE email=%s AND password=%s"
            params = [
                request.POST['email'],
                request.POST['password'],
            ]
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row[0] == 1:
                return HttpResponseRedirect('/home')
    else:
        form = LoginForm()

    return render_to_response('userprofile/login.html', {
        'form' : form,
        },context_instance=RequestContext(request))