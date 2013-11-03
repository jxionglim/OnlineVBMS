import dbaccess
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from analysis.models import allTripCondForm, driverActivityForm, numJobNAmtForm, custDistForm, coyJoblessForm


def analyze(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        currentReq = int(request.get_full_path().split("/")[2])
        if currentReq == 1:
            form = allTripCondForm(request.POST)
            if form.is_valid():
                tripInfo = dbaccess.getTripsByLocation(request.POST['startLocation'], request.POST['endLocation'], request.POST['qty'], request.POST['period'])
                return render_to_response('analysis/result1.html', {
                    'startLoc': request.POST['startLocation'] if request.POST['startLocation'] != "a" else "anywhere",
                    'endLoc': request.POST['endLocation'] if request.POST['endLocation'] != "e" else "everywhere",
                    'qty': request.POST['qty'],
                    'period': request.POST['period'],
                    'tripInfo': tripInfo,
                }, context_instance=RequestContext(request))
        if currentReq == 2:
            form = coyJoblessForm(request.POST)
            if form.is_valid():
                joblessCoy = dbaccess.getJoblessCoy(request.POST['qty'], request.POST['period'])
                return render_to_response('analysis/result2.html', {
                    'qty': request.POST['qty'],
                    'period': request.POST['period'],
                    'joblessCoy': joblessCoy,
                }, context_instance=RequestContext(request))
        if currentReq == 3:
            form = numJobNAmtForm(request.POST)
            if form.is_valid():
                jobAmt = dbaccess.getJobAmtByCoy(request.POST['order'], request.POST['qty'], request.POST['period'])
                return render_to_response('analysis/result3.html', {
                    'qty': request.POST['qty'],
                    'period': request.POST['period'],
                    'jobAmt': jobAmt,
                }, context_instance=RequestContext(request))
        if currentReq == 4:
            form = custDistForm(request.POST)
            if form.is_valid():
                coyCust = dbaccess.getCusDistribution(request.POST['order'])
                return render_to_response('analysis/result4.html', {
                    'coyCust': coyCust,
                }, context_instance=RequestContext(request))
        if currentReq == 5:
            form = driverActivityForm(request.POST)
            if form.is_valid():
                numVeh = dbaccess.getNumVehByCatByCoy(request.POST['company'])
                numDriv = dbaccess.getNumDriByClassByCoy(request.POST['company'])
                company = dbaccess.getCoyInfoByCoyId(request.POST['company'])
                return render_to_response('analysis/result5.html', {
                    'numVeh': numVeh,
                    'numDriv': numDriv,
                    'company': company,
                }, context_instance=RequestContext(request))
    return render_to_response('analysis/options.html', {
        'allTripCond': allTripCondForm(),
        'driverActivity': driverActivityForm(),
        'numJobNAmt': numJobNAmtForm(),
        'custDist': custDistForm(),
        'coyJobless': coyJoblessForm()
    }, context_instance=RequestContext(request))