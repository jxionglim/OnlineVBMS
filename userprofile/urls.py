from django.conf.urls.defaults import *

urlpatterns = patterns('userprofile.views',
    (r'^$', 'viewProfile'),
)
