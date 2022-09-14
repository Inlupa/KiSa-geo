import django_filters
from django import forms
from .models import ReconPointsSurvey, ReconSitesSurvey


class ReconPointsSurveyFilter(django_filters.FilterSet):
    recon_point_id = django_filters.CharFilter('recon_point_id', lookup_expr='exact',
                                               widget=forms.TextInput(
                                                   attrs={'class': 'form-control', 'type': 'integer'}),
                                               label='Номер точки наблюдения')
    date = django_filters.DateFilter(label='Дата наблюдения',
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = ReconPointsSurvey
        fields = ['recon_point_id', 'date']


class ReconSitesSurveyFilter(django_filters.FilterSet):
    recon_site_id = django_filters.CharFilter('recon_site_id', lookup_expr='exact',
                                              widget=forms.TextInput(
                                                  attrs={'class': 'form-control', 'type': 'integer'}),
                                              label='Номер участка рекогносцировки')
    date = django_filters.DateFilter('doc__creation_date', label='Дата составления акта',
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = ReconSitesSurvey
        fields = ['recon_site_id', 'doc__creation_date']
