from django.db import models


class ReconPointsSurvey(models.Model):
    recon_point = models.ForeignKey('ReconPoints', models.DO_NOTHING)
    date = models.DateField()
    point_description = models.CharField(max_length=2000)
    doc = models.ForeignKey('ReconSitesSurvey', models.DO_NOTHING, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'recon_points_survey'
        unique_together = (('recon_point', 'date'),)
        ordering = ('-date',)


class ReconSitesSurvey(models.Model):
    recon_site = models.ForeignKey('ReconSites', models.DO_NOTHING)
    dates = models.CharField(max_length=100)
    survey1 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey1', related_name='survey1')
    survey2 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey2', related_name='survey2', blank=True,
                                null=True)
    work_information = models.CharField(max_length=300, blank=True, null=True)
    survey_information = models.CharField(max_length=300, blank=True, null=True)
    weather = models.CharField(max_length=100)
    route_length = models.DecimalField(max_digits=3, decimal_places=1)
    anthropogenic_impact = models.CharField(max_length=1000)
    conclusion = models.CharField(max_length=2000)
    doc = models.OneToOneField('Documents', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'recon_sites_survey'
        unique_together = (('dates', 'recon_site'),)
        ordering = ('-doc_id',)


class ReconPoints(models.Model):
    recon_point_id = models.IntegerField(primary_key=True)
    recon_point_name = models.CharField(max_length=4)
    recon_site = models.ForeignKey('ReconSites', models.DO_NOTHING)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.


    class Meta:
        managed = False
        db_table = 'recon_points'
        unique_together = (('recon_site', 'recon_point_name'),)



class ReconSites(models.Model):
    recon_site_id = models.IntegerField(primary_key=True)
    recon_site_name = models.CharField(unique=True, max_length=50)
    position = models.CharField(max_length=300, blank=True, null=True)
    geomorph = models.CharField(max_length=1500, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.


    class Meta:
        managed = False
        db_table = 'recon_sites'


class Workers(models.Model):
    worker_id = models.SmallIntegerField(primary_key=True)
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


class Documents(models.Model):
    doc_id = models.IntegerField(primary_key=True)
    doc_type = models.SmallIntegerField()
    reg_status = models.SmallIntegerField()
    reg_number = models.CharField(max_length=15, blank=True, null=True)
    reg_date = models.DateField(blank=True, null=True)
    reg_worker = models.SmallIntegerField(blank=True, null=True)
    doc_source = models.SmallIntegerField(blank=True, null=True)
    doc_name = models.CharField(max_length=50, blank=True, null=True)
    creation_org = models.CharField(max_length=50, blank=True, null=True)
    author1 = models.SmallIntegerField(blank=True, null=True)
    author2 = models.SmallIntegerField(blank=True, null=True)
    author3 = models.SmallIntegerField(blank=True, null=True)
    author4 = models.SmallIntegerField(blank=True, null=True)
    creation_place = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    number_of_pages = models.SmallIntegerField(blank=True, null=True)
    number_of_graphic = models.SmallIntegerField(blank=True, null=True)
    paper_version = models.CharField(max_length=5, blank=True, null=True)
    digital_version = models.CharField(max_length=5, blank=True, null=True)
    secrecy = models.SmallIntegerField(blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'
        unique_together = (('doc_name', 'doc_type'),)



