__author__ = 'mosta'
from django.conf.urls import patterns, url
from reserve import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^hotel/$', views.hotel, name='hotel'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.login_view, name='login'),
                       url(r'^reservation/$', views.reservation, name='reservation'),
                       url(r'^reservation1/$', views.reservation1, name='reservation1'),
                       url(r'^result/$', views.result, name='result'),
                       url(r'^booking/$', views.booking, name='booking'),
                       url(r'^confirm/$', views.confirm, name='confirm'),
                       url(r'^finishing/$', views.finishing, name='finishing'),
                       url(r'^offer_month/$', views.offer_month, name='offer_month'),
                       url(r'^offer_all/$', views.offer_all, name='offer_all'),
                       url(r'^hotel_view/$', views.hotel_view, name='hotel_view'),
                       # url(r'^$', views.index, name='index'),
	                   # url(r'^Question/(?P<poll_id>\d+)/$', views.Question, name='choice'),
                       )