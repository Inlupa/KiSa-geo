from django.urls import path
from .views import *

urlpatterns = [
        path('egp_observes_inspection/create', egp_observes_inspection_create, name='egp_observes_inspection_create'),
        path('egp_observes_inspection/eoi_prepopulated/', eoi_prepopulated, name='eoi_prepopulated'),
        path('egp_observes_inspection/', egp_observes_inspection_init, name='egp_observes_inspection_init'),
        path('egp_observes_inspection/<int:pk>/', egp_observes_inspection_edit, name='egp_observes_inspection_edit'),
]