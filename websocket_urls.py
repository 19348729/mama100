__author__ = 'DELL'
from django.conf.urls import patterns, url
from mama100.cmdb.webssh import *
urlpatterns = patterns('',
    url(r'^wssh/$', webssh_connect),
)