from django.shortcuts import render
from .forms import *
from django.http import JsonResponse
from .models import *
from django.forms import formset_factory, modelformset_factory
from django.core.paginator import Paginator
from .filters import *


def recon_points_survey_init(request):
    recon_point_list = ReconPointsSurvey.objects.all()
    filter = ReconPointsSurveyFilter(request.GET, queryset=recon_point_list)
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recon_points_survey/recon_points_survey_init.html',
                  {'filter': filter, 'page_obj': page_obj})


def recon_points_survey_create(request):
    form_field = FileFieldForm()
    if request.method == 'POST':
        form_recon_points_survey = ReconPointsSurveyForm(request.POST)
        recon_point_id = form_recon_points_survey['recon_point'].value()
        date = form_recon_points_survey['date'].value()
        eps_data = ReconPointsSurvey(recon_point_id=recon_point_id, date=date)
        form_recon_points_survey = ReconPointsSurveyForm(data=request.POST, instance=eps_data)
        if form_recon_points_survey.is_valid():
            form_recon_points_survey.save()
    else:
        form_recon_points_survey = ReconPointsSurveyForm()
        form_field = FileFieldForm()
    return render(request, "recon_points_survey/recon_points_survey.html",
                  context={'form_recon_points_survey': form_recon_points_survey, 'form_field': form_field})


def recon_points_survey_edit(request,pk):
    """Редактирование записи инспекции скважины"""
    instance_recon_point_survey = ReconPointsSurvey.objects.get(pk=pk)
    form_field = FileFieldForm()
    if request.method == 'POST':
        form_recon_point_survey = ReconPointsSurveyForm(data=request.POST, instance=instance_recon_point_survey)
        if form_recon_point_survey.is_valid():
            form_recon_point_survey.save()
    else:
        form_recon_point_survey = ReconPointsSurveyForm(instance=instance_recon_point_survey)

    return render(request, "recon_points_survey/recon_points_survey_edit.html",
                  context={'form_recon_points_survey': form_recon_point_survey, 'form_field': form_field})


def rss_prepopulated(request):
    data = {}
    recon_site_id = request.GET.get('recon_site_id', None)
    creation_date = request.GET.get('creation_date', None)
    date_survey = []
    instance = ReconPointsSurvey.objects.select_related('recon_point__recon_site').filter(
        recon_point__recon_site=recon_site_id, doc__isnull=True).values()
    if len(list(instance)) == 0:
        instance = ReconPointsSurvey.objects.select_related('doc__creation_date').filter(
            recon_point__recon_site=recon_site_id, doc__isnull=False, doc__doc__creation_date=creation_date).values()

    if ReconSitesSurvey.objects.select_related('doc__creation_date').filter(recon_site=recon_site_id,
                                                                            doc__isnull=False,
                                                                            doc__creation_date=creation_date).exists():
        instance_site = ReconSitesSurvey.objects.select_related('doc__creation_date').filter(recon_site=recon_site_id,
                                                                                             doc__isnull=False,
                                                                                             doc__creation_date=creation_date).values()[
            0]
        del instance_site['recon_site_id']
        del instance_site['objectid']
        del instance_site['doc_id']

        change_key_data = ('survey1', 'survey2')
        if change_key_data is not None:
            for key in change_key_data:
                instance_site[key] = instance_site.pop(key + '_id')
        data.update(instance_site)
    keys = ['recon_point_id', 'date']
    for i, quer in enumerate(list(instance)):
        date_survey.append(quer['date'])
        dict = {your_key: quer[your_key] for your_key in keys}
        for keysmy in keys:
            dict['form-' + str(i) + '-' + keysmy.replace('_id', '')] = dict.pop(keysmy)
        data.update(dict)

    data_len = {'queryset': len(list(instance))}

    data.update(data_len)

    return JsonResponse(data, safe=False)


def recon_sites_survey_init(request):
    filter = ReconSitesSurveyFilter(request.GET,
                                    queryset=ReconSitesSurvey.objects.values('recon_site_id', 'doc__creation_date','pk'))
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recon_sites_survey/recon_sites_survey_init.html',
                  {'filter': filter, 'page_obj': page_obj})


def recon_sites_survey_create(request):
    try:
        form_recon_points_survey = formset_factory(ReconPointsSurveyForm)

        if request.method == 'POST':
            form_recon_points_survey = form_recon_points_survey(request.POST)
            form_field = FileFieldForm(request.POST)
            form_recon_sites = ReconSitesForm(request.POST)
            form_documents = DocumentsForm(request.POST)
            recon_site_id = form_recon_sites['recon_site_id'].value()
            date = form_documents['creation_date'].value()
            if Documents.objects.all().exists():
                doc_id = Documents.objects.latest('doc_id').doc_id + 1
            else:
                doc_id = 1

            ess_data = ReconSitesSurvey(recon_site_id=recon_site_id, doc_id=doc_id)
            form_recon_sites_survey = ReconSitesSurveyForm(data=request.POST, instance=ess_data)
            recon_site_instance = ReconSites.objects.get(recon_site_id=recon_site_id)
            form_recon_sites = ReconSitesForm(data=request.POST, instance=recon_site_instance)
            if form_recon_sites_survey.is_valid() and form_recon_sites.is_valid:
                Documents(doc_id=doc_id, doc_type=1900, reg_status=0, creation_date=date).save()
                form_recon_sites_survey.save()
                form_recon_sites.save()
                for form_parent in form_recon_points_survey:
                    instance = ReconPointsSurvey.objects.get(recon_point_id=form_parent['recon_point'].value(),
                                                           date=form_parent['date'].value())
                    instance.doc_id = doc_id
                    instance.save()

        else:
            form_recon_sites_survey = ReconSitesSurveyForm()
            form_recon_sites = ReconSitesForm()
            form_field = FileFieldForm()
            form_survey = ReconPointsSurveyForm()
            form_recon_points_survey = form_recon_points_survey()
            form_documents = DocumentsForm()
        return render(request, "recon_sites_survey/recon_sites_survey.html",
                      context={'form_recon_sites_survey': form_recon_sites_survey, 'form_field': form_field,
                               'form_recon_sites': form_recon_sites,
                               'form_recon_points_survey': form_recon_points_survey, 'form_survey': form_survey,
                               'form_documents': form_documents})
    except:
        form_recon_points_survey = formset_factory(ReconPointsSurveyForm)
        form_recon_sites_survey = ReconSitesSurveyForm()
        form_recon_sites = ReconSitesForm()
        form_field = FileFieldForm()
        form_survey = ReconPointsSurveyForm()
        form_recon_points_survey = form_recon_points_survey()
        form_documents = DocumentsForm()
    return render(request, "recon_sites_survey/recon_sites_survey.html",
                  context={'form_recon_sites_survey': form_recon_sites_survey, 'form_field': form_field,
                           'form_recon_sites': form_recon_sites, 'form_recon_points_survey': form_recon_points_survey,
                           'form_survey': form_survey, 'form_documents': form_documents})


def recon_sites_survey_edit(request, pk):
    """Редактирование записи инспекции скважины"""
    instance_recon_site_survey = ReconSitesSurvey.objects.get(pk=pk)
    instance_recon_points_survey = ReconPointsSurvey.objects.filter(recon_point__recon_site=instance_recon_site_survey.recon_site_id,
                                                                    doc_id=instance_recon_site_survey.doc_id)
    instance_recon_sites = ReconSites.objects.get(recon_site_id=instance_recon_site_survey.recon_site_id)
    instance_documents = Documents.objects.get(doc_id=instance_recon_site_survey.doc_id)
    form_documents = DocumentsForm(instance=instance_documents)
    formset = modelformset_factory(ReconPointsSurvey, form=ReconPointsSurveyForm, extra=0)
    form_field = FileFieldForm()
    form_survey = ReconPointsSurveyForm()
    if request.method == 'POST':
        form_recon_sites_survey = ReconSitesSurveyForm(data=request.POST, instance=instance_recon_site_survey)
        form_recon_points_survey = formset(request.POST, queryset=instance_recon_points_survey)
        form_recon_sites = ReconSitesForm(data=request.POST, instance=instance_recon_sites)
        if form_recon_sites_survey.is_valid():
            form_recon_sites_survey.save()
            form_recon_sites.save()
    else:

        form_recon_sites_survey = ReconSitesSurveyForm(instance=instance_recon_site_survey)
        form_recon_points_survey = formset(queryset=instance_recon_points_survey)
        form_recon_sites = ReconSitesForm(instance=instance_recon_sites)

    return render(request, "recon_sites_survey/recon_sites_survey_edit.html",
                  context={'form_recon_sites_survey': form_recon_sites_survey,
                           'form_recon_sites': form_recon_sites,
                           'form_documents': form_documents,
                           'form_recon_points_survey': form_recon_points_survey,
                           'form_survey': form_survey,
                           'form_field': form_field})
