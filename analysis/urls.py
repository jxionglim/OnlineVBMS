from django.conf.urls import *

urlpatterns = patterns('analysis.views',
    (r'^$', 'analyze'),
)
