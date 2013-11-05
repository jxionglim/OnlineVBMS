from django.conf.urls import *

urlpatterns = patterns('customer.views',
    (r'^addJob$', 'addJob'),
    (r'^addTrip$', 'addTrip'),
    (r'^viewJobs$', 'viewJobs'),
    (r'^viewJobs/j_id=\d+?$', 'viewTripsOfJob'),
    (r'^viewTrip/d_id=\d+?$', 'deleteTripOfJob'),
    (r'^viewTrip/e_id=\d+?&&c_id=\d+?$', 'editTripOfJob'),
    (r'^searchCompanyByLocation$', 'searchCompanyByLocation'),
    (r'^searchCompanyByVehicle$', 'searchCompanyByVehicle'),
    (r'^searchCompanyByVehicleAmt$', 'searchCompanyByVehicleAmt'),
)
