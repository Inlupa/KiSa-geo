import io
import base64
import datetime
from babel.dates import format_date
from plpygis import Geometry
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Max
from .filters import *
from .forms import *
from .models import *
from .act_generator import generate_spring_inspection_acts


def query_result(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        value = cursor.fetchall()
        return value


@login_required
def springs_inspection_init(request):
    """Достаем все записи в таблице инспекций и закидываем в html страницу"""
    springs_inspection_list = SpringsInspection.objects.all()
    doc_filter = SpringsInspectionFilter(request.GET, queryset=springs_inspection_list)
    paginator = Paginator(doc_filter.qs, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'springs_inspection/springs_inspection_init.html',
                  {'filter': doc_filter, 'page_obj': page_obj})


@login_required
def springs_inspection_create(request):
    form_field = FileFieldForm()
    if request.method == 'POST':
        form_springs_inspection = SpringsInspectionForm(request.POST)
        spring_id = form_springs_inspection['spring'].value()
        date = form_springs_inspection['date'].value()
        survey = form_springs_inspection['survey1'].value()
        doc_id = Documents.objects.all().aggregate(Max('doc_id'))['doc_id__max']+1
        ss_data = SpringsSample(doc_id=doc_id,spring_id=spring_id,date=date)
        form_springs_sample = SpringsSampleForm(data=request.POST, instance=ss_data)

        si_data = SpringsInspection(spring_id=spring_id, date=date, doc_id=doc_id)
        form_springs_inspection = SpringsInspectionForm(data=request.POST, instance=si_data)

        sw_data = SpringsRate(doc_id=doc_id, survey_id=survey, date=date, spring_id=spring_id)
        form_springs_rate = SpringsRateForm(data=request.POST, instance=sw_data)

        st_data = SpringsTemperature(doc_id=doc_id, survey_id=survey, date=date, spring_id=spring_id)
        form_springs_temperature = SpringsTemperatureForm(data=request.POST, instance=st_data)

        objectid = si_data.doc_id
        if form_springs_inspection.is_valid() and form_springs_rate.is_valid() and form_springs_temperature.is_valid() and form_springs_sample.is_valid():
            Documents(doc_id=doc_id, doc_type=1002, reg_status=0, creation_date=now()).save()
            form_springs_inspection.save()
            form_springs_rate.save() if form_springs_rate['spring_rate'].value() != '' else None
            form_springs_temperature.save() if form_springs_temperature['temperature'].value() != '' else None
            form_springs_sample.save() if form_springs_sample['sample_name'].value() != '' else None

            DocumentsAttach(rel_doc_id=Documents.objects.get(doc_id=doc_id).doc_id,
                            att_name=str(spring_id) + '_' + str(
                                date) + '.pdf',
                            data=si_generate_acts(request, True)).save()
            files = request.FILES.getlist('file_field')
            for i in files:
                i.seek(0)
                SpringsInspectionAttach(rel_doc_id=objectid, att_name=i.name, data=i.read()).save()

            return HttpResponseRedirect('/springs_inspection')
    else:
        form_springs_inspection = SpringsInspectionForm()
        form_springs_rate = SpringsRateForm()
        form_springs_temperature = SpringsTemperatureForm()
        form_springs_sample = SpringsSampleForm()

    return render(request, "springs_inspection/springs_inspection.html",
                  context={'form_springs_inspection': form_springs_inspection,
                           'form_springs_rate': form_springs_rate,
                           'form_springs_temperature': form_springs_temperature,
                           'form_springs_sample': form_springs_sample,
                           'form_field': form_field})


@login_required
def springs_inspection_edit(request, pk):
    """Редактирование записи инспекции скважины"""
    instance_springs_inspection = SpringsInspection.objects.get(pk=pk)
    doc_id=instance_springs_inspection.doc_id
    spring_id = instance_springs_inspection.spring_id
    date = instance_springs_inspection.date
    try:
        instance_springs_rate = SpringsRate.objects.get(spring_id=spring_id, date=date)
    except SpringsRate.DoesNotExist:
        instance_springs_rate = SpringsRate(spring_id=spring_id, date=date,doc_id=doc_id)
    try:
        instance_springs_temperature = SpringsTemperature.objects.get(spring_id=spring_id, date=date)
    except SpringsTemperature.DoesNotExist:
        instance_springs_temperature = SpringsTemperature(spring_id=spring_id, date=date,doc_id=doc_id)

    try:
        instance_springs_sample = SpringsSample.objects.get(doc_id=doc_id)
    except SpringsSample.DoesNotExist:
        instance_springs_sample = SpringsSample(doc_id=doc_id,spring_id=spring_id, date=date)
    instance_si_attach = SpringsInspectionAttach.objects.filter(rel_doc_id=doc_id)
    if DocumentsAttach.objects.filter(rel_doc_id=str(doc_id)).exists():
        pdfcreate = query_result(
            'select encode(data,\'base64\') from geology.documents_attach where rel_doc_id=\'' + str(
                doc_id) + '\'')
        pdffile = pdfcreate[0][0]
        for i in instance_si_attach:
            i.data = base64.b64encode(bytes(i.data)).decode('utf-8')
    else:
        pdffile = None

    if request.method == 'POST':
        form_springs_inspection = SpringsInspectionForm(data=request.POST, instance=instance_springs_inspection)
        form_springs_rate = SpringsRateForm(data=request.POST, instance=instance_springs_rate)
        form_springs_temperature = SpringsTemperatureForm(data=request.POST,
                                                          instance=instance_springs_temperature)
        form_springs_sample = SpringsSampleForm(data=request.POST, instance=instance_springs_sample)

        file_attach = FileFieldForm()
        if form_springs_inspection.is_valid() and form_springs_rate.is_valid() and form_springs_temperature.is_valid() and form_springs_sample.is_valid():
            form_springs_inspection.save()
            form_springs_rate.save() if form_springs_rate['spring_rate'].value() != '' else None
            form_springs_temperature.save() if form_springs_temperature['temperature'].value() != '' else None
            form_springs_sample.save() if form_springs_sample['sample_name'].value() != '' else None

            instance_doc_attach = DocumentsAttach.objects.get(rel_doc_id=doc_id)
            instance_doc_attach.data = si_generate_acts(request, True)
            instance_doc_attach.save()

            files = request.FILES.getlist('file_field')
            for i in files:
                i.seek(0)
                SpringsInspectionAttach(rel_doc_id=doc_id,
                                        att_name=i.name, data=i.read()).save()
            return HttpResponseRedirect('/springs_inspection')
    else:
        form_springs_inspection = SpringsInspectionForm(instance=instance_springs_inspection)
        form_springs_rate = SpringsRateForm(instance=instance_springs_rate)
        form_springs_temperature = SpringsTemperatureForm(instance=instance_springs_temperature)
        form_springs_sample = SpringsSampleForm(instance=instance_springs_sample)
        file_attach = FileFieldForm()

    return render(request, "springs_inspection/springs_inspection_edit.html",
                  context={'form_springs_inspection': form_springs_inspection,
                           'form_springs_rate': form_springs_rate,
                           'form_springs_temperature': form_springs_temperature,
                           'form_springs_sample': form_springs_sample,
                           'form_si_attach': instance_si_attach,
                           'pdffile': pdffile,
                           'form_field': file_attach})


@login_required
def si_prepopulated(request):
    spring_id = request.GET.get('spring', None)
    dict_kwargs = {'spring_id': spring_id}
    exclude = ['spring', 'date', 'survey1', 'survey2', 'doc', 'sample', 'agreed', 'springssample',
               'springsinspectionattach']
    columns = [f.name for f in SpringsInspection._meta.get_fields() if f.name not in exclude]
    if SpringsInspection.objects.filter(**dict_kwargs).exists():
        max_date = SpringsInspection.objects.filter(**dict_kwargs).latest('date').date
        data = SpringsInspection.objects.filter(**dict_kwargs, date=max_date).values(*columns)[0]
    else:
        data = {key: None for key in columns}
    return JsonResponse(data, safe=False)


@login_required
def si_generate_acts(request, save=False):
    fillactfield = Springs.objects.get(spring_id=request.POST.get("spring"))
    g = Geometry(fillactfield.geom)
    fillsurveys1 = Workers.objects.get(worker_id=request.POST.get('survey1'))
    survey_f = fillsurveys1.name
    if request.POST.get('survey2') == '':
        we = 'Я, нижеподписавшийся, сотрудник Геологической службы ГПБУ "Мосэкомониторинг": **'
        survey_f += '** провёл'
        we += survey_f + ' инспекцию состояния скважины и режимные наблюдения.'
    else:
        we = 'Мы, нижеподписавшиеся, сотрудники Геологической службы ГПБУ "Мосэкомониторинг": **'
        fillsurveys2 = Workers.objects.get(worker_id=request.POST.get('survey2'))
        survey_s = ' и ' + fillsurveys2.name + '** провели'
        we += survey_f + survey_s + ' обследование родника.'

    files = request.FILES.getlist('file_field')
    images = []
    if SpringsInspection.objects.filter(spring_id=request.POST.get('spring'),
                                        date=request.POST.get('date')).exists():
        instance_drawwells_inspection = SpringsInspection.objects.get(spring_id=request.POST.get('spring'),
                                                                      date=request.POST.get('date'))
        instance_di_attach = SpringsInspectionAttach.objects.filter(
            rel_doc_id=instance_drawwells_inspection.doc_id)

        for img in instance_di_attach:
            images.append(io.BytesIO(bytes(img.data)))
    for img in files:
        images.append(img)

    condition_data = (
        ("Показатель", "Год"),
        ("Описание благоустройства", request.POST.get("captage_description")),
        ("Санитарное состояние прилегающей территории", request.POST.get("area_description")),
        ("Дебит родника, л/сек", request.POST.get("spring_rate")),
        ("Температура воды", request.POST.get("temperature")),
        ("Отбор проб", request.POST.get("sample_name")),
    )
    context = {'date': format_date(datetime.datetime.strptime(request.POST.get("date"), '%Y-%m-%d'), "d MMMM yyyy",
                                   locale='ru'), 'well': request.POST.get("spring"),
               'position': str(fillactfield.position),
               'x': str(round(g.x, 6)), 'y': str(round(g.y, 6)), 'name': str(fillactfield.spring_name),
               'weather': request.POST.get("weather"),
               'type': fillactfield.spring_type, 'function': fillactfield.regime,
               'usage': request.POST.get("usage"),
               'geomorph': str(fillactfield.geomorph), 'aquifer': str(fillactfield.aquifer),
               'lithology': str(fillactfield.aquifer),
               'comments': request.POST.get("comments"), 'recommendations': request.POST.get("recommendations"),
               'images': images, 'condition_data': condition_data,
               'survey1': fillsurveys1.name,
               'survey2': '' if request.POST.get('survey2') == '' else fillsurveys2.name,
               'schema': None, 'we': we}
    pdffile = generate_spring_inspection_acts(elements=context)
    if save == False:
        return HttpResponse(base64.b64encode(pdffile).decode("utf-8"))
    else:
        return pdffile


@login_required
def si_delete_attach(request, attachmentid):
    """Удаляет вложения фотодокументации"""
    si_data = get_object_or_404(SpringsInspectionAttach, attachmentid=attachmentid)
    si_data.delete()
    return HttpResponse()
