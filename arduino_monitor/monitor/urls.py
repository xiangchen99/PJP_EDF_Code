from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_list, name='data_list'),
    path('sensor-data/', views.sensor_data_json, name='sensor_data_json'),

]