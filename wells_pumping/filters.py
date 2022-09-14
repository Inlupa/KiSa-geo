from .models import WellsPumping
import django_filters
from django import forms


class WellsPumpingFilter(django_filters.FilterSet):
    well_id = django_filters.CharFilter('well_id', lookup_expr='exact',
                                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'integer'}),
                                        label='Номер скважины')
    date = django_filters.DateFromToRangeFilter(label='Дата проведения опыта',
                                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = WellsPumping
        fields = ['well_id', 'date']
