from rest_framework.views import APIView
from api.models import AnnualFullFormatted
from api.serializers import AnnualFullFormattedSerializer
from rest_framework.response import Response

# Define AnnualFullFormatted view
class AnnualFullFormattedView(APIView):
    def get(self, request, ticker):
        query = AnnualFullFormatted.objects.filter(ticker=ticker)
        serializer = AnnualFullFormattedSerializer(query, many=True)
        return Response(serializer.data)