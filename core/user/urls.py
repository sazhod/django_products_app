from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserListAPIView, UserRetrieveAPIView, UserCreateAPIView

router = DefaultRouter()
# router.register(r'users', CustomUserModelViewSet, basename='users')

urlpatterns = [
    path('users/', UserListAPIView.as_view()),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view()),
    path('users/create/', UserCreateAPIView.as_view()),
]

# urlpatterns += router.urls
