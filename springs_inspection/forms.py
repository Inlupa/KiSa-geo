from django import forms
from .models import *
from django.utils.timezone import now


class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='Фотодокументация', widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SpringsRateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpringsRateForm, self).__init__(*args, **kwargs)
        self.fields['spring_rate'].required = False

    class Meta:
        model = SpringsRate
        fields = ['spring_rate']
        widgets = {
            'spring_rate': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }
        labels = {
            'spring_rate': 'Дебит родника, л/с'
        }


class SpringsTemperatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpringsTemperatureForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].required = False

    class Meta:
        model = SpringsTemperature
        fields = ['temperature']
        widgets = {
            'temperature': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }
        labels = {
            'temperature': 'Температура воды, ℃'
        }


class SpringsSampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpringsSampleForm, self).__init__(*args, **kwargs)
        self.fields['sample_name'].required = False

    class Meta:
        model = SpringsSample
        fields = ['sample_name']
        widgets = {
            'sample_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }
        labels = {
            'sample_name': 'Номер пробы воды'
        }


class SpringsInspectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpringsInspectionForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now
        self.fields['area_description'].label = False
        self.fields['captage_description'].label = False
        self.fields['survey2'].label = False

    class Meta:
        model = SpringsInspection
        fields = ['spring', 'date', 'weather', 'usage', 'captage_condition', 'captage_description',
                  'area_condition', 'area_description', 'improve_description', 'recommendations', 'comments', 'survey1',
                  'survey2']

        widgets = {
            'spring': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'area_condition': forms.Select(attrs={'class': 'form-control'}),
            'captage_condition': forms.Select(attrs={'class': 'form-control'}),
            'usage': forms.Select(attrs={'class': 'form-control'}),
            'weather': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 1}),
            'captage_description': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Описание каптажа'}),
            'area_description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2,
                                                      'placeholder': 'Описание прилегающей территории'}),
            'improve_description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'survey1': forms.Select(attrs={'class': 'form-control'}),
            'survey2': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'spring': 'Номер родника',
            'date': 'Дата обследования',
            'area_condition': 'Состояние прилегающей территории',
            'captage_condition': 'Состояние каптажа',
            'usage': 'Характер использования родника',
            'weather': 'Погодные условия',
            'depth': 'Глубина, м',
            'recommendations': 'Рекомендации',
            'comments': 'Примечания',
            'survey1': 'Обследование провели',
            'improve_description': 'Описание благоустройства'
        }
