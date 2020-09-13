from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import matplotlib.pyplot as plt

from utils import lon, lat, token_owm


class WeatherForecast:
    def __init__(self, latitude, longitude, appid, pattern='%d-%m-%Y %H:%M:%S'):
        self.weather_forecast = None

        self.latitude = latitude
        self.longitude = longitude
        self.appid = appid
        self.units = 'metric'
        self.pattern = pattern

        self.params = {'lat': self.latitude,
                       'lon': self.longitude,
                       'appid': self.appid,
                       'units': self.units}

        self.timezone = None

        self.get_forecast_from_owm()

    def set_pattern(self, pattern):
        self.pattern = pattern

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
        return datetime.fromtimestamp(timestamp, self.timezone).strftime(self.pattern)

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

    def get_fig_hourly_temp(self, path_to_save=None):
        hourly = self.get_hourly_forecast()
        temps = [int(forecast['temp']) for forecast in hourly]
        timestamps = [forecast['time'] for forecast in hourly]
        fig = visual_graphs(temps, timestamps, 'Temperature', 'Hourly Forecast 48 hours')
        if path_to_save:
            path_to_save = Path(path_to_save)
            path_to_save.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(path_to_save)
        return fig


def visual_graphs(values, timestamps, ylabel, title) -> None:
    num_col = len(values)
    len_txt = 20
    xlim = (0, num_col + 1)
    ylim = (0, max(max(values) * 1.1, 1e-5))

    fig, ax = plt.subplots(figsize=(16, 7), facecolor='white')
    ax.set(ylabel=ylabel, ylim=ylim,
           xlim=xlim)

    labels_on_graph = []
    for k in range(len(timestamps)):
        str_tick = timestamps[k]
        len_str_tick = len(str_tick)
        if len_str_tick < len_txt:
            str_tick = str_tick + ' ' * (len_str_tick - len_txt)
        elif len_str_tick > len_txt:
            str_tick = str_tick[0: len_txt]

        labels_on_graph.append(str_tick)

    for i in range(num_col):
        val = values[i]
        ax.text(i + 1, val + ylim[1] * 0.01, int(val), horizontalalignment='center')
        ax.vlines(x=i + 1, ymin=0, ymax=val, color='firebrick', alpha=0.7, linewidth=20)

    plt.xticks(range(1, num_col + 1), labels_on_graph, rotation=-90)
    plt.title(title)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    pacan = WeatherForecast(lat, lon, token_owm, '%H:%M %d-%m')
    curr = pacan.get_current_forecast()
    hourly = pacan.get_hourly_forecast()
    pacan.get_fig_hourly_temp('/home/daloro/Desktop/zalupa.png').show()




