from django import forms
from .models import *
from django.utils.timezone import now


category_3 = {1: 'Удовлетворительное', 2: 'Хорошее', 0: 'Неудовлетворительное'}
category_3 = tuple(map(tuple, category_3.items()))

mark_rep = {0: 'Репер', 1: 'Марка', 2: 'Инклинометр'}
mark_rep = tuple(map(tuple, mark_rep.items()))

cond = {1: 'Действующая', 2: 'Резервная', 3: 'Недействующая', 4: 'Законсервированная', 5: 'Неисправная',
        6: 'Заброшенная', 7: 'Ликвидированная', 8: 'Проектная', 9: 'Пробурена'}
cond = tuple(map(tuple, cond.items()))

class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='Фотодокументация', widget=forms.ClearableFileInput(attrs={'multiple': True}))


class EgpObservesInspectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EgpObservesInspectionForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now
        self.fields['damage_description'].label = False
        self.fields['survey2'].label = False
        self.fields['logs_results'].label = False

    class Meta:
        model = EgpObservesInspection
        fields = (
            'egp_obs', 'date', 'survey1', 'survey2', 'painting_condition', 'label_condition', 'damage_description',
            'logs_status', 'logs_results', 'comments', 'recommendations')

        widgets = {
            'egp_obs': forms.TextInput(attrs={'class': 'form-control', 'type': 'integer'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'painting_condition': forms.Select(choices=category_3, attrs={'class ': 'form-control'}),
            'label_condition': forms.Select(choices=category_3, attrs={'class': 'form-control'}),
            'damage_description': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Описание повреждений'}),
            'logs_status': forms.CheckboxInput(),
            'logs_results': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2, 'placeholder': 'Результаты видеокаротажа'}),
            'comments': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'recommendations': forms.Textarea(
                attrs={'class': 'form-control', 'type': 'text', 'rows': 2}),
            'survey1': forms.Select(attrs={'class': 'form-control'}),
            'survey2': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'egp_obs': 'Номер пункта наблюдений',
            'date': 'Дата инспекции',
            'painting_condition': 'Состояние покраски',
            'label_condition': 'Состояние маркировки',
            'logs_status': 'Проведение видеокаротажа',
            'comments': 'Примечания',
            'recommendations': 'Рекомендации',
            'survey1': 'Обследование провели',
        }

class EgpObservesForm(forms.ModelForm):
    class Meta:
        model = EgpObserves
        fields = ('egp_obs_type',)

        widgets = {
            'egp_obs_type': forms.Select(choices=mark_rep, attrs={'class': 'form-control'}),
        }
        labels = {
            'egp_obs_type': 'Тип пункта наблюдений',
        }

class EgpObservesConditionForm(forms.ModelForm):
    class Meta:
        model = EgpObservesCondition
        fields = ('condition',)

        widgets = {
            'condition': forms.Select(choices=cond, attrs={'class': 'form-control'}),
        }
        labels = {
            'condition': 'Техническое состояние пункта наблюдений',
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
            'creation_date': 'Дата создания акта',
        }
