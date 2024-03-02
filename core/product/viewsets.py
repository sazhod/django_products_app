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
from .permissions import IsTeacherReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Для модели Product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def gaining_access(self, request, pk=None):
        """
        Endpoint products/<int>/gaining_access/
        method POST
        Отвечает за предоставление авторизованному пользователю доступа к продукту.
        Вызывает метод автоматического распределения пользователей по группам.
        """
        try:
            if pk and (group := user_allocation_algorithm(request, pk)) is not None:
                return Response({'status': f'Вы получили доступ к продукту. Вы были добавлены в группу {group.title}'},
                                status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'status': 'Вы уже зарегистрированы в данном продукте.'}, status=status.HTTP_409_CONFLICT)

        return Response({'status': 'Подходящая группа не найдена.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def actual(self, request):
        """
        Endpoint products/actual/
        method GET
        Отвечает за предоставление авторизованному пользователю списка не начатых продуктов.
        """
        products = Product.actual.all()

        if products:
            serializer = ActualProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'status': 'Продукты, доступные для покупки, отсутствуют.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_lessons(self, request, pk=None):
        """
        Endpoint products/<int>/get_lessons
        method GET
        Отвечает за предоставление авторизованному пользователю с ролью студента списка уроков
            связанных с его продуктом.
        """
        has_access = StudentInGroup.objects.filter(
            student=request.user,
            group__pk__in=Group.objects.all().values('product').filter(product__pk=pk).values('pk')).exists()

        if not has_access:
            return Response({'status': 'Отказано в доступе.'}, status=status.HTTP_403_FORBIDDEN)

        lessons = Lesson.objects.filter(product__pk=pk).select_related()
        if lessons:
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'status': 'Уроки не предоставлены.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsTeacherReadOnly])
    def statistics(self, request):
        products = self.get_queryset()

        return Response({'status': 'Уроки не предоставлены.'}, status=status.HTTP_200_OK)
