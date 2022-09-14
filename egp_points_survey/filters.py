from .models import EgpObservesInspection
import django_filters
from django import forms


class EgpObservesInspectionFilter(django_filters.FilterSet):
    egp_obs_id=django_filters.CharFilter('egp_obs_id',lookup_expr='exact',widget=forms.TextInput(attrs={'class':'form-control','type':'integer'}),label='Номер скважины')
    date = django_filters.DateFilter(label='Дата обследования',
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = EgpObservesInspection
        fields = ['egp_obs_id', 'date']

