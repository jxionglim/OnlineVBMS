from django.shortcuts import render_to_response
from django.template import RequestContext


def my_404_view(request):
    return render_to_response('error/404_error.html', {
    }, context_instance=RequestContext(request))


def my_505_view(request):
    return render_to_response('error/500_error.html', {
    }, context_instance=RequestContext(request))