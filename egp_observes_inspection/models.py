from django.db import models


class EgpObserves(models.Model):
    egp_obs_id = models.IntegerField(primary_key=True)
    egp_obs_name = models.CharField(max_length=80)
    egp_obs_type = models.SmallIntegerField()
    position = models.CharField(max_length=300, blank=True, null=True)
    geomorph = models.CharField(max_length=150, blank=True, null=True)
    head = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    egp_site = models.ForeignKey('EgpSites', models.DO_NOTHING)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'egp_observes'
        unique_together = (('egp_site', 'egp_obs_name', 'egp_obs_type'),)


class EgpSites(models.Model):
    egp_site_id = models.IntegerField(primary_key=True)
    egp_site_name = models.CharField(unique=True, max_length=50)
    egp_site_type = models.SmallIntegerField()
    position = models.CharField(max_length=300, blank=True, null=True)
    geomorph = models.CharField(max_length=1500, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'egp_sites'


class EgpObservesInspection(models.Model):
    egp_obs = models.ForeignKey(EgpObserves, models.DO_NOTHING)
    date = models.DateField()
    survey1 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey1', related_name='survey1')
    survey2 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey2', related_name='survey2', blank=True, null=True)
    painting_condition = models.SmallIntegerField()
    label_condition = models.SmallIntegerField()
    damage_description = models.CharField(max_length=300, blank=True, null=True)
    logs_status = models.CharField(max_length=5)
    logs_results = models.CharField(max_length=300, blank=True, null=True)
    comments = models.CharField(max_length=300, blank=True, null=True)
    recommendations = models.CharField(max_length=300, blank=True, null=True)
    doc = models.OneToOneField('Documents', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'egp_observes_inspection'
        unique_together = (('egp_obs', 'date'),)
        ordering = ('-date',)


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


class EgpObservesCondition(models.Model):
    egp_obs = models.ForeignKey(EgpObserves, models.DO_NOTHING)
    date = models.DateField()
    condition = models.SmallIntegerField()
    egp_obs_depth = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    doc = models.ForeignKey(Documents, models.DO_NOTHING, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'egp_observes_condition'
        unique_together = (('egp_obs', 'date'),)
