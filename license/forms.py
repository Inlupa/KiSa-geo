from django import forms
from .models import *
from django.utils.timezone import now


org_license = {0: 'Центрнедра', 1: 'ДПиООС Москвы', 2: 'МЭиП Московской области'}
org_license = tuple(map(tuple, org_license.items()))

licence_status = {0: 'Аннулирована', 1: 'Просрочена', 2: 'Действует'}
license_status = tuple(map(tuple, licence_status.items()))


class LicenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LicenseForm, self).__init__(*args, **kwargs)
        self.fields['date_start'].initial = now
        self.fields['date_end'].initial = now

    class Meta:
        model = License
        fields = ['license_id', 'department', 'subject', 'date_start', 'date_end', 'status', 'comments']
        widgets = {
            'license_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'department': forms.Select(attrs={'class': 'form-control'}, choices=org_license),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=license_status),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
        }
        labels = {
            'license_id': 'Номер лицензии',
            'department': 'Орган, выдавший лицензию',
            'subject': 'Недропользователь',
            'status': 'Статус действия',
            'date_end': 'Дата окончания лицензии',
            'date_start': 'Дата выдачи лицензии',
            'comments': 'Примечание',
        }


class LicenseToWellsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LicenseToWellsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LicenseToWells
        fields = ['well', 'flow_rate']
        widgets = {
            'well': forms.TextInput(attrs={'class': 'form-control'}),
            'flow_rate': forms.TextInput(attrs={'class': 'form-control'}),
        }


class WellsForm(forms.ModelForm):
    class Meta:
        model = Wells
        fields = ['aquifer', 'subsurface_site']
        widgets = {
            'aquifer': forms.TextInput(attrs={'class': 'form-control','readonly':'true'}),
            'subsurface_site': forms.TextInput(attrs={'class': 'form-control','readonly':'true'}),
        }