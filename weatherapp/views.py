
import requests
from django.shortcuts import render
from datetime import datetime, timedelta

def get_weather(request):
    weather_data = {}
    city = request.GET.get('city')

    if city:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=dfda04bec856d8d4fc92ad078ad6de12&units=metric'
        response = requests.get(url).json()

        if response['cod'] == 200:
            timezone_offset = response['timezone']
            sunrise_utc = response['sys']['sunrise']
            sunset_utc = response['sys']['sunset']
            sunrise_local = datetime.utcfromtimestamp(sunrise_utc) + timedelta(seconds=timezone_offset)
            sunset_local = datetime.utcfromtimestamp(sunset_utc) + timedelta(seconds=timezone_offset)
            current_date = datetime.now() + timedelta(seconds=timezone_offset)
            sunrise_str = sunrise_local.strftime('%I:%M %p')
            sunset_str = sunset_local.strftime('%I:%M %p')
            current_date_str = current_date.strftime('%d-%m-%Y')

            weather_data = {
                'city': response['name'],
                'temperature': response['main']['temp'],
                'humidity': response['main']['humidity'],
                'wind_speed': response['wind']['speed'],
                'wind_direction': response['wind']['deg'],
                'sunrise': sunrise_str,
                'sunset': sunset_str,
                'current_date': current_date_str,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }
        else:
            weather_data['error'] = 'Invalid city name. Please enter correct city Name.'

    return render(request, 'home.html', {'weather': weather_data})
