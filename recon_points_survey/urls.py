from django.urls import path, register_converter
from .views import *


urlpatterns = [
        path('recon_points_survey/', recon_points_survey_init, name='recon_points_survey_init'),
        path('recon_points_survey/create/', recon_points_survey_create, name='recon_points_survey_create'),
        path('recon_points_survey/<int:pk>/', recon_points_survey_edit, name='recon_points_survey_edit'),
        path('recon_sites_survey/', recon_sites_survey_init, name='recon_sites_survey_init'),
        path('recon_sites_survey/create', recon_sites_survey_create, name='recon_sites_survey_create'),
        path('recon_sites_survey/<int:pk>/', recon_sites_survey_edit, name='recon_sites_survey_edit'),
        path('recon_sites_survey/rss_prepopulated/', rss_prepopulated, name='rss_prepopulated'),
]
#