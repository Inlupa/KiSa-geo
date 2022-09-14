from django.urls import path
from .views import *

urlpatterns = [
        path('wells_inspection/', wells_inspection_init, name='wells_inspection_init'),
        path('wells_inspection/<int:pk>/', wells_inspection_edit, name='wells_inspection_edit'),
        path('wells_inpsection/wi_prepopulated/', wi_prepopulated, name='wi_prepopulated'),
        path('wells_inspection/create/', wells_inspection_create, name='wells_inspection_create'),
        path('wells_inspection/delete_attach/<int:attachmentid>/', wi_delete_attach, name='wi_delete_attach'),
        path('wells_inspection/generate_act/', wi_generate_acts, name='wi_generate_acts'),
]