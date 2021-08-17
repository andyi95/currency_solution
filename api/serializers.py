from rest_framework import serializers

from api.models import Currency


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('name', 'eng_name', 'nominal',
                  'parent_code', 'iso_num', 'iso_char')
