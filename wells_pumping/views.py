import base64
import datetime
from babel.dates import format_date
from plpygis import Geometry
from django.db import connection
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import *
from .forms import *
from .models import *
from .act_generator import generate_well_pumping_acts


def convert_hm(date_time):
    format = '%H:%M'  # The format
    datetime_str = datetime.datetime.strptime(date_time, format)
    return datetime_str.hour * 3600 + datetime_str.minute * 60


def query_result(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        value = cursor.fetchall()
        return value


@login_required
def wells_pumping_init(request):
    """Достаем все записи в таблице инспекций и закидываем в html страницу"""
    wells_pumping_list = WellsPumping.objects.all()
    filter = WellsPumpingFilter(request.GET, queryset=wells_pumping_list)
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'wells_pumping/wells_pumping_init.html',
                  {'filter': filter, 'page_obj': page_obj})


@login_required
def wells_pumping_create(request):
    if request.method == 'POST':
        form_wells_pumping = WellsPumpingForm(request.POST)
        form_time = TimeFieldsWellsPumpingForm(request.POST)
        well_id = form_wells_pumping['well'].value()
        date = form_wells_pumping['date'].value()
        survey = form_wells_pumping['survey1'].value()
        pump_time = str(convert_hm(form_time['pump_time'].value())) if form_time[
                                                                           'pump_time'].value() != '' else None
        recovery_time = str(convert_hm(form_time['recovery_time'].value())) if form_time[
                                                                                   'recovery_time'].value() != '' else None

        doc_id = Documents.objects.all().aggregate(Max('doc_id'))['doc_id__max']+1

        wp_data = WellsPumping(well_id=well_id, date=date, doc_id=doc_id)
        wp_data.recovery_time = recovery_time
        wp_data.pump_time = pump_time
        form_wells_pumping = WellsPumpingForm(data=request.POST, instance=wp_data)

        ww_data = WellsWaterdepth(doc_id=doc_id, survey_id=survey, date=date, well_id=well_id)
        form_wells_waterdepth = WellsWaterDepthForm(data=request.POST, instance=ww_data)

        wt_data = WellsTemperature(doc_id=doc_id, survey_id=survey, date=date, well_id=well_id)
        form_wells_temperature = WellsTemperatureForm(data=request.POST, instance=wt_data)

        if form_wells_pumping.is_valid() and form_wells_waterdepth.is_valid() and form_wells_temperature.is_valid():
            Documents(doc_id=doc_id, doc_type=1203, reg_status=0, creation_date=now()).save()
            form_wells_pumping.save()

            if form_wells_waterdepth['water_depth'].value() != '':
                form_wells_waterdepth.save()
            if form_wells_temperature['temperature'].value() != '':
                form_wells_temperature.save()

            DocumentsAttach(rel_doc_id=Documents.objects.get(doc_id=doc_id).doc_id,
                            att_name=str(well_id) + '_' + str(
                                date) + '.pdf',
                            data=wp_generate_acts(request, True)).save()
            return HttpResponseRedirect('/wells_pumping')
    else:
        form_wells_pumping = WellsPumpingForm()
        form_wells_waterdepth = WellsWaterDepthForm()
        form_wells_temperature = WellsTemperatureForm()
        form_time = TimeFieldsWellsPumpingForm()
    return render(request, "wells_pumping/wells_pumping.html",
                  context={'form_wells_pumping': form_wells_pumping,
                           'form_wells_waterdepth': form_wells_waterdepth,
                           'form_wells_temperature': form_wells_temperature,
                           'form_time': form_time})


@login_required
def wells_pumping_edit(request, pk):
    instance_wells_pumping = WellsPumping.objects.get(pk=pk)
    doc_id = instance_wells_pumping.doc_id
    well_id = instance_wells_pumping.well_id
    date = instance_wells_pumping.date
    try:
        instance_wells_waterdepth = WellsWaterdepth.objects.get(well_id=well_id, date=date)
    except WellsWaterdepth.DoesNotExist:
        instance_wells_waterdepth = WellsWaterdepth(well_id=well_id, date=date, doc_id=doc_id)
    try:
        instance_wells_temperature = WellsTemperature.objects.get(well_id=well_id, date=date)
    except WellsTemperature.DoesNotExist:
        instance_wells_temperature = WellsTemperature(well_id=well_id, date=date, doc_id=doc_id)
    recovery_time, pump_time = [instance_wells_pumping.recovery_time, instance_wells_pumping.pump_time]
    if DocumentsAttach.objects.filter(rel_doc_id=doc_id).exists():
        pdfcreate = query_result(
            'select encode(data,\'base64\') from geology.documents_attach where rel_doc_id=\'' + str(
                doc_id) + '\'')
        pdffile = pdfcreate[0][0]
    else:
        pdffile = None
    td_recovery_time, td_pump_time = ['{:02d}:{:02d}'.format(int(recovery_time) // 3600, (
            int(recovery_time) // 60) % 60) if recovery_time is not None else None,
                                      '{:02d}:{:02d}'.format(int(pump_time) // 3600, (
                                              int(pump_time) // 60) % 60) if pump_time is not None else None]
    form_wells_time = TimeFieldsWellsPumpingForm(data={'recovery_time': td_recovery_time,
                                                       'pump_time': td_pump_time})

    if request.method == 'POST':
        form_wells_time = TimeFieldsWellsPumpingForm(
            data=request.POST)
        instance_wells_pumping.recovery_time = str(convert_hm(form_wells_time['recovery_time'].value())) if \
            form_wells_time['recovery_time'].value() != '' else None
        instance_wells_pumping.pump_time = str(convert_hm(form_wells_time['pump_time'].value())) if form_wells_time[
                                                                                                        'pump_time'].value() != '' else None
        form_wells_pumping = WellsPumpingForm(data=request.POST, instance=instance_wells_pumping)
        form_wells_waterdepth = WellsWaterDepthForm(data=request.POST, instance=instance_wells_waterdepth)
        form_wells_temperature = WellsTemperatureForm(data=request.POST, instance=instance_wells_temperature)
        if form_wells_pumping.is_valid() and form_wells_waterdepth.is_valid() and form_wells_temperature.is_valid():
            form_wells_pumping.save()
            if form_wells_waterdepth['water_depth'].value() != '':
                form_wells_waterdepth.save()
            if form_wells_temperature['temperature'].value() != '':
                form_wells_temperature.save()
            instance_doc_attach = DocumentsAttach.objects.get(rel_doc_id=doc_id)
            instance_doc_attach.data = wp_generate_acts(request, True)
            instance_doc_attach.save()
            return HttpResponseRedirect('/wells_pumping')
    else:
        form_wells_pumping = WellsPumpingForm(instance=instance_wells_pumping)
        form_wells_waterdepth = WellsWaterDepthForm(instance=instance_wells_waterdepth)
        form_wells_temperature = WellsTemperatureForm(instance=instance_wells_temperature)

    return render(request, "wells_pumping/wells_pumping_edit.html",
                  context={'form_wells_pumping': form_wells_pumping,
                           'form_wells_waterdepth': form_wells_waterdepth,
                           'form_wells_temperature': form_wells_temperature,
                           'form_time': form_wells_time,
                           'pdffile': pdffile})


@login_required
def wp_generate_acts(request, save=False):
    fillactfield = Wells.objects.get(well_id=request.POST.get("well"))
    g = Geometry(fillactfield.geom)
    fillsurveys1 = Workers.objects.get(worker_id=request.POST.get('survey1'))
    if request.POST.get('survey2') != '':
        fillsurveys2 = Workers.objects.get(worker_id=request.POST.get('survey2'))

    if request.POST.get("water_depth") != '' and request.POST.get("depression") != '':
        dynamic_head = str(float(request.POST.get("water_depth")) + float(request.POST.get("depression")))
    else:
        dynamic_head = ''
    condition_data = (
        ("Водоносный горизонт", "Глубина, м", "Диаметр фильтровой колонны, мм", "Интервал установки фильтра",
         "Тип насоса", "Глубина загрузки насоса, м"),
        (AquiferCodes.objects.get(aquifer_id=fillactfield.aquifer.aquifer_id).aquifer_index, '', '', '',
         request.POST.get("pump_type"), request.POST.get("pump_depth")),
    )
    pumping_data = (
        ("Продолжительность прокачки, час:мин", "Статический уровень, м", "Динамический уровень, м", "Понижение, м",
         "Дебит, м3/сут", "Восстановление уровня через 30 минут, %"),
        (request.POST.get("pump_time"), request.POST.get("water_depth"), dynamic_head, request.POST.get("depression"),
         request.POST.get("flow_rate"), request.POST.get("recovery_time")),
    )
    context = {'date': format_date(datetime.datetime.strptime(request.POST.get("date"), '%Y-%m-%d'), "d MMMM yyyy",
                                   locale='ru'),
               'well': request.POST.get("well"),
               'position': str(fillactfield.position),
               'x': str(round(g.x, 6)), 'y': str(round(g.y, 6)), 'comments': request.POST.get("comments"),
               'condition_data': condition_data, 'pump_data': pumping_data, 'survey1': fillsurveys1.name,
               'survey2': '' if request.POST.get('survey2') == '' else fillsurveys2.name,
               'schema': None}
    pdffile = generate_well_pumping_acts(elements=context)

    if save == False:
        return HttpResponse(base64.b64encode(pdffile).decode("utf-8"))
    else:
        return pdffile


@login_required
def wp_prepopulated(request):
    """Предзаполняем форму для новых записей инспекции, чтобы упростить ввод данных"""
    well_id = request.GET.get('well', None)
    exclude = ['well', 'date', 'survey1', 'survey2', 'doc', 'agreed']
    dict_kwargs = {'well_id': well_id}
    columns = [f.name for f in WellsPumping._meta.get_fields() if f.name not in exclude]
    if WellsPumping.objects.filter(**dict_kwargs).exists():
        max_date = WellsPumping.objects.filter(**dict_kwargs).latest('date').date
        data = WellsPumping.objects.filter(**dict_kwargs, date=max_date).values(*columns)[0]
    else:
        data = {key: None for key in columns}
    return JsonResponse(data, safe=False)
