from django.urls import path,include
from django.conf import settings
from .import views

urlpatterns=[
    path('',views.index,name="index"),
    path('registration',views.registration,name="registration"),
    path('signin',views.signin,name="signin"),
    path('portals',views.portals,name="portals"),
    
]