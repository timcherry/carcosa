from django.conf.urls import patterns, include, url

from django.contrib import admin
from qrap.postapi import PostAPI

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carcosa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^api', PostAPI.as_view(), name='post-view'),
)
