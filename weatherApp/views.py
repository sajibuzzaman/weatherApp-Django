from django.shortcuts import redirect, render, get_object_or_404
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def home(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=005f235fb8f211ddba4217fd7c8a6ede"
    errmsg = ''
    msgclass = ''
    msg = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                    
                else:
                    errmsg = "The city is not exist in the world"
            else:
                errmsg = "Already city is added to database"
        if errmsg:
            msg = errmsg
            msgclass = 'is-danger'
        else:
            msg = "The city is successfully added in database"
            msgclass = 'is-success'
        
    form = CityForm()
   
    weather = []
    city = City.objects.all()
    for p in city:
        r = requests.get(url.format(p)).json()
        temparature_F= r['main']['temp']
        temparature_C = (temparature_F-32)*5/9
        city_weather={
            'city': p,
            'temparature': int(temparature_C),
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather.append(city_weather)
    context={
        'weather': weather, 
        'form': form,
        'msg': msg,
        'msgclass': msgclass,
        }

    return render(request, 'weatherApp/index.html', context)

def city_delete(request, city_name):
    city = get_object_or_404(City, name= city_name)
    city.delete()

    return redirect('weatherApp:home')