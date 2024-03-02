from django.db import IntegrityError
from django.db.models import Count, F, Value, Q, Exists, OuterRef
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Group, StudentInGroup, Lesson
from .serializers import ProductSerializer, ActualProductSerializer, LessonSerializer
from .utils import user_allocation_algorithm
from django.utils import timezone


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def gaining_access(self, request, pk=None):
        try:
            if pk and (group := user_allocation_algorithm(request, pk)) is not None:
                return Response({'status': f'Вы получили доступ к продукту. Вы были добавлены в группу {group.title}'},
                                status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'status': 'Вы уже зарегистрированы в данном продукте.'}, status=status.HTTP_409_CONFLICT)

        return Response({'status': 'Подходящая группа не найдена.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def actual(self, request):
        products = Product.actual.all()
        serializer = ActualProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_lessons(self, request, pk=None):
        lessons = Lesson.objects.filter(product__pk=pk).select_related()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

