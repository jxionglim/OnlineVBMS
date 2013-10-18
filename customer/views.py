from django.db import connection, transaction
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from customer.models import JobForm, companySearchForm
import datetime


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def addJob(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            query = 'SELECT MAX(jobId) FROM Job'
            cursor.execute(query)
            row = cursor.fetchone()
            jobId = row[0]+1 if row[0] is not None else 1
            cusId = 1
            query = "INSERT INTO Job VALUES (%s,%s,%s,%s,%s,%s)"
            params = [
                jobId,
                datetime.datetime.now().strftime("%Y-%m-%d"),
                cusId,
                request.POST['coyId'],
                request.POST['amount'],
                request.POST['paidStatus']
            ]
            cursor.execute(query,params)
            transaction.commit_unless_managed()
            return HttpResponseRedirect('/customer')
    else:
        form = JobForm()

    return render_to_response('customer/addJob.html', {
        'form': form
    }, context_instance=RequestContext(request))


def searchCompany(request):
    if request.method == 'POST':
        form = companySearchForm(request.POST)
        if form.is_valid():

            coyNames = request.POST['coyName']
            streetNames = request.POST['streetName']
            coyNameArray = coyNames.split(",")
            streetNameArray = streetNames.split(",")
            cursor = connection.cursor()
            query = "SELECT * FROM company WHERE "

            if coyNameArray:
                query = query + "(coyName LIKE "
                for x in coyNameArray:
                    query = query + "'%s' OR coyName LIKE " % (x)

                query = query[:-18] + "') AND "

            if streetNameArray:
                query = query + "(streetName LIKE "
                for x in streetNameArray:
                    query = query + "'%s' OR streetName LIKE " % (x)

                query = query[:-21] + "') AND "
            query = query[:-5]
            print query
            companyResult = cursor.execute(query)
            companyResultArray = dictfetchall(companyResult)
            #print companyResultArray

            request.session['companyResultArray'] = companyResultArray
            return HttpResponseRedirect('/customer/searchCompanyResults')
    else:
        form = companySearchForm()

    return render_to_response('customer/searchCompany.html', {
        'form': form
    }, context_instance=RequestContext(request))


def searchCompanyResults(request):
    return render_to_response('customer/searchCompanyResults.html', {
    }, context_instance=RequestContext(request))


def searchVehicle(request):
    if request.method == 'POST':
        form = companySearchForm(request.POST)
        if form.is_valid():

            coyNames = request.POST['coyName']
            streetNames = request.POST['streetName']
            coyNameArray = coyNames.split(",")
            streetNameArray = streetNames.split(",")
            cursor = connection.cursor()
            query = "SELECT * FROM company WHERE "

            if coyNameArray:
                query = query + "(coyName LIKE "
                for x in coyNameArray:
                    query = query + "'%s' OR coyName LIKE " % (x)

                query = query[:-18] + "') AND "

            if streetNameArray:
                query = query + "(streetName LIKE "
                for x in streetNameArray:
                    query = query + "'%s' OR streetName LIKE " % (x)

                query = query[:-21] + "') AND "
            query = query[:-5]
            print query
            companyResult = cursor.execute(query)
            companyResultArray = dictfetchall(companyResult)
            #print companyResultArray

            request.session['companyResultArray'] = companyResultArray
            return HttpResponseRedirect('/customer/searchVehicleResults')
    else:
        form = companySearchForm()

    return render_to_response('customer/searchVehicle.html', {
        'form': form
    }, context_instance=RequestContext(request))


def searchVehicleResults(request):
    return render_to_response('customer/searchVehicleResults.html', {
    }, context_instance=RequestContext(request))