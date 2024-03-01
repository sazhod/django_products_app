from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='products')

urlpatterns = [

]

urlpatterns += router.urls
