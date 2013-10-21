from django.conf.urls import *

urlpatterns = patterns('customer.views',
    (r'^$', 'addJob'),
    (r'^addJob$', 'addJob'),
    (r'^searchCompany$', 'searchCompany'),
    (r'^searchCompanyResults$', 'searchCompanyResults'),
    (r'^searchVehicle$', 'searchVehicle$'),
    (r'^searchVehicleResults$', 'searchVehicleResults$'),
)
