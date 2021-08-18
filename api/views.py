import datetime

import urllib3
import xmltodict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Currency, Rates
from api.serializers import CurrencySerializer


class ListCurrency(ReadOnlyModelViewSet):
    """
    Base viewset, returning currencies list
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


def get_rate(date, code):
    currency = get_object_or_404(Currency, iso_char=code)
    rate = Rates.objects.filter(date=date, currency=currency)
    if not rate.exists():
        date_cbr = datetime.date.strftime(date, '%d/%m/%Y')
        url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_cbr}'
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        data = xmltodict.parse(response.data)
        rates = data['ValCurs']['Valute']
        res = next((i for i in rates if i['CharCode'] == code), None)
        rate = float(res['Value'].replace(',', '.'))
        Rates.objects.create(
            currency=currency,
            date=date,
            rate=rate
        )
        return rate
    else:
        rate = rate.first()
        return rate.rate


class CurrencyDeltaViewSet(APIView):
    """
    Get and return in JSON currency difference
    """
    def get(self, request, *args, **kwargs):
        code = kwargs.get('currency_code')
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
        currency_diff = get_rate(start, code) - get_rate(end, code)
        currency_diff = round(currency_diff, 4)
        data = {
            'difference': currency_diff,
        }
        return JsonResponse(data)
