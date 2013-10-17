from django.conf.urls import patterns, url

from admin import views

urlpatterns = patterns('',
    url(r'^$', views.register, name='register')
)