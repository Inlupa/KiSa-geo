from django import forms
from .models import *
from django.utils.timezone import now


class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='Фотодокументация', widget=forms.ClearableFileInput(attrs={'multiple': True}))


class DrawwellsWaterDepthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DrawwellsWaterDepthForm, self).__init__(*args, **kwargs)
        self.fields['water_depth'].required = False

    class Meta:
        model = DrawwellsWaterdepth
        fields = ['water_depth']
        widgets = {
            'water_depth': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}),
        }
        labels = {
            'water_depth': 'Глубина до воды, м'
        }


class DrawwellsTemperatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DrawwellsTemperatureForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].required = False

    class Meta:
        model = DrawwellsTemperature
        fields = ['temperature']
        widgets = {
            'temperature': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}),
        }
        labels = {
            'temperature': 'Температура воды, ℃'
        }


class DrawwellsSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DrawwellsSampleForm, self).__init__(*args, **kwargs)
        self.fields['sample_name'].required = False

    class Meta:
        model = DrawwellsSample
        fields = ['sample_name']
        widgets = {
            'sample_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }
        labels = {
            'sample_name': 'Номер пробы воды'
        }


class DrawwellsInspectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DrawwellsInspectionForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now
        self.fields['area_description'].label = False
        self.fields['captage_description'].label = False
        self.fields['survey2'].label = False

    class Meta:
        model = DrawwellsInspection
        fields = ['drawwell', 'date', 'usage', 'captage_condition', 'captage_description', 'lug_height', 'depth',
                  'area_condition', 'area_description', 'recommendations', 'comments', 'survey1', 'survey2']

        widgets = {
            'drawwell': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'area_condition': forms.Select(attrs={'class': 'form-control'}),
            'captage_condition': forms.Select(attrs={'class': 'form-control'}),
            'usage': forms.Select(attrs={'class': 'form-control'}),
            'lug_height': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '5', 'step': '0.01'}),
            'depth': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}),
            'captage_description': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Описание каптажа'}),
            'area_description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2,
                                                      'placeholder': 'Описание прилегающей территории'}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'survey1': forms.Select(attrs={'class': 'form-control'}),
            'survey2': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'drawwell': 'Номер колодца',
            'date': 'Дата обследования',
            'area_condition': 'Состояние прилегающей территории',
            'captage_condition': 'Состояние каптажа',
            'usage': 'Характер использования колодца',
            'lug_height': 'Высота оголовка, м',
            'depth': 'Глубина колодца, м',
            'recommendations': 'Рекомендации',
            'comments': 'Примечания',
            'survey1': 'Обследование провели'
        }
