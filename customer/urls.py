from django.conf.urls import *

urlpatterns = patterns('customer.views',
    (r'^$', 'addJob'),
    (r'^addJob$', 'addJob'),
    (r'^addTrip$', 'addTrip'),
    (r'^viewJobs$', 'viewJobs'),
    (r'^viewJobs/j_id=\d+?$', 'viewTripsOfJob'),
    (r'^viewTrip/d_id=\d+?$', 'deleteTripOfJob'),
    (r'^viewTrip/e_id=\d+?$', 'editTripOfJob'),
    (r'^searchCompanyByLocation$', 'searchCompanyByLocation'),
    (r'^searchCompanyByLocationResults$', 'searchCompanyByLocationResults'),
    (r'^searchCompanyByVehicle$', 'searchCompanyByVehicle'),
    (r'^searchCompanyByVehicleResults$', 'searchCompanyByVehicleResults'),
    (r'^searchCompanyByVehicleAmt$', 'searchCompanyByVehicleAmt'),
    (r'^searchCompanyByVehicleAmtResults$', 'searchCompanyByVehicleAmtResults')
)
