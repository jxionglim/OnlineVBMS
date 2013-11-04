from django.conf.urls import *

urlpatterns = patterns('analysis.views',
    (r'^$', 'analyze'),
    (r'^1$', 'analyze'),
    (r'^2$', 'analyze'),
    (r'^3$', 'analyze'),
    (r'^4$', 'analyze'),
)
