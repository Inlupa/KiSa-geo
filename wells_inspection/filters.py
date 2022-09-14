from .models import WellsInspection
import django_filters
from django import forms


class WellsInspectionFilter(django_filters.FilterSet):
    well_id = django_filters.CharFilter('well_id', lookup_expr='exact',
                                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'integer'}),
                                        label='Номер скважины')
    date = django_filters.DateFilter(label='Дата инспекции',
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = WellsInspection
        fields = ['well_id', 'date']
