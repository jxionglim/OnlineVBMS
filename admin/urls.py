from django.conf.urls import patterns, url
from admin import views

urlpatterns = patterns('',
    (r'^$', views.register)
)