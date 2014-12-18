from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog.views import *
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', TemplateView.as_view(template_name="main_page.html")),
    (r'^login/$',login_page),
    (r'^register/$',register_page),
    (r'^logout/$',logout_page),
    (r'^$', main_page),
    (r'^main/$', main_page),
    (r'^list/$', list_page),
)
