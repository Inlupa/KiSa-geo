from django import forms
from .models import *
from django.utils.timezone import now


class TimeFieldsWellsPumpingForm(forms.Form):
    pump_time = forms.TimeField(label='Продолжительность откачки', required=False,
                                widget=forms.TimeInput(attrs={'type': 'time'}))
    recovery_time = forms.TimeField(label='Продолжительность восстановления', required=False,
                                    widget=forms.TimeInput(attrs={'type': 'time'}))


class WellsPumpingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WellsPumpingForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now
        self.fields['survey2'].label = False

    class Meta:
        model = WellsPumping
        fields = (
            'well', 'date', 'survey1', 'survey2', 'test_type', 'pump_type', 'pump_depth',
            'flow_rate', 'depression', 'comments')
        widgets = {
            'well': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'survey1': forms.Select(attrs={'class': 'form-control'}),
            'survey2': forms.Select(attrs={'class': 'form-control'}),
            'pump_type': forms.Select(attrs={'class': 'form-control'}),
            'test_type': forms.Select(attrs={'class': 'form-control'}),
            'pump_depth': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '100', 'step': '0.01'}),
            'flow_rate': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '15000', 'step': '0.001'}),
            'depression': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '100', 'step': '0.01'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 3}),
        }

        labels = {
            'well': 'Номер скважины',
            'date': 'Дата проведения опыта',
            'survey1': 'Опыт провели:',
            'pump_type': 'Тип водоподъёмного оборудования',
            'test_type': 'Тип опыта',
            'pump_depth': 'Глубина загрузки оборудования, м',
            'flow_rate': 'Дебит откачки, л/с',
            'depression': 'Понижение уровня, м',
            'comments': 'Примечания',
        }


class WellsWaterDepthForm(forms.ModelForm):
    class Meta:
        model = WellsWaterdepth
        fields = ('water_depth',)
        widgets = {
            'water_depth': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '150', 'step': '0.01'}), }
        labels = {
            'water_depth': 'Статический уровень, м'
        }


class WellsTemperatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WellsTemperatureForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].required = False

    class Meta:
        model = WellsTemperature
        fields = ('temperature',)
        widgets = {
            'temperature': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}), }

        labels = {
            'temperature': 'Температура воды, ℃'
        }
