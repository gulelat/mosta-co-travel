from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Hotels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^reserve/', include('reserve.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/mosta/PycharmProjects/Hotels/media',}),
    # url(r'^accounts/login/$',  login),
    # url(r'^accounts/logout/$', logout),
    # url(r'^polls/',include('polls.urls')),
)
