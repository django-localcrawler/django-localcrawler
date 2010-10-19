from django.conf import settings
from django.conf.urls.defaults import handler500, handler404, patterns, include, \
    url
from django.contrib import admin
from testapp.views import RenderTemplate

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', RenderTemplate('index.html')),
    (r'(?P<template>.+?)/$', RenderTemplate()),
    (r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
)