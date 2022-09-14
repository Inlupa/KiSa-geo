import os, shutil
import io
import base64
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.db.models import Max, Min
from django.core.paginator import Paginator
from plpygis import Geometry
from .filters import *
from .forms import *
from .models import *


def egp_observes_inspection_init(request):
    """Достаем все записи в таблице инспекций и закидываем в html страницу"""
    egp_obs_list = EgpObservesInspection.objects.all()
    filter = EgpObservesInspectionFilter(request.GET, queryset=egp_obs_list)
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'egp_observes_inspection/egp_observes_inspection_init.html',
                  {'filter': filter, 'page_obj': page_obj})


def egp_observes_inspection_create(request):
    if request.method == 'POST':
        form_egp_observes_inspection = EgpObservesInspectionForm(request.POST)
        form_egp_observes = EgpObservesForm(request.POST)
        form_field = FileFieldForm(request.POST)
        egp_obs_id = form_egp_observes_inspection['egp_obs'].value()
        date = form_egp_observes_inspection['date'].value()

        if Documents.objects.all().exists():
            doc_id = Documents.objects.latest('doc_id').doc_id + 1
        else:
            doc_id = 1


        eoi_data = EgpObservesInspection(egp_obs_id=egp_obs_id, date=date, doc_id=doc_id)
        form_egp_observes_inspection = EgpObservesInspectionForm(data=request.POST, instance=eoi_data)

        eoc_data = EgpObservesCondition(egp_obs_id=egp_obs_id, date=date, doc_id=doc_id)
        form_egp_observes_condition = EgpObservesConditionForm(data=request.POST, instance=eoc_data)
        if form_egp_observes_inspection.is_valid() and form_egp_observes_condition.is_valid():
            Documents(doc_id=doc_id, doc_type=2101, reg_status=0, creation_date=now()).save()
            form_egp_observes_inspection.save()
            form_egp_observes_condition.save()
    else:
        form_egp_observes_inspection = EgpObservesInspectionForm()
        form_egp_observes_condition = EgpObservesConditionForm()
        form_egp_observes = EgpObservesForm()
        form_field = FileFieldForm()
    return render(request, "egp_observes_inspection/egp_observes_inspection.html",
                  context={'form_egp_observes_inspection': form_egp_observes_inspection, 'form_field': form_field,
                           'form_egp_observes': form_egp_observes,
                           'form_egp_observes_condition': form_egp_observes_condition})


def egp_observes_inspection_edit(request, pk):
    """Редактирование записи инспекции скважины"""
    instance_egp_obs_inspection = EgpObservesInspection.objects.get(pk=pk)
    egp_obs_id = instance_egp_obs_inspection.egp_obs_id
    date = instance_egp_obs_inspection.date
    instance_egp_obs_condition = EgpObservesCondition.objects.get(egp_obs_id=egp_obs_id, date=date)
    instance_egp_obs = EgpObserves.objects.get(egp_obs_id=egp_obs_id)
    form_egp_observes = EgpObservesForm(instance=instance_egp_obs)
    form_field = FileFieldForm()
    if request.method == 'POST':
        form_egp_observes_inspection = EgpObservesInspectionForm(data=request.POST, instance=instance_egp_obs_inspection)
        form_egp_observes_condition = EgpObservesConditionForm(data=request.POST, instance=instance_egp_obs_condition)
        if form_egp_observes_inspection.is_valid() and form_egp_observes_condition.is_valid():
            form_egp_observes_inspection.save()
            form_egp_observes_condition.save()
    else:

        form_egp_observes_inspection = EgpObservesInspectionForm(instance=instance_egp_obs_inspection)
        form_egp_observes_condition = EgpObservesConditionForm(instance=instance_egp_obs_condition)

    return render(request, "egp_observes_inspection/egp_observes_inspection_edit.html",
                  context={'form_egp_observes_inspection': form_egp_observes_inspection, 'form_field': form_field,
                           'form_egp_observes': form_egp_observes,
                           'form_egp_observes_condition': form_egp_observes_condition})


def eoi_prepopulated(request):
    data = None
    egp_point = request.GET.get('egp_point', None)
    date = request.GET.get('date', None)
    return JsonResponse(data, safe=False)