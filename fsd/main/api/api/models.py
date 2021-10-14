# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnnualFullFormatted(models.Model):
    # rowid = models.AutoField(db_column="rowid", primary_key=True)
    ticker = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    source = models.TextField(db_column="Data_Link", blank=True, null=True)
    year_ending = models.TextField(db_column="end_date", blank=True, null=True)
    earningspersharediluted = models.FloatField(blank=True, null=True)
    earningspersharebasic = models.FloatField(blank=True, null=True)
    earningspersharebasicanddiluted = models.FloatField(blank=True, null=True)
    cashandcashequivalentsatcarryingvalue = models.FloatField(blank=True, null=True)
    cash = models.FloatField(blank=True, null=True)
    cashandduefrombanks = models.FloatField(blank=True, null=True)
    netincomeloss = models.FloatField(blank=True, null=True)
    profitloss = models.FloatField(blank=True, null=True)
    operatingincomeloss = models.FloatField(blank=True, null=True)
    assetscurrent = models.FloatField(blank=True, null=True)
    assets = models.FloatField(blank=True, null=True)
    liabilities = models.FloatField(blank=True, null=True)
    stockholdersequity = models.FloatField(blank=True, null=True)
    stockholdersequityincludingnoncontrollinginterest = (models.TextField(
        blank=True, null=True))
    liabilitiesandstockholdersequity = models.FloatField(blank=True, null=True)
    accountspayablecurrent = models.FloatField(blank=True, null=True)
    accountsreceivablenetcurrent = models.FloatField(blank=True, null=True)
    inventorynet = models.FloatField(blank=True, null=True)
    researchanddevelopmentexpense = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "annual_full_formatted_distinct"
