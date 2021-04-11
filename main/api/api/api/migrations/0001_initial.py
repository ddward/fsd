# Generated by Django 3.1.4 on 2021-01-29 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualFullFormatted',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('ticker', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('cik', models.IntegerField(blank=True, db_column='CIK', null=True)),
                ('cik2', models.TextField(blank=True, null=True)),
                ('industry', models.TextField(blank=True, db_column='Industry', null=True)),
                ('sub_industry', models.TextField(blank=True, db_column='Sub_Industry', null=True)),
                ('report_type', models.TextField(blank=True, db_column='Report_Type', null=True)),
                ('report_id', models.TextField(blank=True, db_column='Report_id', null=True)),
                ('source', models.TextField(blank=True, db_column='Data_Link', null=True)),
                ('report_date', models.TextField(blank=True, db_column='submission_date', null=True)),
                ('instant_date', models.TextField(blank=True, null=True)),
                ('year_ending', models.TextField(blank=True, db_column='end_date', null=True)),
                ('earningspersharediluted', models.FloatField(blank=True, null=True)),
                ('earningspersharebasic', models.FloatField(blank=True, null=True)),
                ('earningspersharebasicanddiluted', models.FloatField(blank=True, null=True)),
                ('cashandcashequivalentsatcarryingvalue', models.FloatField(blank=True, null=True)),
                ('cash', models.FloatField(blank=True, null=True)),
                ('cashandduefrombanks', models.FloatField(blank=True, null=True)),
                ('netincomeloss', models.FloatField(blank=True, null=True)),
                ('profitloss', models.FloatField(blank=True, null=True)),
                ('operatingincomeloss', models.FloatField(blank=True, null=True)),
                ('assetscurrent', models.FloatField(blank=True, null=True)),
                ('assets', models.FloatField(blank=True, null=True)),
                ('liabilities', models.FloatField(blank=True, null=True)),
                ('stockholdersequity', models.FloatField(blank=True, null=True)),
                ('stockholdersequityincludingportionattributabletononcontrollinginterest', models.TextField(blank=True, null=True)),
                ('liabilitiesandstockholdersequity', models.FloatField(blank=True, null=True)),
                ('accountspayablecurrent', models.FloatField(blank=True, null=True)),
                ('accountsreceivablenetcurrent', models.FloatField(blank=True, null=True)),
                ('inventorynet', models.FloatField(blank=True, null=True)),
                ('researchanddevelopmentexpense', models.FloatField(blank=True, null=True)),
                ('link_count', models.IntegerField(blank=True, null=True)),
                ('ticker_count', models.TextField(blank=True, null=True)),
                ('cik_count', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'annual_full_formatted_distinct',
                'managed': True,
            },
        ),
    ]
