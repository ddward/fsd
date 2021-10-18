from rest_framework import serializers

from api.models import AnnualFullFormatted


class AnnualFullFormattedSerializer(serializers.ModelSerializer):
    """Serializers for API representation"""
    class Meta:
        model = AnnualFullFormatted
        fields = [
            "source",
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
            "stockholdersequityincludingnoncontrollinginterest",
            "liabilitiesandstockholdersequity",
            "accountspayablecurrent",
            "accountsreceivablenetcurrent",
            "inventorynet",
            "researchanddevelopmentexpense",
        ]