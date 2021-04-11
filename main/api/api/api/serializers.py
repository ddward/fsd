from rest_framework import serializers

from api.models import AnnualFullFormatted

# Serializers for API representation
class AnnualFullFormattedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnualFullFormatted
        fields = ["source",
            "ticker",
            "name",
            "year_ending",
            "earningspersharediluted",
            "earningspersharebasic",
            "earningspersharebasicanddiluted",
            "cashandcashequivalentsatcarryingvalue",
            "cash",
            "cashandduefrombanks",
            "netincomeloss",
            "profitloss",
            "operatingincomeloss",
            "assetscurrent",
            "assets",
            "liabilities",
            "stockholdersequity",
            "stockholdersequityincludingportionattributabletononcontrollinginterest",
            "liabilitiesandstockholdersequity",
            "accountspayablecurrent",
            "accountsreceivablenetcurrent",
            "inventorynet",
            "researchanddevelopmentexpense",
        ]