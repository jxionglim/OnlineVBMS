from django.conf.urls import *

urlpatterns = patterns('userprofile.views',
    (r'^$', 'viewProfile'),
    (r'^id=\d+?$', 'viewProfile'),
    (r'^edit$', 'editProfile'),
    (r'^addAdmin$', 'addAdmin'),
)
