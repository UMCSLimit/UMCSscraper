import requests
import sys
from flask import Response

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
        #print(weather['main']['temp'])
        print(weather)
        return Response(
				response=weather,
				status=200,
				mimetype='application/json'
			)
    def getwxforecast(self):
        location = 'Lublin'
        weather = self.get_f_weather(self.api_key, location)
        return Response(
            response=weather,
            status=200,
            mimetype='application/json'
        )


if __name__ == "__main__":
    wx = Weather()
    print(wx.getwxmain())
