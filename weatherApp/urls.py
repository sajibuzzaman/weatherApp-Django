from django.urls import path
from . import views

app_name = 'weatherApp'
urlpatterns = [
    path('', views.home, name="home"),
    path('delete/<city_name>/', views.city_delete, name="city_delete"),
]