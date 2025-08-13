from django.shortcuts import render
import requests
from django.conf import settings

def home(request):
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = settings.OPENWEATHER_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                error = data.get("message", "Error fetching data.")
            else:
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon']
                }
        except Exception as e:
            error = str(e)

    return render(request, 'appWeather/home.html', {
        'weather_data': weather_data,
        'error': error
    })
