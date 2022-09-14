from django.db import models

category_3 = { 0: 'Неудовлетворительное',1: 'Удовлетворительное', 2: 'Хорошее'}
category_3 = tuple(map(tuple, category_3.items()))

wells_condition = {1: 'Действующая', 2: 'Резервная', 3: 'Недействующая', 4: 'Законсервированная', 5: 'Неисправная',
                   6: 'Заброшенная', 7: 'Ликвидированная', 8: 'Проектная', 9: 'Пробурена'}
wells_condition = tuple(map(tuple, wells_condition.items()))


class WellsInspection(models.Model):
    well = models.ForeignKey('Wells', models.CASCADE)
    date = models.DateField()
    survey1 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey1', related_name='survey1')
    survey2 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey2', related_name='survey2', blank=True, null=True)
    weather = models.CharField(max_length=50, blank=True, null=True)
    painting_condition = models.SmallIntegerField(choices=category_3)
    lable_condition = models.SmallIntegerField(choices=category_3)
    well_lug_condition = models.SmallIntegerField(choices=category_3)
    well_head_condition = models.SmallIntegerField(choices=category_3)
    well_collar_condition = models.SmallIntegerField(choices=category_3)
    damage_status = models.BooleanField()
    damage_description = models.CharField(max_length=150, blank=True, null=True)
    automation_status = models.BooleanField()
    automation_condition = models.SmallIntegerField(choices=category_3,blank=True, null=True)
    automation_description = models.CharField(max_length=100, blank=True, null=True)
    area_condition = models.SmallIntegerField(choices=category_3)
    area_description = models.CharField(max_length=300, blank=True, null=True)
    logs_status = models.BooleanField()
    logs_results = models.CharField(max_length=150, blank=True, null=True)
    comments = models.CharField(max_length=150, blank=True, null=True)
    recommendations = models.CharField(max_length=300, blank=True, null=True)
    agreed = models.ForeignKey('Workers', models.DO_NOTHING, db_column='agreed', related_name='agreed', blank=True, null=True)
    doc = models.OneToOneField('Documents', models.CASCADE, primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_inspection'
        unique_together = (('well', 'date'),)
        ordering = ('-date',)


class Wells(models.Model):
    well_id = models.IntegerField(primary_key=True)
    well_name = models.CharField(max_length=50, blank=True, null=True)
    well_type = models.SmallIntegerField()
    position = models.CharField(max_length=300, blank=True, null=True)
    geomorph = models.CharField(max_length=300, blank=True, null=True)
    head = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    aquifer = models.ForeignKey('AquiferCodes', models.DO_NOTHING, blank=True, null=True)
    moved = models.SmallIntegerField()
    subsurface_site = models.ForeignKey('SubsurfaceSites', models.DO_NOTHING, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wells'


class WellsWaterdepth(models.Model):
    well = models.ForeignKey(Wells, models.CASCADE)
    date = models.DateField()
    survey = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey', blank=True, null=True)
    water_depth = models.DecimalField(max_digits=6, decimal_places=2)
    doc = models.ForeignKey('Documents', models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_waterdepth'
        unique_together = (('date', 'well'),)


class WellsTemperature(models.Model):
    well = models.ForeignKey(Wells, models.CASCADE)
    date = models.DateField()
    survey = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey', blank=True, null=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    doc = models.ForeignKey('Documents', models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_temperature'
        unique_together = (('date', 'well'),)


class Documents(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_type = models.SmallIntegerField()
    reg_status = models.SmallIntegerField()
    reg_number = models.CharField(max_length=20, blank=True, null=True)
    reg_date = models.DateField(blank=True, null=True)
    reg_worker = models.ForeignKey('Workers', models.DO_NOTHING, db_column='reg_worker', blank=True, null=True)
    doc_source = models.SmallIntegerField(blank=True, null=True)
    doc_name = models.CharField(max_length=50, blank=True, null=True)
    creation_org = models.CharField(max_length=50, blank=True, null=True)
    author1 = models.CharField(max_length=25, blank=True, null=True)
    author2 = models.CharField(max_length=25, blank=True, null=True)
    author3 = models.CharField(max_length=25, blank=True, null=True)
    author4 = models.CharField(max_length=25, blank=True, null=True)
    creation_place = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    number_of_pages = models.SmallIntegerField(blank=True, null=True)
    number_of_graphic = models.SmallIntegerField(blank=True, null=True)
    paper_version = models.BooleanField(blank=True, null=True)
    digital_version = models.BooleanField(blank=True, null=True)
    secrecy = models.SmallIntegerField(blank=True, null=True)
    storage = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'
        unique_together = (('doc_name', 'doc_type', 'creation_date'),)


class AquiferCodes(models.Model):
    aquifer_id = models.SmallIntegerField(primary_key=True)
    aquifer_name = models.CharField(max_length=150)
    aquifer_index = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'aquifer_codes'


class Workers(models.Model):
    worker_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    name_1 = models.CharField(max_length=50)
    name_2 = models.CharField(max_length=50)
    name_3 = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    post = models.IntegerField()
    unit = models.IntegerField()
    phone_personal = models.CharField(max_length=20, blank=True, null=True)
    phone_work = models.SmallIntegerField(blank=True, null=True)
    e_mail = models.CharField(max_length=50, blank=True, null=True)
    e_mail_work = models.CharField(max_length=50)
    login = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'workers'

    def __str__(self):
        return self.name



class WellsLugheight(models.Model):
    well = models.ForeignKey(Wells, models.CASCADE)
    date = models.DateField()
    lug_height = models.DecimalField(max_digits=4, decimal_places=2)
    doc = models.ForeignKey(Documents, models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_lugheight'
        unique_together = (('well', 'date'),)


class WellsDepth(models.Model):
    well = models.ForeignKey(Wells, models.CASCADE)
    date = models.DateField()
    depth = models.DecimalField(max_digits=6, decimal_places=2)
    doc = models.ForeignKey(Documents, models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_depth'
        unique_together = (('date', 'well'),)


class WellsCondition(models.Model):
    well = models.ForeignKey(Wells, models.CASCADE)
    date = models.DateField()
    condition = models.SmallIntegerField(choices=wells_condition)
    doc = models.ForeignKey(Documents, models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_condition'
        unique_together = (('date', 'well'),)


class DocumentsAttach(models.Model):
    attachmentid = models.AutoField(primary_key=True)
    rel_doc = models.ForeignKey(Documents, models.CASCADE)
    att_name = models.CharField(max_length=250)
    data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents_attach'
        unique_together = (('rel_doc', 'att_name'),)


class DocumentsPath(models.Model):
    attachmentid = models.AutoField(primary_key=True)
    rel_doc = models.ForeignKey(Documents, models.CASCADE)
    att_name = models.CharField(max_length=250)
    path = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'documents_path'
        unique_together = (('rel_doc', 'att_name'),)


class WellsInspectionAttach(models.Model):
    attachmentid = models.AutoField(primary_key=True)
    rel_doc = models.ForeignKey(WellsInspection, models.CASCADE)
    att_name = models.CharField(max_length=250)
    data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wells_inspection_attach'
        unique_together = (('att_name', 'rel_doc'),)


class WellsConstruction(models.Model):
    well = models.ForeignKey(Wells, models.CASCADE)
    construction_type = models.SmallIntegerField()
    diameter = models.SmallIntegerField()
    depth_from = models.DecimalField(max_digits=6, decimal_places=2)
    depth_till = models.DecimalField(max_digits=6, decimal_places=2)
    doc = models.ForeignKey(Documents, models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wells_construction'
        unique_together = (('well', 'depth_from', 'construction_type', 'depth_till', 'diameter'),)


class SubsurfaceSites(models.Model):
    subsurface_site_id = models.IntegerField(primary_key=True)
    subsurface_site_name = models.CharField(max_length=100, blank=True, null=True)
    mineral = models.SmallIntegerField(blank=True, null=True)
    deposit_site_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    deposit = models.ForeignKey('FieldsGeneral', models.DO_NOTHING, blank=True, null=True)
    gmsn_id = models.IntegerField(blank=True, null=True)
    uib_id = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'subsurface_sites'


class FieldsGeneral(models.Model):
    deposit_id = models.IntegerField(primary_key=True)
    deposit_name = models.CharField(unique=True, max_length=93, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'fields_general'