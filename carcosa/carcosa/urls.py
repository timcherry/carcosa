from django.conf.urls import patterns, include, url

from django.contrib import admin
from qrap import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carcosa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', views.index, name='index'),
)
