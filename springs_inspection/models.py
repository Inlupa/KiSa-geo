from django.db import models

category_3 = { 0: 'Неудовлетворительное', 1: 'Удовлетворительное', 2: 'Хорошее'}
category_3 = tuple(map(tuple, category_3.items()))

usage = {0: 'Не используется', 1: 'Редко используется', 2: 'Часто используется', 3: 'Используется'}
usage = tuple(map(tuple, usage.items()))


class SpringsInspection(models.Model):
    spring = models.ForeignKey('Springs', models.CASCADE)
    date = models.DateField()
    survey1 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey1', related_name='survey1')
    survey2 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey2', related_name='survey2', blank=True, null=True)
    weather = models.CharField(max_length=100, blank=True, null=True)
    usage = models.SmallIntegerField(choices=usage)
    captage_condition = models.SmallIntegerField(choices=category_3)
    captage_description = models.CharField(max_length=300, blank=True, null=True)
    area_condition = models.SmallIntegerField(choices=category_3)
    area_description = models.CharField(max_length=300, blank=True, null=True)
    improve_description = models.CharField(max_length=150, blank=True, null=True)
    comments = models.CharField(max_length=150, blank=True, null=True)
    recommendations = models.CharField(max_length=200, blank=True, null=True)
    agreed = models.ForeignKey('Workers', models.DO_NOTHING, db_column='agreed', related_name='agreed', blank=True, null=True)
    doc = models.OneToOneField('Documents', models.CASCADE, primary_key=True)

    class Meta:
        managed = False
        db_table = 'springs_inspection'
        unique_together = (('date', 'spring'),)
        ordering = ('-date',)


class Springs(models.Model):
    spring_id = models.AutoField(primary_key=True)
    spring_name = models.CharField(max_length=7, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    geomorph = models.CharField(max_length=150, blank=True, null=True)
    head = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    aquifer = models.ForeignKey('AquiferCodes', models.DO_NOTHING, blank=True, null=True)
    spring_type = models.SmallIntegerField(blank=True, null=True)
    regime = models.SmallIntegerField(blank=True, null=True)
    natural_monument_status = models.BooleanField()
    spna = models.ForeignKey('Spna', models.DO_NOTHING, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'springs'


class SpringsRate(models.Model):
    spring = models.ForeignKey(Springs, models.CASCADE)
    date = models.DateField()
    survey = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey', blank=True, null=True)
    spring_rate = models.DecimalField(max_digits=6, decimal_places=3)
    doc = models.ForeignKey('Documents', models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'springs_rate'
        unique_together = (('date', 'spring'),)


class SpringsTemperature(models.Model):
    spring = models.ForeignKey(Springs, models.CASCADE)
    date = models.DateField()
    survey = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey', blank=True, null=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    doc = models.ForeignKey('Documents', models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'springs_temperature'
        unique_together = (('date', 'spring'),)


class SpringsSample(models.Model):
    doc = models.ForeignKey('Documents', models.CASCADE, blank=True, null=True)
    spring = models.ForeignKey(Springs, models.CASCADE)
    date = models.DateField()
    sample_id = models.AutoField(primary_key=True)
    sample_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'springs_sample'
        unique_together = (('spring', 'date'),)


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


class DocumentsAttach(models.Model):
    attachmentid = models.AutoField(primary_key=True)
    rel_doc = models.ForeignKey(Documents, models.CASCADE)
    att_name = models.CharField(max_length=250)
    data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents_attach'
        unique_together = (('rel_doc', 'att_name'),)


class SpringsInspectionAttach(models.Model):
    attachmentid = models.AutoField(primary_key=True)
    rel_doc = models.ForeignKey(SpringsInspection, models.CASCADE)
    att_name = models.CharField(max_length=250)
    data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'springs_inspection_attach'
        unique_together = (('att_name', 'rel_doc'),)


class Spna(models.Model):
    spna_id = models.IntegerField(primary_key=True)
    spna_type = models.SmallIntegerField()
    spna_name = models.CharField(unique=True, max_length=250)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'spna'