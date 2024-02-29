from django.db.models import Count, F, Value, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Group, StudentInGroup
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def gaining_access(self, request, pk=None):
        user = request.user
        student_in_group = StudentInGroup.objects.filter()
        group = Group.objects.annotate(c=Count('studentingroup')).exclude(c=F('max_number_of_user')).filter(product=pk).order_by('c').first()
        print(group, user)
        if group:
            student_in_group = StudentInGroup(group=group, student=user)
            student_in_group.save()

            return Response({'status': f'Вы получили доступ к продукту. Вы были добавлены в группу {group.title}'})
        return Response({'status': 'Произошла ошибка.'})

