from django.db import models


class License(models.Model):
    license_id = models.CharField(unique=True, max_length=10)
    department = models.SmallIntegerField()
    subject = models.CharField(max_length=300)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField()
    status = models.SmallIntegerField()
    comments = models.CharField(max_length=1000, blank=True, null=True)
    doc = models.OneToOneField('Documents', models.DO_NOTHING, primary_key=True)
    objectid = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'license'


class LicenseToWells(models.Model):
    well = models.ForeignKey('Wells', models.DO_NOTHING)
    flow_rate = models.DecimalField(max_digits=9, decimal_places=4)
    license = models.ForeignKey(License, models.DO_NOTHING)
    objectid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'license_to_wells'
        unique_together = (('well', 'license'),)


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
    objectid = models.IntegerField(unique=True)
    gdb_geomattr_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wells'


class SubsurfaceSites(models.Model):
    subsurface_site_id = models.IntegerField(primary_key=True)
    subsurface_site_name = models.CharField(max_length=100, blank=True, null=True)
    mineral = models.SmallIntegerField()
    deposit_site_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    deposit = models.ForeignKey('FieldsGeneral', models.DO_NOTHING, blank=True, null=True)
    gmsn_id = models.IntegerField(blank=True, null=True)
    uib_id = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    objectid = models.IntegerField(unique=True)
    gdb_geomattr_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subsurface_sites'


class FieldsGeneral(models.Model):
    deposit_id = models.IntegerField(primary_key=True)
    deposit_name = models.CharField(unique=True, max_length=93, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    objectid = models.IntegerField(unique=True)
    gdb_geomattr_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fields_general'


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
    objectid = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'documents'
        unique_together = (('doc_name', 'doc_type'),)


class AquiferCodes(models.Model):
    aquifer_id = models.SmallIntegerField(primary_key=True)
    aquifer_name = models.CharField(max_length=150)
    aquifer_index = models.CharField(unique=True, max_length=50)
    objectid = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'aquifer_codes'
