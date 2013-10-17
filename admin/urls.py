from django.conf.urls import patterns, include, url

from admin import views

urlpatterns = patterns('',
    (r'^$', views.register, name='register')
)
