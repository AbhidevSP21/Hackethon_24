import os
import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from .models import Customers, uploads, FashionItem
import pandas as pd
import requests
from pathlib import Path
from PIL import Image

# Path to the folder with categorized clothing images
import os
from django.conf import settings

# Define BASE_FOLDER relative to your project structure
BASE_FOLDER = os.path.join(settings.BASE_DIR, 'classified_colors', 'corrected')

# Check if the folder exists at runtime
if not os.path.exists(BASE_FOLDER):
    raise FileNotFoundError(f"The specified folder does not exist: {BASE_FOLDER}")


# Helper function: Get all clothing types and colors
def get_clothing_types_and_colors(base_folder):
    clothing_types = os.listdir(base_folder)
    categories = {}
    for clothing_type in clothing_types:
        clothing_type_path = os.path.join(base_folder, clothing_type)
        if os.path.isdir(clothing_type_path):
            colors = os.listdir(clothing_type_path)
            categories[clothing_type] = colors
    return categories

# Helper function: Load images based on color preference
def load_images_for_color_recommendation(color_preference):
    images = []
    for clothing_type in os.listdir(BASE_FOLDER):
        clothing_type_folder = os.path.join(BASE_FOLDER, clothing_type)
        if os.path.isdir(clothing_type_folder):
            color_folder = os.path.join(clothing_type_folder, color_preference)
            if os.path.exists(color_folder):
                for filename in os.listdir(color_folder):
                    if filename.lower().endswith((".jpg", ".png", ".jpeg", ".bmp")):
                        image_path = os.path.join(color_folder, filename)
                        img_url = os.path.join(settings.MEDIA_URL, image_path.replace(settings.BASE_DIR, '').replace("\\", "/"))
                        images.append({"clothing_type": clothing_type, "img_url": img_url})
    return images

# View: Main page with color selection
def index(request):
    categories = get_clothing_types_and_colors(BASE_FOLDER)
    available_colors = sorted(set([color for types in categories.values() for color in types]))
    return render(request, 'index.html', {'available_colors': available_colors})

# AJAX View: Get clothing recommendations based on selected color
def get_recommendations(request):
    color_preference = request.GET.get('color', '')
    recommended_images = load_images_for_color_recommendation(color_preference)
    return JsonResponse({'images': recommended_images})

# View: Registration page
def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([name, email, password, confirm_password]):
            return render(request, 'registration.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email already registered'})

        user = User.objects.create(username=email, email=email, password=make_password(password.strip()))
        user.first_name = name
        user.save()

        customer = Customers.objects.create(user=user, name=name)
        customer.save()

        login(request, user)
        return redirect('index')

    return render(request, 'registration.html')

# View: Sign-in page
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        if not all([email, password]):
            return render(request, 'signin.html', {'error': 'Email and password are required'})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user)
            return redirect('portals')
        else:
            return render(request, 'signin.html', {'error': 'Invalid email or password'})

    return render(request, 'signin.html')

# View: Portals page (protected)
@login_required
def portals(request):
    user_customers = Customers.objects.filter(user=request.user)
    return render(request, 'portals.html', {'user_customers': user_customers})

# View: Upload items page
def uploaditems(request):
    return render(request, 'uploaditems.html', context={})

# View: Upload functionality
def upload(request):
    if request.method == 'POST':
        type = request.POST.get("type_of_cloth")
        color = request.POST.get("color")
        size = request.POST.get("size")
        gender = request.POST.get("gender")
        upload_file = request.FILES.get("upload_file")

        data = uploads(
            type_of_cloth=type,
            color=color,
            size=size,
            gender=gender,
            upload_file=upload_file
        )
        data.save()
    return redirect('portals')

# View: Display uploaded items
def getdetails(request):
    data = uploads.objects.filter(userid=request.user)
    return render(request, 'portals.html', {'data': data})

# Weather update page
def weatherupdate(request):
    return render(request, 'weatherupdate.html', context={})

# Recommendation logic
def recommend_outfit(df, temp, weather_condition):
    # Recommendation logic here
    pass  # Omitted for brevity, insert your function as-is

# Fetch and process weather data
def recommend(request):
    city = request.GET.get('city')
    temp, weather_condition = get_weather(city)

    if temp is not None:
        df = pd.read_csv('D:/Django projects/hackathon/Hackethon_24/SwapFit/data/styles.csv')
        recommended_items = recommend_outfit(df, temp, weather_condition)
        context = {
            'city': city,
            'temp': temp,
            'weather_condition': weather_condition,
            'recommended_items': recommended_items.to_dict(orient='records')
        }
        return render(request, 'SwapFit/recommendation.html', context)
    else:
        return render(request, 'error.html', {'error': 'Failed to fetch weather data.'})

# Fetch weather data
def get_weather(city):
    # Weather fetching logic here
    pass  # Omitted for brevity, insert your function as-is

# Map weather condition codes
def map_condition_code(code):
    condition_mapping = {
        0: "clear",
        1: "cloudy",
        2: "rainy",
        3: "stormy",
    }
    return condition_mapping.get(code, "unknown")
