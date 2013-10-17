from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'userprofile.views.login'),
<<<<<<< HEAD
    (r'^register$', 'userprofile.views.register'),
    (r'^customer/', include('customer.urls')),
    (r'^user/', include('userprofile.urls')),
=======
	(r'^register$', 'userprofile.views.register'),
	(r'^user/', include('userprofile.urls')),
    (r'^admin/', include('admin.urls')),
>>>>>>> 6b4e8a0fc751403b6fe8771f3570c441986ab33e
)
