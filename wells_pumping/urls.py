from django.urls import path
from .views import *


urlpatterns = [
    path('wells_pumping/', wells_pumping_init, name='wells_pumping_init'),
    path('wells_pumping/<int:pk>/', wells_pumping_edit, name='wells_pumping_edit'),
    path('wells_pumping/create/', wells_pumping_create, name='wells_pumping_create'),
    path('wells_pumping/generate_act/', wp_generate_acts, name='wp_generate_acts'),
    path('wells_pumping/wp_prepopulated/', wp_prepopulated, name='wp_prepopulated'),
]
