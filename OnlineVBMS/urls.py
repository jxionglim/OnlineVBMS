from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	(r'^register$', 'userprofile.views.register'),
	(r'^user/', include('userprofile.urls')),
)
