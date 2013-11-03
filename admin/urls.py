from django.conf.urls import *

urlpatterns = patterns('admin.views',
    (r'^addCompany$', 'registerCompany'),
    (r'^addDriver$', 'registerDriver'),
    (r'^addDriver/id=\d+?$', 'registerDriver'),
    (r'^addVehicle$', 'registerVehicle'),
    (r'^addVehicle/id=\d+?$', 'registerVehicle'),
    (r'^viewCompany$', 'viewCompany'),
    (r"^editCompany/id=\d+?$", 'editCompany'),
    (r'^deleteCompany/id=\d+?$', 'deleteCompany'),
    (r'^viewDriver/id=\d+?$', 'viewDriver'),
    (r'^editDriver/d_id=\d+?$', 'editDriver'),
    (r'^deleteDriver/d_id=\d+?$', 'deleteDriver'),
    (r'^viewVehicle/id=\d+?$', 'viewVehicle'),
    (r'^deleteVehicle/v_id=\d+?$', 'deleteVehicle'),
)