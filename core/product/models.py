from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Count, OuterRef
from django.utils import timezone


User = get_user_model()


class ActualProductManager(models.Manager):
    def get_queryset(self):
        return Lesson.objects.values('product').filter(product__start_date__gte=timezone.localdate()).annotate(
            lesson_count=Count('product')).prefetch_related('product').values(
            'product__title', 'lesson_count', 'product__start_date',
            'product__start_time', 'product__cost')


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': settings.TEACHER})
    title = models.CharField(max_length=255, verbose_name='Название')
    start_date = models.DateField(verbose_name='Дата старта', null=True)
    start_time = models.TimeField(verbose_name='Время старта')
    cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')

    objects = models.Manager()
    actual = ActualProductManager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def clean(self):
        super().clean()
        if self.start_date <= timezone.localdate():
            raise ValidationError('Дата начала должна быть позже текущей даты!')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255, verbose_name='Название')
    link = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    min_number_of_user = models.PositiveSmallIntegerField(verbose_name='Минимальное количество учеников')
    max_number_of_user = models.PositiveSmallIntegerField(verbose_name='Максимальное количество учеников')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def clean(self):
        super().clean()
        if self.max_number_of_user <= self.min_number_of_user:
            raise ValidationError('Максимальное количество учеников должно быть больше минимального!')

    def __str__(self):
        return self.title


class StudentInGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': settings.STUDENT})

    class Meta:
        verbose_name = 'Студент в группе'
        verbose_name_plural = 'Студенты в группах'
        constraints = [
            models.UniqueConstraint(
                fields=("group", "student"), name="unique_student_in_group"
            ),
        ]

    def __str__(self):
        return f'{self.group}_{self.student.email}'
