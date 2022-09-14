from .forms import *
from .models import *
from django.shortcuts import render
from django.http import JsonResponse

from django.forms import formset_factory, modelformset_factory


def lic_prepopulated(request):
    license_id = request.GET.get('license_id', None)
    data = {}
    doc_id = License.objects.filter(license_id=license_id).values('doc_id')
    data_init = LicenseToWells.objects.filter(license_id=doc_id[0]['doc_id']).values('well_id')
    well_id = [set['well_id'] for set in list(data_init)]
    # data_t = prepopulated_create(License, license_id, None, 'license', True)
    # data_w = prepopulated_create(LicenseToWells, well_id, None, 'license', False, formset_prepop=True, prefix='cat',
    #                              querylen=len(list(data_init)))
    # data_wel = prepopulated_create(Wells, well_id, None, 'well_main', False, formset_prepop=True, prefix='wel',
    #                              querylen=len(list(data_init)))
    # data_len = {'queryset': len(list(data_init))}
    # merge = [data_t, data_w,data_wel, data_len]
    # for d in merge:
    #     if d is not None:
    #         data.update(d)
    return JsonResponse(data, safe=False)


def license_input(request):
    form_license = LicenseForm(request.POST or None)
    formset_license = formset_factory(LicenseToWellsForm)
    # wells_formset = modelformset_factory(Wells, form=WellsForm, extra=0)
    doc_id = None
    wells_formset = formset_factory(WellsForm)
    date = None
    well_id = []
    if request.method == 'POST':
        formset_wells = wells_formset(request.POST,prefix='wel')
        formset_license = formset_license(request.POST, prefix='cat')
        license_id = form_license['license_id'].value()

        if License.objects.filter(license_id=license_id).exists():
            doc_id = License.objects.get(license_id=license_id).doc_id
        elif Documents.objects.all().exists():
            doc_id = Documents.objects.latest('doc_id').doc_id + 1
        else:
            doc_id = 1
        lic_data = instance_create(License, license_id, date, 'license', 'license', Documents, True, 4001,
                                   doc_id=doc_id)
        form_license = LicenseForm(data=request.POST, instance=lic_data)

        if form_license.is_valid():
            form_license.save()

        if formset_license.is_valid():
            # for obj in formset_license.deleted_objects:
            #     obj.delete()
            print([form.cleaned_data for form in formset_license.deleted_forms])
            for i, form_child in enumerate(formset_license):
                w_data = instance_create(LicenseToWells, doc_id, form_child['well'].value(), 'license_to_wells',
                                         'license_wells', Documents, False, None)
                form_child = LicenseToWellsForm(data=form_child.cleaned_data, instance=w_data)
                if form_child.is_valid():
                    form_child.save()
        else:
            print(formset_license.non_form_errors())
    else:
        formset_license = formset_license(prefix='cat')
        formset_wells = wells_formset(prefix='wel')

    return render(request, "license/license.html",
                  context={'form_license': form_license,
                           'formset': formset_license, 'formset_wells':formset_wells})
