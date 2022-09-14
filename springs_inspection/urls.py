from django.urls import path
from .views import *

urlpatterns = [
    path('springs_inspection/', springs_inspection_init, name='springs_inspection_init'),
    path('springs_inspection/<int:pk>/', springs_inspection_edit, name='springs_inspection_edit'),
    path('springs_inpsection/di_prepopulated/', si_prepopulated, name='si_prepopulated'),
    path('springs_inspection/create/', springs_inspection_create, name='springs_inspection_create'),
    path('springs_inspection/delete_attach/<int:attachmentid>/', si_delete_attach, name='si_delete_attach'),
    path('springs_inspection/generate_act/', si_generate_acts, name='si_generate_acts'),
]