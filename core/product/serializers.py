from rest_framework import serializers
from .models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ActualProductSerializer(serializers.Serializer):
    title = serializers.CharField(source='product__title')
    lesson_count = serializers.IntegerField()
    start_date = serializers.DateField(source='product__start_date')
    start_time = serializers.TimeField(source='product__start_time')
    cost = serializers.DecimalField(max_digits=6, decimal_places=2, source='product__cost')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ['id', 'product']
