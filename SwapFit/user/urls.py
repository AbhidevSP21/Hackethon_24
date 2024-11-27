from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns=[
    path('',views.index,name="index"),
    path('registration',views.registration,name="registration"),
    path('signin',views.signin,name="signin"),
    path('portals',views.portals,name="portals"),
    path('uploaditems',views.uploaditems,name="uploaditems"),
    path('upload',views.upload,name="upload"),
    path('getdetails',views.getdetails,name="getdetails"),
    path('weatherupdate',views.weatherupdate,name="weatherupdate")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)