from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from .serializers import CustomUserSerializer


User = get_user_model()


class AllUsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all().exclude(role=settings.SUPERUSER)
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class TeachersListAPIView(generics.ListAPIView):
    queryset = User.teachers.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class StudentsListAPIView(generics.ListAPIView):
    queryset = User.students.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UndefinedUsersListAPIView(generics.ListAPIView):
    queryset = User.undefined_users.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, *args, **kwargs):
        if not pk:
            raise
        instance = get_object_or_404(User.objects, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            pass

        return Response(serializer.data)
