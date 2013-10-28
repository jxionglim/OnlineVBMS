from django.conf.urls import *

urlpatterns = patterns('customer.views',
    (r'^$', 'addJob'),
    (r'^addJob$', 'addJob'),
    (r'^addTrip$', 'addTrip'),
    (r'^viewJobs$', 'viewJobs'),
    (r'^viewJobs/j_id=\d+?$', 'viewTripsOfJob'),
    (r'^viewTrip/d_id=\d+?$', 'deleteTripOfJob'),
    (r'^viewTrip/e_id=\d+?$', 'editTripOfJob'),
    (r'^searchCompany$', 'searchCompany'),
    (r'^searchCompanyResults$', 'searchCompanyResults'),
    (r'^searchVehicle$', 'searchVehicle'),
    (r'^searchVehicleResults$', 'searchVehicleResults')
)
