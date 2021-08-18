import urllib3
import xmltodict
from django.db import migrations


def update_curr(apps, schema_editor):
    Currency = apps.get_model('api', 'Currency')
    url = 'http://www.cbr.ru/scripts/XML_valFull.asp'

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    currencies = data['Valuta']['Item']
    Currency.objects.all().delete()
    for item in currencies:
        Currency.objects.create(
            name=item['Name'],
            eng_name=item['EngName'],
            nominal=item['Nominal'],
            parent_code=item['ParentCode'],
            iso_num=item['ISO_Num_Code'],
            iso_char=item['ISO_Char_Code']
        )


class Migration(migrations.Migration):
    """
    Updates currencies database
    """
    dependencies = [
        ('api', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(update_curr),
    ]
