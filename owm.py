import json
from datetime import datetime, timezone, timedelta

import requests

from utils import lon, lat, token_owm


class WeatherForecast:
    def __init__(self, latitude, longitude, appid):
        self.weather_forecast = None

        self.latitude = latitude
        self.longitude = longitude
        self.appid = appid
        self.units = 'metric'

        self.params = {'lat': self.latitude,
                       'lon': self.longitude,
                       'appid': self.appid,
                       'units': self.units}

        self.timezone = None

        self.get_forecast_from_owm()

    def get_forecast_from_owm(self):
        weather_endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
        response = requests.get(weather_endpoint, params=self.params)
        if response.status_code == 200:
            self.weather_forecast = response.json()
            timezone_offset = self.weather_forecast['timezone_offset']
            self.timezone = timezone(timedelta(seconds=timezone_offset))
        else:
            raise ValueError('Status code is not 200')

    def convert_timestamp2datetime(self, timestamp):
        return datetime.fromtimestamp(timestamp, self.timezone).strftime('%d-%m-%Y %H:%M:%S')

    def _get_current_or_hourly_forecast(self, type_forecast):
        if type_forecast == 'current':
            forecast_list = [self.weather_forecast['current']]
        elif type_forecast == 'hourly':
            forecast_list = self.weather_forecast['hourly']
        else:
            raise NotImplementedError('No implemented type forecast')

        responses_list = []
        for forecast in forecast_list:
            response = {'time': self.convert_timestamp2datetime(forecast['dt'])}
            fields = ['temp', 'pressure', 'humidity', 'wind_speed']
            response.update({k: forecast[k] for k in fields})
            responses_list.append(response)
        return responses_list

    def get_current_forecast(self):
        return self._get_current_or_hourly_forecast('current')

    def get_hourly_forecast(self):
        return self._get_current_or_hourly_forecast('hourly')


pacan = WeatherForecast(lat, lon, token_owm)
curr = pacan.get_current_forecast()
hourly = pacan.get_hourly_forecast()

print(curr)
print(hourly)
print(len(hourly))

temps = [forecast['temp'] for forecast in hourly]

import matplotlib.pyplot as plt

print(temps)

plt.plot(temps)
plt.show()






