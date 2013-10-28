from django.conf.urls import *

urlpatterns = patterns('analysis.views',
    (r'^$', 'viewProfile'),
    (r'^edit$', 'editProfile'),
)
