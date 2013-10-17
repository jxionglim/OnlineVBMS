from django.conf.urls import *

urlpatterns = patterns('customer.views',
    (r'^$', 'addJob'),
)
