from django.db import models


class Staff(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения')
    role = models.CharField(max_length=100, verbose_name='Должность')

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name

