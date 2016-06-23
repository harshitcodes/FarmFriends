# third party stuff

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db.models import Q


# weather and location based api
import googlemaps
import forecastio
from datetime import datetime

from .forms import *

# Create your views here.


gmaps_api_key = 'AIzaSyDzkw5vTEuq5xK_iaqpWrMnkaVwYNWqekc'
forecast_api_key = '5723f2e50a02af7c0b467d5c8e58c21e'

@require_http_methods(['GET', 'POST'])
def get_weather(request):
	if request.method == "GET":
		f = LocationForm(request.GET)
		if f.is_valid():
			# print(f)
			# instance = f.save(commit = False)
			location = f.cleaned_data['location']
			print(location)
			gmaps = googlemaps.Client(gmaps_api_key)
			geocode_result = gmaps.geocode(str(location))
			lng = geocode_result[0]['geometry']['location']['lng']
			lat = geocode_result[0]['geometry']['location']['lat']
			current_time = datetime.now()
			forecast = forecastio.load_forecast(forecast_api_key, lat, lng,current_time)
			byhour = forecast.hourly()
			summary = byhour.summary
			temp = byhour.data[0].temperature
			print(temp)
			precipitation = byhour.data[0].precipProbability
			icon = byhour.data[0].icon
			context = {'summary' : summary, 'temp' : temp, 'precip' : precipitation, 'icon' : icon}
			return render(request, 'weather/weather_rendering.html', context)
	return render(request, 'weather/weather.html', {'form' : f})

