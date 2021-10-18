from rest_framework.views import APIView
from api.models import AnnualFullFormatted
from api.serializers import AnnualFullFormattedSerializer
from rest_framework.response import Response


class AnnualFullFormattedView(APIView):
    """Send API response for general company level queries
    """
    def get(self, request, ticker):
        query = AnnualFullFormatted.objects.filter(ticker=ticker)
        serializer = AnnualFullFormattedSerializer(query, many=True)
        return Response(serializer.data)


# TODO: Add more granular endpoints