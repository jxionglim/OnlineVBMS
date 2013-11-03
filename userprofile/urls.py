from django.conf.urls import *

urlpatterns = patterns('userprofile.views',
    (r'^$', 'viewProfile'),
    (r'^edit$', 'editProfile'),
    (r'^addAdmin$', 'addAdmin'),
)
