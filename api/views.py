import datetime

import urllib3
import xmltodict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Currency
from api.serializers import CurrencySerializer


class ListCurrency(ReadOnlyModelViewSet):
    """
    Base viewset, returning currencies list
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


def get_rate(date, code):
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    rates = data['ValCurs']['Valute']
    res = next((i for i in rates if i['CharCode'] == code), None)
    return float(res['Value'].replace(',', '.'))


class CurrencyDeltaViewSet(APIView):
    """
    Get and return in JSON currency difference
    """
    def get(self, request, *args, **kwargs):
        code = kwargs.get('currency_code')
        if not Currency.objects.filter(iso_char=code).exists():
            return Response(
                'The currency code not found',
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            start = datetime.datetime.strptime(
                request.query_params.get('start'), '%Y-%m-%d'
            )
            end = datetime.datetime.strptime(
                request.query_params.get('end'), '%Y-%m-%d'
            )
        except TypeError:
            end = datetime.datetime.now()
            start = end - datetime.timedelta(days=1)

        start_cbr = datetime.date.strftime(start, '%d/%m/%Y')
        end_cbr = datetime.date.strftime(end, '%d/%m/%Y')
        currency_diff = get_rate(start_cbr, code) - get_rate(end_cbr, code)
        currency_diff = round(currency_diff, 4)
        data = {
            'difference': currency_diff,
        }
        return JsonResponse(data)


@api_view(['GET'])
def update_currencies(request):
    """
    Updates currencies database
    """
    url = 'http://www.cbr.ru/scripts/XML_valFull.asp'

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    currencies = data['Valuta']['Item']
    Currency.objects.all().delete()
    for item in currencies:
        print(item)
        Currency.objects.create(
            name=item['Name'],
            eng_name=item['EngName'],
            nominal=item['Nominal'],
            parent_code=item['ParentCode'],
            iso_num=item['ISO_Num_Code'],
            iso_char=item['ISO_Char_Code']
        )
    return Response(data=None, status=status.HTTP_201_CREATED)
