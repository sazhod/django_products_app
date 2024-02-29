from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (AllUsersListAPIView, TeachersListAPIView, StudentsListAPIView,
                    UndefinedUsersListAPIView, UserRetrieveAPIView, UserCreateAPIView)

router = DefaultRouter()
# router.register(r'users', CustomUserModelViewSet, basename='users')

urlpatterns = [
    path('all/', AllUsersListAPIView.as_view()),
    path('teachers/', TeachersListAPIView.as_view()),
    path('students/', StudentsListAPIView.as_view()),
    path('undefined/', UndefinedUsersListAPIView.as_view()),
    path('<int:pk>/', UserRetrieveAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),
]

# urlpatterns += router.urls
