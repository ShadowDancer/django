from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import *
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', redirect_page),
    (r'^login/$',login_page),
    (r'^register/$',register_page),
    (r'^logout/$',logout_page),
    (r'^/$', redirect_page),
    (r'^account/$', account_page),
    (r'^transfer/$', transfer_page),
    (r'^list/$', list_page),
)
