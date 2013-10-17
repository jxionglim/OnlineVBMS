from django.db import connection, transaction
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from admin.models import AddCompanyForm, AddDriverForm, AddVehicleForm

def register(request):
    if request.method == 'POST':
        cform = AddCompanyForm(request.POST)
        dform = AddDriverForm(request.POST)
        vform = AddVehicleForm(request.POST)
        if cform.is_valid() and dform.is_valid() and vform.is_valid():
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
                request.POST['driverClass'],
                coyId
            ]
            cursor.execute(query, params)
            transaction.commit_unless_managed()

            """query = "INSERT INTO Vehicle VALUES (%s,%s,%s,%s,%s,%s,%s)"
            params = [
                request.POST['carplateNo'],
                request.POST['iuNo'],
                request.POST['manufacturer'],
                request.POST['model'],
                request.POST['transType'],
                request.POST['driverClass'],
                request.POST['capacity'],
            ]
            cursor.execute(query, params)
            transaction.commit_unless_managed()"""
            return HttpResponseRedirect('/admin')
    else:
        cform = AddCompanyForm()
        dform = AddDriverForm()
        vform = AddVehicleForm()
    return render_to_response('admin/addCompany.html', {
    'cform': cform,
    'dform': dform,
    'vform': vform
    }, context_instance=RequestContext(request))

