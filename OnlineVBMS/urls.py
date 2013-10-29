from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'userprofile.views.login'),
    (r'^home$', 'userprofile.views.home'),
    (r'^logout$', 'userprofile.views.logout'),
    (r'^register$', 'userprofile.views.register'),
    (r'^customer/', include('customer.urls')),
    (r'^user/', include('userprofile.urls')),
    (r'^admin/', include('admin.urls')),
    (r'^analysis/', include('analysis.urls')),
    )

