import dbaccess
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from analysis.models import AnalysisForm

def analyze(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        pass
    else:
        form = AnalysisForm()

    return render_to_response('analysis/options.html', {
        'form': form
    }, context_instance=RequestContext(request))