from rest_framework import serializers
from .models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ActualProductSerializer(serializers.ModelSerializer):

    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ['user']

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(product=obj).count()


