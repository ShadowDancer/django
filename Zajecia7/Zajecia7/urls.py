from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import *
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Zajecia7.views.home', name='home'),
    url(r'^blog/', include('blog.urls')),
    (r'^$', redirect_page ),
)
