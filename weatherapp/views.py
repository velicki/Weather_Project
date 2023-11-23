from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=API_id'
    PARAMS = {'units':'metric'}

    API_KEY = 'API_key'
    SEARCH_ENGINE_ID = 'id_number'

    query = city
    page = 1
    start = (page-1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    
    search_items = data.get("items")

    try:
        image_url = search_items[0]['link']
        data = requests.get(url,PARAMS).json()

        description = data["weather"][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']

        day = datetime.date.today()

        return render(request, 'weatherapp\index.html',{'description':description,'icon':icon, 'temp':temp,'feels_like':feels_like,'temp_min':temp_min,'temp_max':temp_max,'humidity':humidity, 'day':day, 'city':city, 'exception_occured':False, 'image_url':image_url})
    except:
        exception_occured=True
        messages.error(request,'Entered city is not availible to API')
        day = datetime.date.today()
        return render(request, 'weatherapp\index.html',{'description':'clear sky','icon':'01d', 'temp':25,'feels_like':25,'temp_min':25,'temp_max':25,'humidity':64, 'day':day, 'city':'indore', 'exception_occured':True})
