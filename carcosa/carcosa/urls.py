from django.conf.urls import patterns, include, url

from django.contrib import admin
from qrap.postapi import PostAPI, Reveal
from qrap.front import Front, Company

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carcosa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^post', PostAPI.as_view(), name='post-view'),
    url(r'^reveal', Reveal.as_view(), name='reveal-view'),
    url(r'^c/(?P<company>\w+)', Company.as_view(), name='company-view'),
    url(r'', Front.as_view(), name='post-view')
)
