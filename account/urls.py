from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # post views
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard')

]