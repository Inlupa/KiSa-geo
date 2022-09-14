from django.urls import path
from .views import *

urlpatterns = [
        path('license/', license_input, name='license_input'),
        path('license/lic_prepopulated/', lic_prepopulated, name='lic_prepopulated'),
]
