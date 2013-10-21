from django.conf.urls import *

urlpatterns = patterns('admin.views',
    (r'^addCompany$', 'registerCompany'),
    (r'^addDriver$', 'registerDriver'),
    (r'^addVehicle$', 'registerVehicle'),
)