from django.urls import path,include
from django.conf import settings
from  .views import index,fashion,lifestyle,recommend,travel,vlogs,upload,form,registration,signin,portals

urlpatterns=[
    path('',index,name="index"),
    path('fashion',fashion,name="fashion"),
    path('lifestyle',lifestyle,name="lifestyle"),
    path('recommendation',recommend,name="recommendation"),
    path('travel',travel,name="travel"),
    path('vlogs',vlogs,name="vlogs"),
    path('upload',upload,name="upload"),
    path('form',form,name="form"),

    path('',index,name="index"),
    path('registration',registration,name="registration"),
    path('signin',signin,name="signin"),
    path('portals',portals,name="portals")
    
]