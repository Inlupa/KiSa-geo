import os
import base64
from functools import reduce
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .filters import *
from .forms import *
from .models import *
from .act_generator import generate_well_inspection_acts

DOC_TYPE = 1001
PATH_DOC = r'\\tech-geo\fgi\FUND\wells'


@login_required
def wells_inspection_init(request):
    wells_inspection_list = WellsInspection.objects.all()
    doc_filter = WellsInspectionFilter(request.GET, queryset=wells_inspection_list)
    paginator = Paginator(doc_filter.qs, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'wells_inspection/wells_inspection_in.html',
                  {'filter': doc_filter, 'page_obj': page_obj})


@login_required
def wells_inspection_create(request):
    if request.method == 'POST':
        form_wells_inspection = WellsInspectionForm(request.POST)
        files = request.FILES.getlist('file_field')
        well_id = form_wells_inspection['well'].value()
        date = form_wells_inspection['date'].value()
        survey = form_wells_inspection['survey1'].value()
        doc_id = Documents.objects.all().aggregate(Max('doc_id'))['doc_id__max'] + 1

        default_measure = {'well_id': well_id, 'date': date, 'doc_id': doc_id, 'survey_id': survey}
        default_survey = dict(default_measure)
        default_survey.pop('survey_id', None)

        wi_data = WellsInspection(**default_survey)
        form_wells_inspection = WellsInspectionForm(data=request.POST, instance=wi_data)

        ww_data = WellsWaterdepth(**default_measure)
        form_wells_waterdepth = WellsWaterdepthForm(data=request.POST, instance=ww_data)

        wt_data = WellsTemperature(**default_measure)
        form_wells_temperature = WellsTemperatureForm(data=request.POST, instance=wt_data)

        wc_data = WellsCondition(**default_survey)
        form_wells_condition = WellsConditionForm(data=request.POST, instance=wc_data)

        wd_data = WellsDepth(**default_survey)
        form_wells_depth = WellsDepthForm(data=request.POST, instance=wd_data)

        wl_data = WellsLugheight(**default_survey)
        form_wells_lugheight = WellsLugheightForm(data=request.POST, instance=wl_data)

        check_condition = reduce((lambda x, y: x * y),
                                 [form_wells_inspection.is_valid(), form_wells_waterdepth.is_valid(),
                                  form_wells_temperature.is_valid(), form_wells_condition.is_valid(),
                                  form_wells_depth.is_valid(), form_wells_lugheight.is_valid()])

        if check_condition:
            path_documents = os.path.join(PATH_DOC, well_id, str(doc_id))
            is_exist = os.path.exists(path_documents)
            if not is_exist:
                os.makedirs(path_documents)

            name_pdf, pages = wi_generate_acts(request, True, doc_id)
            doc_name = 'Акт инспекции скважины №{0} от {1}'.format(well_id, str(date))
            author1 = Workers.objects.get(worker_id=survey).name
            survey2 = request.POST.get('survey2')
            author2 = Workers.objects.get(worker_id=survey2).name if survey2 != '' else None
            default_documents = {'doc_id': doc_id, 'doc_type': DOC_TYPE, 'creation_org': 1, 'creation_date': now(),
                                 'reg_status': 0, 'digital_version': True, 'number_of_pages': pages,
                                 'number_of_graphic': 0, 'doc_name': doc_name, 'author1': author1, 'author2': author2}

            Documents(**default_documents).save()
            form_wells_inspection.save()
            form_wells_condition.save()
            form_wells_lugheight.save()
            form_wells_waterdepth.save() if form_wells_waterdepth['water_depth'].value() != '' else None
            form_wells_depth.save() if form_wells_depth['depth'].value() != '' else None
            form_wells_temperature.save() if form_wells_temperature['temperature'].value() != '' else None

            DocumentsPath(rel_doc_id=doc_id, att_name=name_pdf, path=path_documents).save()
            for i in files:
                DocumentsPath(rel_doc_id=doc_id, att_name=i.name, path=path_documents).save()
            return HttpResponseRedirect('/wells_inspection')

    form_wells_inspection = WellsInspectionForm()
    form_wells_waterdepth = WellsWaterdepthForm()
    form_wells_temperature = WellsTemperatureForm()
    form_wells_condition = WellsConditionForm()
    form_wells_depth = WellsDepthForm()
    form_wells_lugheight = WellsLugheightForm()
    form_field = FileFieldForm()
    return render(request, "wells_inspection/wells_inspection.html",
                  context={'form_wells_inspection': form_wells_inspection,
                           'form_wells_waterdepth': form_wells_waterdepth,
                           'form_wells_temperature': form_wells_temperature,
                           'form_wells_condition': form_wells_condition,
                           'form_wells_lugheight': form_wells_lugheight,
                           'form_wells_depth': form_wells_depth,
                           'form_field': form_field, })


@login_required
def wells_inspection_edit(request, pk):
    instance_wells_inspection = WellsInspection.objects.get(pk=pk)
    doc_id = instance_wells_inspection.doc_id
    well_id = instance_wells_inspection.well_id
    date = instance_wells_inspection.date
    default_non_exist = {'well_id': well_id, 'date': date, 'doc_id': doc_id}
    default_exist = dict(default_non_exist)
    default_exist.pop('doc_id', None)

    try:
        instance_wells_waterdepth = WellsWaterdepth.objects.get(**default_exist)
    except WellsWaterdepth.DoesNotExist:
        instance_wells_waterdepth = WellsWaterdepth(**default_non_exist)
    try:
        instance_wells_temperature = WellsTemperature.objects.get(**default_exist)
    except WellsTemperature.DoesNotExist:
        instance_wells_temperature = WellsTemperature(**default_non_exist)
    try:
        instance_wells_condition = WellsCondition.objects.get(**default_exist)
    except WellsCondition.DoesNotExist:
        instance_wells_condition = WellsCondition(**default_non_exist)
    try:
        instance_wells_depth = WellsDepth.objects.get(**default_exist)
    except WellsDepth.DoesNotExist:
        instance_wells_depth = WellsDepth(**default_non_exist)
    instance_wells_lugheight = WellsLugheight.objects.get(**default_exist)

    # FIXME: переделать подтягивание документов
    instance_attach = DocumentsPath.objects.filter(rel_doc_id=doc_id)
    # if DocumentsAttach.objects.filter(rel_doc_id=doc_id).exists():
    #     pdfcreate = query_result(
    #         'select encode(data,\'base64\') from geology.documents_attach where rel_doc_id=\'' + str(
    #             doc_id) + '\'')
    #     pdffile = pdfcreate[0][0]
    # else:
    #     pdffile = None
    # for i in instance_attach:
    #     i.data = base64.b64encode(bytes(i.data)).decode('utf-8')

    if request.method == 'POST':
        form_wells_inspection = WellsInspectionForm(data=request.POST, instance=instance_wells_inspection)
        form_wells_waterdepth = WellsWaterdepthForm(data=request.POST, instance=instance_wells_waterdepth)
        form_wells_temperature = WellsTemperatureForm(data=request.POST, instance=instance_wells_temperature)
        form_wells_condition = WellsConditionForm(data=request.POST, instance=instance_wells_condition)
        form_wells_depth = WellsDepthForm(data=request.POST, instance=instance_wells_depth)
        form_wells_lugheight = WellsLugheightForm(data=request.POST, instance=instance_wells_lugheight)

        check_condition = reduce((lambda x, y: x * y),
                                 [form_wells_inspection.is_valid(), form_wells_waterdepth.is_valid(),
                                  form_wells_temperature.is_valid(), form_wells_condition.is_valid(),
                                  form_wells_depth.is_valid(), form_wells_lugheight.is_valid()])

        if check_condition:
            path_documents = os.path.join(PATH_DOC, well_id, str(doc_id))
            is_exist = os.path.exists(path_documents)
            if not is_exist:
                os.makedirs(path_documents)

            survey1 = request.POST.get('survey1')
            author1 = Workers.objects.get(worker_id=survey1).name
            survey2 = request.POST.get('survey2')
            author2 = Workers.objects.get(worker_id=survey2).name if survey2 != '' else None
            name_pdf, pages = wi_generate_acts(request, True, doc_id)

            current_doc = Documents.objects.get(doc_id=doc_id)
            current_doc.pages = pages
            current_doc.author1 = author1
            current_doc.author2 = author2
            current_doc.save()

            form_wells_inspection.save()
            form_wells_condition.save()
            form_wells_lugheight.save()
            form_wells_waterdepth.save() if form_wells_waterdepth['water_depth'].value() != '' else None
            form_wells_depth.save() if form_wells_depth['depth'].value() != '' else None
            form_wells_temperature.save() if form_wells_temperature['temperature'].value() != '' else None

            files = request.FILES.getlist('file_field')
            for i in files:
                DocumentsPath(rel_doc_id=doc_id, att_name=i.name, path=path_documents).save()

            return HttpResponseRedirect('/wells_inspection')

    form_wells_inspection = WellsInspectionForm(instance=instance_wells_inspection)
    form_wells_waterdepth = WellsWaterdepthForm(instance=instance_wells_waterdepth)
    form_wells_temperature = WellsTemperatureForm(instance=instance_wells_temperature)
    form_wells_condition = WellsConditionForm(instance=instance_wells_condition)
    form_wells_depth = WellsDepthForm(instance=instance_wells_depth)
    form_wells_lugheight = WellsLugheightForm(instance=instance_wells_lugheight)
    file_attach = FileFieldForm()

    return render(request, "wells_inspection/wells_inspection_edit.html",
                  context={'form_wells_inspection': form_wells_inspection,
                           'form_wells_waterdepth': form_wells_waterdepth,
                           'form_wells_temperature': form_wells_temperature,
                           'form_wells_condition': form_wells_condition,
                           'form_wells_lugheight': form_wells_lugheight,
                           'form_wells_depth': form_wells_depth,
                           'form_wi_attach': instance_attach,
                           'pdffile': pdffile,
                           'fieldform': file_attach})


@login_required
def wi_prepopulated(request):
    well_id = request.GET.get('well', None)
    exclude = ['well', 'date', 'survey1', 'survey2', 'doc', 'agreed', 'wellsinspectionattach']
    dict_kwargs = {'well_id': well_id}
    columns = [f.name for f in WellsInspection._meta.get_fields() if f.name not in exclude]
    if WellsInspection.objects.filter(**dict_kwargs).exists():
        max_date = WellsInspection.objects.filter(**dict_kwargs).latest('date').date
        data = WellsInspection.objects.filter(**dict_kwargs, date=max_date).values(*columns)[0]
    else:
        data = {key: None for key in columns}
    return JsonResponse(data, safe=False)


@login_required
def wi_generate_acts(request, save=False, doc_id=None):
    well_id = request.POST.get('well')
    date = request.POST.get('date')
    pdffile = generate_well_inspection_acts(request)
    name_pdf = '{0}_{1}.pdf'.format(well_id, date)
    if save:
        pdffile.output(os.path.join(PATH_DOC, well_id, str(doc_id), name_pdf))
        return name_pdf, pdffile.page_no()

    return HttpResponse(base64.b64encode(bytes(pdffile.output())).decode("utf-8"))


@login_required
def wi_delete_attach(request, attachmentid):
    """Удаляет вложения фотодокументации"""
    wi_data = get_object_or_404(WellsInspectionAttach, attachmentid=attachmentid)
    wi_data.delete()
    return HttpResponse()
