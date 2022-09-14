from django import forms
from .models import *
from django.utils.timezone import now


class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='Фотодокументация', widget=forms.ClearableFileInput(attrs={'multiple': True}))


class WellsWaterdepthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WellsWaterdepthForm, self).__init__(*args, **kwargs)
        self.fields['water_depth'].required = False

    class Meta:
        model = WellsWaterdepth
        fields = ['water_depth']
        widgets = {
            'water_depth': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '150', 'step': '0.01'}),
        }
        labels = {
            'water_depth': 'Глубина до воды, м'
        }


class WellsTemperatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WellsTemperatureForm, self).__init__(*args, **kwargs)
        self.fields['temperature'].required = False

    class Meta:
        model = WellsTemperature
        fields = ['temperature']
        widgets = {
            'temperature': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}),
        }
        labels = {
            'temperature': 'Температура воды, ℃'
        }


class WellsConditionForm(forms.ModelForm):
    class Meta:
        model = WellsCondition
        fields = ['condition']
        widgets = {
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'condition': 'Техническое состояние скважины'
        }


class WellsDepthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WellsDepthForm, self).__init__(*args, **kwargs)
        self.fields['depth'].required = False

    class Meta:
        model = WellsDepth
        fields = ['depth']
        widgets = {
            'depth': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}),
        }
        labels = {
            'depth': 'Глубина скважины, м'
        }


class WellsLugheightForm(forms.ModelForm):
    class Meta:
        model = WellsLugheight
        fields = ['lug_height']
        widgets = {
            'lug_height': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'min': '0', 'max': '50', 'step': '0.01'}),
        }
        labels = {
            'lug_height': 'Высота патрубка, м'
        }


class WellsInspectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WellsInspectionForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now
        self.fields['damage_status'].required = False
        self.fields['automation_status'].required = False
        self.fields['logs_status'].required = False
        self.fields['automation_condition'].required = False

        self.fields['area_description'].label = False
        self.fields['damage_description'].label = False
        self.fields['automation_description'].label = False
        self.fields['logs_results'].label = False
        self.fields['survey2'].label = False

    class Meta:
        model = WellsInspection
        fields = ['well', 'date', 'weather', 'painting_condition', 'lable_condition', 'well_lug_condition',
                  'well_head_condition', 'well_collar_condition', 'damage_status', 'damage_description',
                  'automation_status', 'automation_condition', 'automation_description', 'area_condition',
                  'area_description', 'logs_status', 'logs_results', 'recommendations', 'comments', 'survey1',
                  'survey2']

        widgets = {
            'well': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'area_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'painting_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'lable_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'well_lug_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'well_head_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'well_collar_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'automation_condition': forms.Select(attrs={'class': 'form-control'}, ),
            'damage_status': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'automation_status': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'logs_status': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'weather': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 1}),
            'damage_description': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Описание повреждений'}),
            'area_description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2,
                                                      'placeholder': 'Описание прилегающей территории'}),
            'automation_description': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Описание автоматики'}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'logs_results': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Результаты видеокаротажа'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'survey1': forms.Select(attrs={'class': 'form-control'}),
            'survey2': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'well': 'Номер скважины',
            'area_condition': 'Состояние прилегающей территории',
            'painting_condition': 'Состояние покраски',
            'lable_condition': 'Состояние маркировки',
            'well_lug_condition': 'Состояние патрубка',
            'well_head_condition': 'Состояние оголовка',
            'well_collar_condition': 'Состояние устья',
            'automation_condition': 'Состояние автоматики',
            'damage_status': 'Наличие повреждений',
            'automation_status': 'Наличие автоматики',
            'logs_status': 'Проведение видеокаротажа',
            'weather': 'Погодные условия',
            'damage_description': 'Описание повреждений',
            'area_description': 'Описание прилегающей территории',
            'automation_description': 'Описание автоматики',
            'recommendations': 'Рекомендации',
            'logs_results': 'Результаты видеокаротажа',
            'comments': 'Примечания',
            'survey1': 'Обследование провели',
            'date': 'Дата инспекции',
        }
