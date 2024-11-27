from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import matplotlib.pyplot as plt
from django.shortcuts import render
from pathlib import Path
from .models import FashionItem
import os
import requests
import pandas as pd
# BASE_DIR from settings.py

def recommend_outfit(df, temp, weather_condition):
    recommendations = pd.DataFrame()
    df = df.dropna(subset=['season', 'articleType'])


    # Determine current season based on temperature
    if temp > 30:
        current_season = 'Summer'
    elif 15 < temp <= 30:
        current_season = 'Spring'
    elif 5 < temp <= 15:
        current_season = 'Fall'
    else:
        current_season = 'Winter'


    # Filter items based on weather conditions
    if weather_condition.lower() == 'clear':
        recommendations = df[
            (df['articleType'].str.contains('T-shirt|Shorts|Dress', case=False)) &
            (df['season'].str.contains(current_season, case=False)) &
            (df['masterCategory'] == 'Apparel')
        ]
    elif weather_condition.lower() in ['rain', 'stormy']:
        recommendations = df[
            (df['articleType'].str.contains('Raincoat|Waterproof|Stormproof|Jacket|Boots', case=False)) &
            (df['season'].str.contains(current_season, case=False)) &
            (df['masterCategory'] == 'Apparel')
        ]
    if recommendations.empty:
        recommendations = df[
            (df['season'].str.contains(current_season, case=False)) &
            (df['masterCategory'] == 'Apparel')
        ]


    return recommendations[['id', 'articleType', 'baseColour', 'season', 'productDisplayName']]


# Function to handle the main index page
def index(request):
    return render(request, 'SwapFit/index.html')


# Function to handle city-based recommendation
def recommend(request):
    city = request.GET.get('city')  # Get the city from the URL query parameters
    temp, weather_condition = get_weather(city)  # Fetch the weather data


    if temp is not None:
        # Load the fashion items dataset
        df = pd.read_csv('D:\Django projects\hackathon\Hackethon_24\SwapFit\data\styles.csv')  # Ensure correct file path
        recommended_items = recommend_outfit(df, temp, weather_condition)  # Get recommended outfits
        # Pass the weather data and recommended items to the template
        context = {
            'city': city,
            'temp': temp,
            'weather_condition': weather_condition,
            'recommended_items': recommended_items.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
        }
        return render(request, 'SwapFit/recommendation.html', context)
    else:
        return render(request, 'error.html', {'error': 'Failed to fetch weather data.'})


# Function to get weather data using OpenWeatherMap API
def get_weather(city):
    api_key = "b5b5fd951335436cb600b2a10b0958d2"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                temp = weather_data['current_weather']['temperature']
                condition_code = weather_data['current_weather']['weathercode']
                weather_condition = map_condition_code(condition_code)
                return temp, weather_condition
    return None, None


# Mapping weather codes to conditions
def map_condition_code(code):
    condition_mapping = {
        0: "clear",
        1: "cloudy",
        2: "rainy",
        3: "stormy",
    }
    return condition_mapping.get(code, "unknown")







def fashion(request):
    return render(request, 'Swapfit/fashion.html',context={})
def lifestyle(request):
    return render(request, 'Swapfit/lifestyle.html',context={})
# # def recommending(request):
#     return render(request, 'Swapfit/recommendation.html',context={})
def travel(request):
    return render(request, 'Swapfit/travel.html',context={})
def vlogs(request):
    return render(request, 'Swapfit/vlogs.html',context={})
def upload(request):
    return render(request, 'Swapfit/uploads.html',context={})
def form(request):
    return render(request, 'Swapfit/form.html',context={})
