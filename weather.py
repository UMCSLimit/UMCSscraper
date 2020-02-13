import requests
import sys
from flask import Response
import json
class Weather:
    def __init__(self):
        self.api_key = 'fa8a0d077c0f90dc6a4f252da0a0ec08'
 
    def get_weather(self, api_key, location):
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
        r = requests.get(url)
        return r
    def get_f_weather(self, api_key, location):
        url = "https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}".format(location, api_key)
        r = requests.get(url)
        return r
    def getwxmain(self):  
        location = 'Lublin'
        weather = self.get_weather(self.api_key, location)
        wx = weather.json()
        wx['main']['temp'] = round(wx['main']['temp'],0)
        wx['main']['feels_like'] = round(wx['main']['feels_like'],0)
        wx['main']['temp_min'] = round(wx['main']['temp_min'],0)
        wx['main']['temp_max'] = round(wx['main']['temp_max'],0)
        weather = json.dumps(wx)
        #print(weather['main']['temp'])
        #print(weather)
        return Response(
				response=weather,
				status=200,
				mimetype='application/json'
			)
    def getwxforecast(self):
        location = 'Lublin'
        weather = self.get_f_weather(self.api_key, location)
        weather = weather.json()
        i=0
        tokeep = [0,1,2,8,16,24, 32]
        q=0
        deleted = 0
        while i < weather['cnt']:
            if i not in tokeep:
                del weather['list'][i-deleted]
                deleted+=1
            if i in tokeep:
                #round temps
                weather['list'][i-deleted]['main']['temp_max'] = round(weather['list'][i-deleted]['main']['temp_max'],0)
                weather['list'][i-deleted]['main']['temp_min'] = round(weather['list'][i-deleted]['main']['temp_min'],0)
                weather['list'][i-deleted]['main']['temp'] = round(weather['list'][i-deleted]['main']['temp'],0)
                weather['list'][i-deleted]['main']['feels_like'] = round(weather['list'][i-deleted]['main']['feels_like'],0)
            i+=1
        print('elementow: ' + str(i))
        wx = json.dumps(weather)
        return Response(
            response=wx,
            status=200,
            mimetype='application/json'
        )


if __name__ == "__main__":
    wx = Weather()
    print(wx.getwxforecast())
