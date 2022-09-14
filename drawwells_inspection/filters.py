from .models import DrawwellsInspection
import django_filters
from django import forms



class DrawWellsInspectionFilter(django_filters.FilterSet):
    drawwell_id = django_filters.CharFilter('drawwell_id', lookup_expr='exact',
                                            widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'integer'}),
                                            label='Номер колодца')
    date = django_filters.DateFilter(label='Дата обследования',
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = DrawwellsInspection
        fields = ['drawwell_id', 'date']



