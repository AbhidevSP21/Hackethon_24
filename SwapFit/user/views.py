from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import matplotlib.pyplot as plt


# Create your views here.

def index(request):
    return render(request, 'index.html',context={})