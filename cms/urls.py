from django.conf.urls import include, url

urlpatterns = [
	url(r'^signup/$', 'cms.views.signup',name='signup'),
	url(r'^login/$', 'cms.views.login',name='login'),
	url(r'^logout/$', 'cms.views.logout',name='logout'),
	url(r'^activate/(?P<uid>\d+)/(?P<token>[0-9A-Za-z_\-]+)/$', 'cms.views.activate',\
	 name='activate'),
	url(r'^home/$', 'cms.views.home',name='home'),

]