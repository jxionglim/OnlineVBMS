from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'userprofile.views.login'),
    (r'^home$', 'customer.views.searchCompanyByLocation'),
    (r'^searchVehicleAmt$', 'customer.views.searchCompanyByVehicle'),
    (r'^searchVehicleType$', 'customer.views.searchCompanyByVehicleAmt'),
    (r'^logout$', 'userprofile.views.logout'),
    (r'^register$', 'userprofile.views.register'),
    (r'^viewCompanyProfile/id=\d+?$', 'admin.views.viewCompanyProfile'),
    (r'^customer/', include('customer.urls')),
    (r'^user/', include('userprofile.urls')),
    (r'^admin/', include('admin.urls')),
    (r'^analysis/', include('analysis.urls')),
    )

handler404 = 'error.views.my_404_view'
handler500 = 'error.views.my_505_view'