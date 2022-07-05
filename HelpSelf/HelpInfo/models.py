# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Computers(models.Model):
    id = models.AutoField(db_column='Id', unique=True, primary_key=True)
    bios_serial = models.TextField(db_column='BIOS_Serial', unique=True, blank=True, null=True)
    comp_name = models.TextField(db_column='Comp_Name', unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Computers'


class Ipees(models.Model):
    id = models.AutoField(db_column='Id', unique=True, primary_key=True)
    ip = models.TextField(db_column='IP', unique=True, blank=True, null=True)
    status = models.IntegerField(db_column='Status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IPees'


class Users(models.Model):
    id = models.AutoField(db_column='Id', unique=True, primary_key=True)
    user = models.TextField(db_column='User', blank=True, null=True)
    domain = models.TextField(db_column='Domain', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class Info(models.Model):
    id = models.AutoField(db_column='Id', unique=True, primary_key=True)
    comp = models.ForeignKey(Computers, models.DO_NOTHING, db_column='Comp_Id', blank=True,
                             null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='User_Id', blank=True, null=True)
    ip = models.ForeignKey(Ipees, models.DO_NOTHING, related_name='IP_Id', db_column='IP_Id', blank=True, null=True)
    status = models.ForeignKey(Ipees, models.DO_NOTHING, related_name='Status_Id', db_column='Status_Id', blank=True,
                               null=True)

    class Meta:
        managed = False
        db_table = 'Info'
