from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import Customers
from django.contrib.auth.decorators import login_required
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
    print("here")
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
    return render(request, 'index.html',context={})

def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print("Name received:", name)
        # Ensure none of the fields are None
        if not all([name, email, password, confirm_password]):
            return render(request, 'registration.html', {'error': 'All fields are required'})

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        # Check if email is already used
        if User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email already registered'})

        # Create the user
        user = User.objects.create(username=email, email=email, password=make_password(password.strip()))
        
        # Optionally, you can set the first_name of the User model
        user.first_name = name  # Store the name in the user's first_name field (optional)
        user.save()

        # Create the customer profile
        customer = Customers.objects.create(user=user, name=name)  # Ensure the 'name' field is saved
        customer.save()

        # Log the user in after registration
        login(request, user)

        return redirect('index')  # Redirect to the homepage or appropriate view

    return render(request, 'registration.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # username field holds email in the form
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not all([email, password]):
            return render(request, 'signin.html', {'error': 'Email and password are required'})

        # Authenticate using email
        try:
            user = User.objects.get(email=email)  # Get the user by email
        except User.DoesNotExist:
            user = None

        # If user exists, authenticate them
        if user and user.check_password(password):  # Check if the password matches
            login(request, user)  # Log the user in
            return redirect('portals')  # Redirect to the portal page after successful login
        else:
            # Authentication failed
            return render(request, 'signin.html', {'error': 'Invalid email or password'})

    # If GET request, render the sign-in page
    return render(request, 'signin.html')

@login_required

def portals(request):
    user_customers = Customers.objects.filter(user=request.user)
    return render(request, 'portals.html', {'user_customers': user_customers})
    
