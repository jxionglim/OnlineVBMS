import dbaccess, urlparse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from admin.models import AddCompanyForm, AddDriverForm, AddVehicleForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def registerCompany(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
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

@csrf_exempt
def registerDriver(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    status = 'normal'
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
                request.session['coyId']
            ]
            dbaccess.insertDriver(params)
            if request.get_full_path().__contains__('id'):
                return HttpResponseRedirect('/admin/addDriver/id='+str(request.session['coyId']))
            else:
                return HttpResponseRedirect('/admin/addDriver')
    else:
        form = AddDriverForm()
        if request.get_full_path().__contains__('id'):
            request.session['coyId'] = request.get_full_path().split('=')[1]
            status = 'redirect'
        else:
            if 'coyId' not in request.session:
                return HttpResponseRedirect('/home')
        print(status)
    if 'coyId' in request.session:
        coyId = request.session['coyId']
    else:
        coyId = None
    return render_to_response('admin/addDriver.html', {
        'form': form,
        'status': status,
        'coyId': coyId
    }, context_instance=RequestContext(request))

@csrf_exempt
def registerVehicle(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    status = 'normal'
    if request.method == 'POST':
        form = AddVehicleForm(request, request.POST)
        if form.is_valid():
            drivingclass = None
            transType = None
            if request.POST['vehType'] == 'c':
                if request.POST['transType'] == 'manual':
                    drivingclass = '3'
                    transType = 'manual'
                else:
                    drivingclass = '3a'
                    transType = 'auto'
            elif request.POST['vehType'] == 'b':
                if request.POST['transType'] == 'manual':
                    drivingclass = '4'
                    transType = 'manual'
                else:
                    drivingclass = '4a'
                    transType = 'auto'
            elif request.POST['vehType'] == 'l':
                if request.POST['tons'] == '1':
                    drivingclass = '3'
                    transType = 'manual'
                elif request.POST['tons'] == '3':
                    drivingclass = '4'
                    transType = 'manual'
                elif request.POST['tons'] == '5':
                    drivingclass = '5'
                    transType = 'manual'
            params = [
                request.POST['carplateNo'],
                request.POST['iuNo'],
                request.POST['manufacturer'],
                request.POST['model'],
                request.POST['capacity'],
                drivingclass,
                transType,
                request.POST['vehType'],
                request.session['coyId']
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
            if request.get_full_path().__contains__('id'):
                return HttpResponseRedirect('/admin/addVehicle/id='+str(request.session['coyId']))
            else:
                return HttpResponseRedirect('/admin/addVehicle')
    else:
        form = AddVehicleForm(request)
        if request.get_full_path().__contains__('id'):
            request.session['coyId'] = request.get_full_path().split('=')[1]
            status = 'redirect'
        else:
            if 'coyId' not in request.session:
                return HttpResponseRedirect('/home')
    if 'coyId' in request.session:
        coyId = request.session['coyId']
    else:
        coyId = None
    return render_to_response('admin/addVehicle.html', {
        'form': form,
        'status': status,
        'coyId': coyId
    }, context_instance=RequestContext(request))

@csrf_exempt
def viewCompany(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    if 'coyId' in request.session:
        del request.session['coyId']
    allCoy = dbaccess.getCompanies()
    return render_to_response('admin/viewCompany.html', {
        'allCoy': allCoy
    }, context_instance=RequestContext(request))

@csrf_exempt
def viewDriver(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    if 'coyId' in request.session:
        del request.session['coyId']
    coyId = request.get_full_path().split('=')[1]
    drivers = dbaccess.getDriversById(request.get_full_path().split('=')[1])
    return render_to_response('admin/viewDriver.html', {
        'drivers': drivers,
        'coyId': coyId
    }, context_instance=RequestContext(request))

@csrf_exempt
def viewVehicle(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    if 'coyId' in request.session:
        del request.session['coyId']
    coyId = request.get_full_path().split('=')[1]
    cars = dbaccess.getCarsById(request.get_full_path().split('=')[1])
    buses = dbaccess.getBusesById(request.get_full_path().split('=')[1])
    lorries = dbaccess.getLorriesById(request.get_full_path().split('=')[1])
    return render_to_response('admin/viewVehicle.html', {
        'cars': cars,
        'buses': buses,
        'lorries': lorries,
        'coyId': coyId,
        'carStatus': True if len(cars) != 0 else False,
        'busStatus': True if len(buses) != 0 else False,
        'lorryStatus': True if len(lorries) != 0 else False
    }, context_instance=RequestContext(request))

@csrf_exempt
def editCompany(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    coyRow = dbaccess.getCompanyById(request.get_full_path().split('=')[1])
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            params = [
                request.POST['coyName'],
                request.POST['email'],
                request.POST['faxNo'],
                request.POST['coyContactNo'],
                request.POST['zipcode'],
                request.POST['streetName'],
                coyRow[0]
            ]
            dbaccess.updateCompany(params)
            return HttpResponseRedirect('/admin/viewCompany')
    else:
        form = AddCompanyForm(initial={
            'coyName': coyRow[1],
            'email': coyRow[2],
            'faxNo': coyRow[3],
            'coyContactNo': coyRow[4],
            'zipcode': coyRow[5],
            'streetName': coyRow[6],
        })
    return render_to_response('admin/editCompany.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@csrf_exempt
def editDriver(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    driverRow = dbaccess.getDriverByDid(request.get_full_path().split('=')[1])
    if request.method == 'POST':
        form = AddDriverForm(request.POST)
        if form.is_valid():
            params = [
                request.POST['firstName'],
                request.POST['lastName'],
                request.POST['driverContactNo'],
                request.POST['drivingClass'],
                driverRow[0]
            ]
            dbaccess.updateDriver(params)
            return HttpResponseRedirect('/admin/viewDriver/id=' + str(driverRow[5]))
    else:
        form = AddDriverForm(initial={
            'firstName': driverRow[1],
            'lastName': driverRow[2],
            'driverContactNo': driverRow[3],
            'drivingClass': driverRow[4],
        })
    return render_to_response('admin/editDriver.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@csrf_exempt
def deleteCompany(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    dbaccess.deleteCompany(request.get_full_path().split('=')[1])
    return HttpResponseRedirect('/admin/viewCompany')

@csrf_exempt
def deleteDriver(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    coyId = dbaccess.getDriverByDid(request.get_full_path().split('=')[1])[5]
    dbaccess.deleteDriver(request.get_full_path().split('=')[1])
    return HttpResponseRedirect('/admin/viewDriver/id=' + str(coyId))

@csrf_exempt
def deleteVehicle(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home')
    coyId = dbaccess.getCoyIdByCarplateNo(request.get_full_path().split('=')[1])
    dbaccess.deleteVehicle(request.get_full_path().split('=')[1])
    return HttpResponseRedirect('/admin/viewVehicle/id=' + str(coyId))