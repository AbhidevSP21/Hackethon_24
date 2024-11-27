from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from  .views import index,fashion,lifestyle,recommend,travel,vlogs,upload,form,registration,signin,portals

urlpatterns=[
<<<<<<< HEAD
    path('',views.index,name="index"),
    path('registration',views.registration,name="registration"),
    path('signin',views.signin,name="signin"),
    path('portals',views.portals,name="portals"),
    path('uploaditems',views.uploaditems,name="uploaditems"),
    path('upload',views.upload,name="upload"),
    path('getdetails',views.getdetails,name="getdetails"),
    path('weatherupdate',views.weatherupdate,name="weatherupdate"),
    path('recommend/', views.get_recommendations, name='get_recommendations')  # AJAX for recommendations
]
=======
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
>>>>>>> 588a6573ca789bf6118970185de340f4122c9f49
    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)