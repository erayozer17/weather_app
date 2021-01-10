from django.shortcuts import render

def get_current_weather_in_city(request):
    return render(request, 'deneme.html', {})
