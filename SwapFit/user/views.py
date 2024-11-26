from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import matplotlib.pyplot as plt
from .models import Customers
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
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
    