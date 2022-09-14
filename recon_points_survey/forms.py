from django import forms
from .models import *
from django.utils.timezone import now
from datetime import date

efficiency = {0: 'Эффективен', 1: 'Частично эффективен', 2: 'Не эффективен', 4: 'Отсутствует'}
efficiency = tuple(map(tuple, efficiency.items()))

zero_to_3 = {u'null': 'нет', 0: '0', 1: '1', 2: '2', 3: '3'}
zero_to_3 = tuple(map(tuple, zero_to_3.items()))


class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='Фотодокументация', widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ReconPointsSurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReconPointsSurveyForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now

    class Meta:
        model = ReconPointsSurvey
        fields = (
            'recon_point', 'date', 'point_description')

        widgets = {
            'recon_point': forms.TextInput(attrs={'class': 'form-control','type':'integer'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'point_description': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 3, 'placeholder': 'Описание процессов'}),
        }
        labels = {
            'recon_point': 'Номер точки наблюдения',
            'date': 'Дата наблюдения',
            'point_description': 'Описание точки наблюдения',
        }


class ReconSitesForm(forms.ModelForm):
    class Meta:
        model = ReconSites
        fields = ('recon_site_id', 'position', 'geomorph')
        widgets = {
            'recon_site_id': forms.TextInput(attrs={'class': 'form-control', 'type': 'integer'}),
            'position': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'geomorph': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
        }
        labels = {
            'recon_site_id': 'Номер участка',
            'position': 'Адресная привязка',
            'geomorph': 'Геоморфологическая привязка'
        }


class ReconSitesSurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReconSitesSurveyForm, self).__init__(*args, **kwargs)
        self.fields['survey2'].label = False
    class Meta:
        model = ReconSitesSurvey
        fields = ('dates', 'survey1', 'survey2', 'weather', 'route_length',
                  'anthropogenic_impact', 'conclusion','survey_information','work_information')
        widgets = {

            'dates': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'survey1': forms.Select(attrs={'class': 'form-control'}),
            'survey2': forms.Select(attrs={'class': 'form-control'}),
            'route_length': forms.TextInput(attrs={'class': 'form-control', 'type': 'numeric'}),
            'weather': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'survey_information': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'work_information': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'anthropogenic_impact': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'conclusion': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
        }
        labels = {
            'dates': 'Даты проведения обследования',
            'survey1': 'Обследование провели',
            'route_length': 'Длина маршрута, м',
            'weather': 'Погодные условия',
            'anthropogenic_impact': 'Признаки техногенного воздействия',
            'conclusion': 'Заключение',
            'survey_information':'Информация о обследовании',
            'work_information':'Информация о проведенных работах',
        }

class DocumentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentsForm, self).__init__(*args, **kwargs)
        self.fields['creation_date'].initial = now
    class Meta:
        model = Documents
        fields = ('creation_date',)
        widgets = {

            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
        labels = {
            'creation_date': 'Дата составления акта',
        }
