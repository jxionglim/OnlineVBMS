from django.db import connection, transaction
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from customer.models import JobForm
import datetime



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
