from django.shortcuts import render
import requests

def get_wind_direction(degree):
    """डिग्री को Cardinal direction में बदलें"""
    directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West']
    idx = int((degree + 22.5) // 45) % 8
    return directions[idx]

def home(request):
    context = {}
    forecast_data = []

    if request.method == "POST":
        city = request.POST.get('city')
        key = '7a8457caf38e3cc928ffb1efd7953401'
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric"

        response = requests.get(api)
        if response.status_code == 200:
            data = response.json()
            forecast_res = requests.get(forecast_url).json()

            wind_deg = data["wind"].get("deg", 0)
            wind_dir = get_wind_direction(wind_deg)

            context = {
                'city': city,
                'temperature': round((data["main"]["temp"] * 9/5) + 32, 2),
                'description': data["weather"][0]["description"].capitalize(),
                'main': data["weather"][0]["main"],
                'icon': data["weather"][0]["icon"],
                'pressure': data["main"]["pressure"],
                'deg': f"{wind_deg}° ({wind_dir})",
                'wind_speed': data["wind"]["speed"]
            }

            if forecast_res.get('cod') == '200':
                for item in forecast_res['list']: 
                    if "12:00:00" in item['dt_txt']:
                        forecast_data.append({
                            'date': item['dt_txt'].split()[0],
                            'temp': item['main']['temp'],
                            'desc': item['weather'][0]['description'].title(),
                            'icon': item['weather'][0]['icon']
                        })

            context['forecast'] = forecast_data

    return render(request, 'index.html', context)
