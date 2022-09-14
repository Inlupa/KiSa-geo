from django.db import models
efficiency = {0: 'Эффективен', 1: 'Частично эффективен', 2: 'Не эффективен', 4: 'Отсутствует'}
efficiency = tuple(map(tuple, efficiency.items()))
#u'null'
zero_to_3 = {None: 'нет', 0: '0', 1: '1', 2: '2', 3: '3'}
zero_to_3 = tuple(map(tuple, zero_to_3.items()))


class EgpSitesSurvey(models.Model):
    egp_site = models.ForeignKey('EgpSites', models.CASCADE)
    dates = models.CharField(max_length=100, blank=True, null=True)
    survey_information = models.CharField(max_length=300, blank=True, null=True)
    work_information = models.CharField(max_length=300, blank=True, null=True)
    survey1 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey1', related_name='survey1', blank=True, null=True)
    survey2 = models.ForeignKey('Workers', models.DO_NOTHING, db_column='survey2', related_name='survey2', blank=True, null=True)
    weather = models.CharField(max_length=300, blank=True, null=True)
    route_length = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    urban_objects = models.CharField(max_length=1500, blank=True, null=True)
    anthropogenic_impact = models.CharField(max_length=1500, blank=True, null=True)
    conclusion = models.CharField(max_length=5000, blank=True, null=True)
    agreed = models.ForeignKey('Workers', models.DO_NOTHING, db_column='agreed', related_name='agreed', blank=True, null=True)
    doc = models.OneToOneField('Documents', models.CASCADE, primary_key=True)

    class Meta:
        managed = False
        db_table = 'egp_sites_survey'
        unique_together = (('egp_site', 'dates'),)
        ordering = ('-doc_id',)


class EgpPointsSurvey(models.Model):
    egp_point = models.ForeignKey('EgpPoints', models.CASCADE)
    date = models.DateField()
    landslide_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    erosion_lateral_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    erosion_ravine_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    flat_flushing_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    scree_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    flooding_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    suffosion_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    karst_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    swamping_rate = models.SmallIntegerField(choices=zero_to_3, blank=True, null=True)
    point_description = models.CharField(max_length=1500)
    impact_buildings = models.BooleanField()
    impact_construction = models.BooleanField()
    impact_coverage = models.BooleanField()
    impact_description = models.CharField(max_length=1500)
    date_improve = models.SmallIntegerField(blank=True, null=True)
    drainage_status = models.BooleanField(blank=True, null=True)
    retaining_wall_status = models.BooleanField()
    gabion_status = models.BooleanField()
    gabion_mesh_status = models.BooleanField()
    rock_placement_status = models.BooleanField()
    geogrid_status = models.BooleanField()
    improve_efficiency = models.SmallIntegerField(choices=efficiency)
    improve_description = models.CharField(max_length=1500)
    doc = models.ForeignKey(EgpSitesSurvey, models.CASCADE, blank=True, null=True)
    objectid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'egp_points_survey'
        unique_together = (('egp_point', 'date'),)
        ordering = ('-date',)


class EgpPoints(models.Model):
    egp_point_id = models.IntegerField(primary_key=True)
    egp_point_name = models.CharField(max_length=80)
    egp_site = models.ForeignKey('EgpSites', models.CASCADE)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'egp_points'
        unique_together = (('egp_site', 'egp_point_name'),)


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


class EgpPointsSurveyAttach(models.Model):
    attachmentid = models.AutoField(primary_key=True)
    rel_doc = models.ForeignKey(EgpPointsSurvey, models.CASCADE)
    att_name = models.CharField(max_length=250)
    data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egp_points_survey_attach'
        unique_together = (('att_name', 'rel_doc'),)
