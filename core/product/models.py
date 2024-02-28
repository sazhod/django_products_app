from django.db import models
from django.conf import settings


class Product(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': settings.TEACHER})
    title = models.CharField(max_length=255, verbose_name='Название')
    start_date = models.DateField(verbose_name='Дата старта', null=True)
    start_time = models.TimeField(verbose_name='Время старта')
    cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    link = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    min_number_of_user = models.PositiveSmallIntegerField(verbose_name='Минимальное количество учеников')
    max_number_of_user = models.PositiveSmallIntegerField(verbose_name='Максимальное количество учеников')
    students = models.ManyToManyField('user.CustomUser', limit_choices_to={'role': settings.STUDENT})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
