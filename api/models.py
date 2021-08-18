from django.db import models


class Currency(models.Model):
    """
    A separate class for base currencies info storage
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Название валюты (rus)'
    )
    eng_name = models.CharField(
        max_length=255,
        verbose_name='Название валюты (eng)'
    )
    nominal = models.PositiveSmallIntegerField(
        verbose_name='Номинал единицы'
    )
    parent_code = models.CharField(
        max_length=255,
        verbose_name='Parent code',
    )
    iso_num = models.PositiveSmallIntegerField(
        verbose_name='Числовой ISO код',
        null=True, blank=True
    )
    iso_char = models.CharField(
        max_length=255,
        verbose_name='Символьный ISO код',
        null=True, blank=True
    )


class Rates(models.Model):
    """
    Class for currency rates caching
    """
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE,
        related_name='currency', verbose_name='валюта'
    )
    rate = models.FloatField(verbose_name='Котировка')
    date = models.DateField(verbose_name='Дата')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('currency', 'rate', 'date'),
                name='Котировка валюты на день'
            )
        ]
