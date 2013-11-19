# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from registration.forms import RegistrationFormUniqueEmail
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^settings/', include('livesettings.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^$', views.home),
    url(r'^contacts/$', views.contacts),
    url(r'^about/$', views.about),
    url(r'^participate/$', views.participate),
    url(r'^projects/$', views.projects),
    url(r'^projects/(?P<slug>[\w-]+)/$$', views.projects_nomination),
    url(r'^project/$', views.edit_project),
    url(r'^del_project/$', views.del_project),
    url(r'^project/(?P<slug>[\w-]+)/$' , views.project),
    url(r'^news/$', views.news),
    url(r'^news/(?P<slug>[\w-]+)/$' , views.news_article),
    url(r'^comments/$', views.comments),
    url(r'^search/$', views.search),
    url(r'^user/(?P<username>[\w-]+)/$' , views.user),
    url(r'^jury/$', views.jury),
    url(r'^profile/$', views.profile),
    url(r'^seminars/$', views.seminars),
    url(r'^seminar/(?P<slug>[\w-]+)/$' , views.seminar),
    url(r'^partners/$', views.partners),
    #url(r'^registration/$', views.registration),

    url(r'^login/$', views.login),
    
    url(r'^ulogin/', include('django_ulogin.urls')),
    url(r'^logout/',  'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/register/$', 'registration.views.register',
    {'form_class': RegistrationFormUniqueEmail,
     'backend': 'registration.backends.default.DefaultBackend'},       
     name='registration_register'),
    url(r'^accounts/', include('registration.urls')),
    
    url(r'^(?P<page_name>[\w-]+)/$' , views.page),
    
)
