from django.db import connection, transaction
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from admin.models import AddCompanyForm, AddDriverForm, AddVehicleForm, AddCarForm, AddBusForm, AddLorryForm


def registerCompany(request):
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            query = 'SELECT MAX(coyId) FROM Company'
            cursor.execute(query)
            row = cursor.fetchone()
            coyId = row[0]+1 if row[0] is not None else 1
            query = "INSERT INTO Company VALUES (%s,%s,%s,%s,%s,%s,%s)"
            params = [
                coyId,
                request.POST['coyName'],
                request.POST['email'],
                request.POST['faxNo'],
                request.POST['coyContactNo'],
                request.POST['zipcode'],
                request.POST['streetName']
            ]
            cursor.execute(query, params)
            transaction.commit_unless_managed()
            request.session['coyId'] = coyId
            return HttpResponseRedirect('/admin/addDriver')
    else:
        form = AddCompanyForm()
    return render_to_response('admin/addCompany.html', {
        'form': form
    }, context_instance=RequestContext(request))


def registerDriver(request):
    if request.method == 'POST':
        form = AddDriverForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            query = 'SELECT MAX(driverId) FROM Driver'
            cursor.execute(query)
            row = cursor.fetchone()
            driverId = row[0]+1 if row[0] is not None else 1
            query = "INSERT INTO Driver VALUES (%s,%s,%s,%s,%s,%s)"
            params = [
                driverId,
                request.POST['firstName'],
                request.POST['lastName'],
                request.POST['driverContactNo'],
                request.POST['drivingClass'],
                request.POST['coyId']
            ]
            cursor.execute(query,params)
            transaction.commit_unless_managed()
            request.session['coyId'] = request.POST['coyId']
            return HttpResponseRedirect('/admin/addDriver')
    else:
        form = AddDriverForm()
    return render_to_response('admin/addDriver.html', {
        'form': form
    }, context_instance=RequestContext(request))


def registerVehicle(request):
    if request.method == 'POST':
        form = AddVehicleForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            query = "INSERT INTO Vehicle VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = [
                request.POST['carplateNo'],
                request.POST['iuNo'],
                request.POST['manufacturer'],
                request.POST['model'],
                request.POST['capacity'],
                request.POST['drivingClass'],
                request.POST['transType'],
                request.POST['vehType'],
                request.POST['coyId']
            ]
            cursor.execute(query,params)
            transaction.commit_unless_managed()

            if request.POST['vehType'] == "c":
                query = "INSERT INTO CAR VALUES (%s,%s)"
                params = [
                    request.POST['carplateNo'],
                    request.POST['category']
                ]
                cursor.execute(query,params)
                transaction.commit_unless_managed()
            return HttpResponseRedirect('/admin/addVehicle')
    else:
        form = AddVehicleForm()
    return render_to_response('admin/addVehicle.html', {
        'form': form,
        'cform': AddCarForm,
        'bform': AddBusForm,
        'lform': AddLorryForm
    }, context_instance=RequestContext(request))