import dbaccess
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from admin.models import AddCompanyForm, AddDriverForm, AddVehicleForm, AddCarForm, AddBusForm, AddLorryForm
from django.db import connection, transaction


def registerCompany(request):
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            coyId = dbaccess.getMaxCompanyId()+1
            params = [
                coyId,
                request.POST['coyName'],
                request.POST['email'],
                request.POST['faxNo'],
                request.POST['coyContactNo'],
                request.POST['zipcode'],
                request.POST['streetName']
            ]
            dbaccess.insertCompany(params)
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
            driverId = dbaccess.getMaxDriverId()+1
            params = [
                driverId,
                request.POST['firstName'],
                request.POST['lastName'],
                request.POST['driverContactNo'],
                request.POST['drivingClass'],
                request.POST['coyId']
            ]
            dbaccess.insertDriver(params)
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
            dbaccess.insertVehicle(params)

            if request.POST['vehType'] == "c":
                params = [
                    request.POST['carplateNo'],
                    request.POST['category']
                ]
                dbaccess.insertCar(params)
            elif request.POST['vehType'] == "b":
                params = [
                    request.POST['carplateNo'],
                    request.POST['category']
                ]
                dbaccess.insertBus(params)
            elif request.POST['vehType'] == "l":
                params = [
                    request.POST['carplateNo'],
                    request.POST['tons']
                ]
                dbaccess.insertLorry(params)
            return HttpResponseRedirect('/admin/addVehicle')
    else:
        form = AddVehicleForm()
    return render_to_response('admin/addVehicle.html', {
        'form': form,
        'cform': AddCarForm,
        'bform': AddBusForm,
        'lform': AddLorryForm
    }, context_instance=RequestContext(request))