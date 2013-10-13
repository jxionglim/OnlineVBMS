from django.db import connection
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from userprofile.models import RegisterForm

# Create your views here.
def register(request):
	return render_to_response('userprofile/register.html', {
		'form' : RegisterForm(),
		},context_instance=RequestContext(request))
		
def viewProfile(request):
	return render_to_response('userprofile/register.html', {
		'form' : RegisterForm(),
		},context_instance=RequestContext(request))