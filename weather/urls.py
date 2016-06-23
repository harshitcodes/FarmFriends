from django.conf.urls import include, url

urlpatterns = [
	url(r'^$', 'weather.views.get_weather',name='get_weather'),

]