import django_filters
from django import forms
from .models import SpringsInspection


class SpringsInspectionFilter(django_filters.FilterSet):
    spring_id = django_filters.CharFilter('spring_id', lookup_expr='exact',
                                          widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'integer'}),
                                          label='Номер родника')
    date = django_filters.DateFromToRangeFilter(label='Дата обследования',
                                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = SpringsInspection
        fields = ['spring_id', 'date']
