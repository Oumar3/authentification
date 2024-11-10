from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginn,name='login'),
    path('logoute/',views.logoute,name='logoute'),
    path('register/',views.register,name='register'),
]
